from fyers_api import fyersModel
from fyers_api import accessToken
import requests
import datetime
import pandas as pd
import time
import pytz
from credentials import *


# Below code prints the Auth code for the fyers API

session=accessToken.SessionModel(client_id=client_id, secret_key=secret_key,redirect_uri=redirect_uri,
response_type=response_type, grant_type=grant_type,
state=state,nonce=nonce)
url = session.generate_authcode()
response = requests.get(url)
print(response.url)
response = session.generate_authcode()
print(response)


# Once this step is done copy the Auth code and head to gen_access_token