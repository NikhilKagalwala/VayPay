# import time
# import json
# from flask import jsonify
# import plaid
# import datetime as dt
# import mysql.connector
# import db_creds
# # import plaid.configuration
# from plaid import Configuration
# # import plaid.plaid
# # import plaid.plaid
# import plaid.yml_check
# from plaid.model.products import Products
# from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
# from plaid.model.sandbox_public_token_create_request_options import SandboxPublicTokenCreateRequestOptions
# from plaid.model.sandbox_public_token_create_request_options_transactions import SandboxPublicTokenCreateRequestOptionsTransactions
# from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
# from plaid.model.transactions_get_request import TransactionsGetRequest
# from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
# from plaid.model.item_remove_request import ItemRemoveRequest
# from plaid.model.transactions_refresh_request import TransactionsRefreshRequest

# # from util import (
# #     create_client,
# #     SANDBOX_INSTITUTION,
# # )

# access_token = None

# # NOTE: Data is only generated over the past 2 years.  Ensure that the date
# # range used for transactions/get is within 2 years old
# END_DATE = dt.date.today()
# START_DATE = (END_DATE - dt.timedelta(days=(10)))
# def create_client():
#     '''Create a new client for testing.'''
#     configuration = Configuration(
#         host=plaid.plaid.Environment.sandbox,
#         api_key={
#             'clientId': client_id,
#             'secret': secret,
#             'plaidVersion': '2020-09-14'
#         }
#     )

# client = create_client()
# pt_request = SandboxPublicTokenCreateRequest(
#     institution_id=SANDBOX_INSTITUTION,
#     client_id = "2",
#     initial_products=[Products('transactions')],
#     options=SandboxPublicTokenCreateRequestOptions(
#         transactions=SandboxPublicTokenCreateRequestOptionsTransactions(
#             start_date=START_DATE,
#             end_date=END_DATE,
#         )
#     )
# )
# pt_response = client.sandbox_public_token_create(pt_request)
# exchange_request = ItemPublicTokenExchangeRequest(
#     public_token=pt_response['public_token']
# )
# exchange_response = client.item_public_token_exchange(exchange_request)
# access_token = exchange_response['access_token']
# print(access_token)
# print("============================================")
# options = TransactionsGetRequestOptions()
# time.sleep(1)
# request = TransactionsGetRequest(
#                 access_token=access_token,
#                 start_date=START_DATE,
#                 end_date=END_DATE,
#                 options=options
#                 )
# response = client.transactions_get(request)
# print(response['transactions'])

# def get_transactions_user(user_id, start_date, end_date):
#     # TODO: Write Code here to query the user_information table with the user_id and retrieve the access token and users name
#     # create a cursor
#     # open connection
#     conn = mysql.connector.connect(**db_creds.db_config)
#     cursor = conn.cursor()

#     query_user_info = "SELECT first_name, access_token FROM user_information WHERE user_id = %s"
#     cursor.execute(query_user_info % (user_id))
#     print(cursor.fetchall())

    
#     user_first_name = "Test User 1"
#     access_token = "access-sandbox-3279643b-4eb9-466b-bf32-4a7e36ccc070"
#     # Assuming you have an access token
#     if access_token == None:
#         return jsonify([])
#     data_list = []
#     client = create_client()
#     options = TransactionsGetRequestOptions()
#     request = TransactionsGetRequest(
#                 access_token=access_token,
#                 start_date=start_date,
#                 end_date=end_date,
#                 options=options
#                 )
#     transactions_response = client.transactions_get(request)
#     data_list = []
#     for transaction in transactions_response['transactions']:
#         # Add in the insert into the transactions table here
#         transaction_data = {
#             'date': transaction['date'], # Check if date is actually something
#             'spent_by': user_first_name,
#             'amount': transaction['amount'],
#             'merchant': transaction.get('merchant', {}).get('name', 'N/A'),
#         }
#         if (transaction['date'] >= start_date and transaction['date'] <= end_date):
#             data_list.append(transaction_data)
            
#     return jsonify(data_list)

# print("testing\n")
# current_date = dt.now()
# # Calculate the start date as 3 weeks ago
# start_date = current_date - dt.timedelta(weeks=3)
# # Calculate the end date as the start date plus 7 days (1 week)
# end_date = start_date + dt.timedelta(days=7)
# get_transactions_user(4, start_date, end_date)