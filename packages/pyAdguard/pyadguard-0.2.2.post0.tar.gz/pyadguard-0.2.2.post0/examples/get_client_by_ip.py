# %% imports
from pyadguard import AdguardAPI
from dotenv import dotenv_values

config = dotenv_values(".env")

# %% create an instance of AdguardAPI
adguard = AdguardAPI(
    host=config["ADGUARD_HOST"],
    username=config["ADGUARD_USERNAME"],
    password=config["ADGUARD_PASSWORD"],
    backend="https"
)
# %% get a client by IP

# the url is /clients/find
print(adguard.clients.find.get(params={'ip0': '192.168.2.142'}))
# %%
