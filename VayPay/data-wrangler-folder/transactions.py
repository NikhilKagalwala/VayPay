import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode


# Set your Plaid API credentials
PLAID_CLIENT_ID = '655010f30811d6001b5bc2f1'
PLAID_SECRET = '3b2a315d2d845c70b24c4fedf57589'
PLAID_ENV = 'sandbox'  # or 'development' or 'production'

configuration = plaid.Configuration(
  host=plaid.Environment.Sandbox,
  api_key={
    'clientId': '655010f30811d6001b5bc2f1',
    'secret': '3b2a315d2d845c70b24c4fedf57589',
  }
)

SANDBOX_INSTITUTION = 'ins_109508'
SANDBOX_INSTITUTION_NAME = 'First Platypus Bank'

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# Create a link token (this is used to initialize the Plaid Link UI)
request = LinkTokenCreateRequest(
            products=[Products("transactions")],
            client_name="Plaid Test App",
            country_codes=[CountryCode('US')],
            redirect_uri='https://chat.openai.com',
            language='en',
            webhook='https://webhook.example.com',
            user=LinkTokenCreateRequestUser(
                client_user_id="1"
            )
        )
response = client.link_token_create(request)
print(response)

# Get the link token
link_token = response['link_token']

# Print the link token (you would typically send this to your frontend)
print("Link Token:", link_token)

# Now the user will click on the link generated and connect their bank account.

# After the user has linked their account, you will have a public token.
# Exchange the public token for an access token and item ID
# request = ItemPublicTokenExchangeRequest(
#   public_token= '/sandbox/item/public_token/create',
# )
pt_request = SandboxPublicTokenCreateRequest(
    institution_id="TEST INSTITUTION",
    initial_products=[Products('transactions')]
)
pt_response = client.sandbox_public_token_create(pt_request)
# The generated public_token can now be
# exchanged for an access_token
exchange_request = ItemPublicTokenExchangeRequest(
    public_token=pt_response['public_token']
)
exchange_response = client.item_public_token_exchange(exchange_request)

# response = client.item_public_token_exchange(request)
access_token = exchange_response['access_token']
item_id = exchange_response['item_id']


# Retrieve transactions for the last 30 days
start_date = '2023-01-01'  # Replace with your desired start date
end_date = '2023-02-01'    # Replace with your desired end date
transactions_response = client.Transactions.get(
    access_token,
    start_date=start_date,
    end_date=end_date,
)

# Print transactions
print("Transactions:", transactions_response['transactions'])
