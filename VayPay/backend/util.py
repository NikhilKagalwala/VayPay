'''Shared objects for integration testing.'''

import os
import plaid
from plaid.api import plaid_api

client_id = '655010f30811d6001b5bc2f1'
secret = '3b2a315d2d845c70b24c4fedf57589'

def create_client():
    '''Create a new client for testing.'''
    configuration = plaid.Configuration(
        host=plaid.Environment.Sandbox,
        api_key={
            'clientId': client_id,
            'secret': secret,
            'plaidVersion': '2020-09-14'
        }
    )

    api_client = plaid.ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)


    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)

SANDBOX_INSTITUTION = 'ins_109508'
SANDBOX_INSTITUTION_NAME = 'First Platypus Bank'

SANDBOX_INSTITUTIONS = [
    'ins_109508',
    'ins_109509',
    'ins_109510',
    'ins_109511',
    'ins_109512',
]

WEBHOOK_VERIFICATION_KEY_ID = '6c5516e1-92dc-479e-a8ff-5a51992e0001'