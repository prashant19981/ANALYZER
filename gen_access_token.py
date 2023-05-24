from fyers_api import accessToken
import requests
from credentials import *



# Copy the generated Auth Code in gen_auth_code and paste it below

auth_code = ""
session=accessToken.SessionModel(client_id=client_id,
secret_key=secret_key,redirect_uri=redirect_uri,
response_type=response_type, grant_type=grant_type,
state=state,nonce=nonce)
session.set_token(auth_code)
response = session.generate_token()
print(response)
access_token = response["access_token"]