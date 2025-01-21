import json
import logging
import requests
import posixpath
from urllib import parse as urlparse
from http import client as httplib


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

logging.getLogger("urllib3").setLevel(logging.DEBUG)
logging.getLogger("urllib3").propagate = True


# https://metacpan.org/pod/AnyEvent::HTTP
ANYEVENT_HTTP_STATUS_CODES = {
    595: "Errors during connection establishment, proxy handshake",
    596: "Errors during TLS negotiation, request sending and header processing",
    597: "Errors during body receiving or processing",
    598: "User aborted request via on_header or on_body",
    599: "Other, usually nonretryable, errors (garbled URL etc.)",
}


class ResourceException(Exception):
    """
    An Exception thrown when an Adguard API call failed
    """

    def __init__(self, status_code, status_message, content, errors=None):
        """
        Create a new ResourceException

        :param status_code: The HTTP status code (faked by non-HTTP backends)
        :type status_code: int
        :param status_message: HTTP Status code (faked by non-HTTP backends)
        :type status_message: str
        :param content: Extended information on what went wrong
        :type content: str
        :param errors: Any specific errors that were encountered (converted to string), defaults to None
        :type errors: Optional[object], optional
        """
        self.status_code = status_code
        self.status_message = status_message
        self.content = content
        self.errors = errors
        if errors is not None:
            content += f" - {errors}"
        message = f"{status_code} {status_message}: {content}".strip()
        super().__init__(message)


class JsonSimpleSerializer:
    def loads(self, response):
        try:
            return json.loads(response.content)
        except (UnicodeDecodeError, ValueError):
            return {"errors": response.content}

    def loads_errors(self, response):
        try:
            return json.loads(response.text).get("errors")
        except (UnicodeDecodeError, ValueError):
            return {"errors": response.content}


class AdguardResource:
    def __init__(self, **kwargs):
        self._store = kwargs

    def __repr__(self):
        return f"AdguardResource ({self._store.get('base_url')})"

    def __getattr__(self, item):
        if item.startswith("_"):
            raise AttributeError(item)

        kwargs = self._store.copy()
        kwargs["base_url"] = self.url_join(self._store["base_url"], item)
        return AdguardResource(**kwargs)

    def url_join(self, base, *args):
        scheme, netloc, path, query, fragment = urlparse.urlsplit(base)
        path = path if len(path) else "/"
        path = posixpath.join(path, *[str(x) for x in args])
        return urlparse.urlunsplit([scheme, netloc, path, query, fragment])

    def __call__(self, resource_id=None):
        if resource_id in (None, ""):
            return self

        if isinstance(resource_id, (bytes, str)):
            resource_id = resource_id.split("/")
        elif not isinstance(resource_id, (tuple, list)):
            resource_id = [str(resource_id)]

        kwargs = self._store.copy()
        if resource_id is not None:
            kwargs["base_url"] = self.url_join(self._store["base_url"], *resource_id)

        return AdguardResource(**kwargs)

    def _request(self, method, data=None, params=None):
        url = self._store["base_url"]
        logger.info(f"{method} {url} with data: {data}")

        # Clean up None values in data and params
        if params:
            params = {k: v for k, v in params.items() if v is not None}
            params = params['params']

        if data:
            data = {k: v for k, v in data.items() if v is not None}
            data = data['data']
        try:
            # Use json parameter for proper serialization
            resp = self._store["session"].request(method, url, json=data, params=params)
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise

        logger.debug(f"Status code: {resp.status_code}, output: {resp.content!r}")

        if resp.status_code >= 400:
            if hasattr(resp, "reason"):
                raise ResourceException(
                    resp.status_code,
                    httplib.responses.get(
                        resp.status_code, ANYEVENT_HTTP_STATUS_CODES.get(resp.status_code)
                    ),
                    resp.reason,
                    errors=(self._store["serializer"].loads_errors(resp)),
                )
            else:
                raise ResourceException(
                    resp.status_code,
                    httplib.responses.get(
                        resp.status_code, ANYEVENT_HTTP_STATUS_CODES.get(resp.status_code)
                    ),
                    resp.text,
                )
        elif 200 <= resp.status_code <= 299:
            return self._store["serializer"].loads(resp)

    def get(self, *args, **params):
        return self(args)._request("GET", params=params)

    def post(self, *args, **data):
        return self(*args)._request("POST", data=data)

    def put(self, *args, **data):
        return self(args)._request("PUT", data=data)

    def delete(self, *args, **params):
        return self(args)._request("DELETE", params=params)

    def create(self, *args, **data):
        return self.post(*args, **data)

    def set(self, *args, **data):
        return self.put(*args, **data)


class AdguardAPI(AdguardResource):
    def __init__(self, host, username, password, backend="https", **kwargs):
        super().__init__(**kwargs)
        backend = backend.lower()

        self._backend_name = backend

        self.session = requests.Session()
        self.session.auth = (username, password)

        self._store = {
            "base_url": f"{backend}://{host}/control",
            "session": self.session,
            "serializer": JsonSimpleSerializer(),
        }

    def __repr__(self):
        dest = getattr(self._backend, "target", self._store.get("base_url"))
        return f"AdguardAPI ({self._backend_name} backend for {dest})"
