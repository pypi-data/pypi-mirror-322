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
# %% add a rewrite to the AdGuard Home instance

# the url is /rewrite/add
rewrite = adguard.rewrite.add.create(data={
    "domain": "example.com",
    "answer": "example.org",
})
print(rewrite)
# %%
