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
# %% read the rewrites of the AdGuard Home instance

# the url is /rewrite/list
rewrites = adguard.rewrite.list.get()
print(rewrites)
# %%
