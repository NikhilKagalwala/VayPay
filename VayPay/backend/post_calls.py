import json
import mysql.connector
import db_creds
from datetime import datetime
from flask import Flask, jsonify, request
from datetime import timedelta
from random import randint
import plaid_connect
import hashlib

def hash_password(password):
    # Choose a secure hashing algorithm (e.g., SHA-256)
    hasher = hashlib.sha256()
    # Update the hasher with the password encoded as bytes
    hasher.update(password.encode('utf-8'))
    # Return the hexadecimal representation of the hash
    return hasher.hexdigest()

def validateLogin(input):
    existing_user_id = None
    try:
        # create a cursor
        # open connection
        conn = mysql.connector.connect(**db_creds.db_config)
        cursor = conn.cursor()
        print(1)
        # hashed_password = hash_password(input["password_hash"])
        password = hash_password(input["password_hash"])
        print('03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4')
        # Check if the login already exists in the user_information table
        check_query = "SELECT user_id FROM user_information WHERE email = %s AND password_hash = %s"
        print(1.5)
        cursor.execute(check_query, (input["email"], str(password)))
        print(2)
        existing_user_id = cursor.fetchone()[0]

    except mysql.connector.Error as err:
        print(f"Error: {err}")    
    
    finally:
        # close connection
        cursor.close()
        conn.close()
        # If the login already exists, return the user_id
        print(existing_user_id)
        return existing_user_id
    
def validateJoinGroup(input):
    group_id = None
    try:
        # create a cursor
        # open connection
        conn = mysql.connector.connect(**db_creds.db_config)
        cursor = conn.cursor()

        # Check if the login already exists in the user_information table
        check_query = "SELECT group_id FROM group_information WHERE invite_code = %s AND group_password = %s"
        cursor.execute(check_query, (input["invite_code"], hash(input["group_password"])))
        group_id = cursor.fetchone()[0]  

        if group_id:
            insert_query = "INSERT INTO user_group (user_id, group_id) VALUES (%s, %s)"
            cursor.execute(insert_query, (input["user_id"], group_id))
            conn.commit()

    finally:
        # close connection
        cursor.close()
        conn.close()

        # If the login already exists, return the user_id
        if group_id:
            return group_id
        else:
            return "Invalid group credentials"

def addUser(input):
    user_id = None
    try:
        print(input)
        # create a cursor
        # open connection
        conn = mysql.connector.connect(**db_creds.db_config)
        cursor = conn.cursor() 
   
        # insert new row
        insert_stmt = (
            "INSERT INTO user_information (first_name, last_name, phone_number, country, email, password_hash, datetime_created)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        cursor.execute(insert_stmt, (
            input["data"]["first_name"],
            input["data"]["last_name"],
            input["data"]["phone_number"],
            input["data"]["country"],
            input["data"]["email"],
            hash_password(input["data"]["password_hash"]),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        # get last id of recently added row
        cursor.execute("SELECT LAST_INSERT_ID()")
        user_id = cursor.fetchone()[0]
        # commit changes
        conn.commit()

    finally:
        # close connection
        cursor.close()
        conn.close()
        return user_id
            
def addGroup(input):
    group_id = None
    try:
        # open connection
        conn = mysql.connector.connect(**db_creds.db_config)
        cursor = conn.cursor()
        # insert new row
        insert_stmt = (
            "INSERT INTO group_information (vacation_title, group_password, vacation_start_datetime, vacation_end_datetime, group_created_datetime, invite_code, active)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        group_created_datetime = datetime.now()
        # start_date = datetime.strptime(input["vacation_start_datetime"], "%Y-%m-%d")
        # end_date = datetime.strptime(input["vacation_end_datetime"], "%Y-%m-%d") + timedelta(days=1, seconds=-1)
        start_date = datetime.now()
        end_date = datetime.now()
        active = 1
        if (group_created_datetime >= start_date and group_created_datetime <= end_date):
            active = 1
        uniqueid = randint(100000, 999999)
        cursor.execute(insert_stmt, (
            input["vacation_title"],
            hash_password(input["group_password"]),
            start_date,
            end_date,
            group_created_datetime,
            str(uniqueid),  # generate group invitation code
            active
        ))

        conn.commit()

        # get last id of recently added row
        cursor.execute("SELECT LAST_INSERT_ID()")
        group_id = cursor.fetchone()[0]

        # If the group credentials already exists, add a row to user_group table
        if group_id:
            # Assuming user_group table has columns user_id and group_id
            insert_user_group_query = "INSERT INTO user_group (user_id, group_id) VALUES (%s, %s)"
            cursor.execute(insert_user_group_query, (input["user_id"], input["group_id"]))
            # commit changes
            conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # close connection and cursor
        cursor.close()
        conn.close()
        return group_id

def addCreditCard(input):
    try:
        # open connection
        conn = mysql.connector.connect(**db_creds.db_config)
        cursor = conn.cursor()

        # insert new row
        insert_stmt = (
            "INSERT INTO credit_cards (credit_card_number, credit_card_name, user_id, date_added) "
            "VALUES (%s, %s, %s, %s)"
        )
        cursor.execute(insert_stmt, (
            input["credit_card_number"],
            input["credit_card_name"],
            input["user_id"],
            datetime.now()
        ))

        # commit changes
        conn.commit()

    finally:
        # close connection and cursor
        cursor.close()
        conn.close()
        return 1 # to indicate success

def updateGroupTransactions(input):
    user_ids = []
    user_names = []
    start_date = None
    end_date = None
    output = {}
    try:
        # create a cursor
        # open connection
        conn = mysql.connector.connect(**db_creds.db_config)
        cursor = conn.cursor()

        # SQL query to get user information from user_group table
        query_user_info = "SELECT user_id FROM user_group WHERE group_id = %s"
        cursor.execute(query_user_info % (input["group_id"]))
        output_user_ids = cursor.fetchall()
        for item in output_user_ids:
            user_ids.append(item[0])
        query_user_info = "SELECT vacation_start_datetime, vacation_end_datetime FROM group_information WHERE group_id = %s"
        cursor.execute(query_user_info % (input["group_id"]))
        start_date, end_date = cursor.fetchone()
        for user_id in enumerate(user_ids):
            output[user_id] = plaid_connect.get_transactions_user(id, start_date, end_date)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # close connection
        cursor.close()
        conn.close()
        return output

def getGroupDetails(group_id):
    print(group_id)
    output = {}
    try:
        # create a cursor
        # open connection
        conn = mysql.connector.connect(**db_creds.db_config)
        cursor = conn.cursor()

        # SQL query to get all columns from the row with group_id = input["group_id"]
        query = "SELECT * FROM group_information WHERE group_id = %s"

        cursor.execute(query % (group_id))

        # Fetch the first row, if any
        result = cursor.fetchone()

        # Check if a row was found
        if result:
            # Assuming your_table_name has column names
            column_names = [desc[0] for desc in cursor.description]

            # Map the column names to the corresponding values and add to output dictionary
            output = dict(zip(column_names, result))


            # Fetch user_ids associated with the given group_id from user_group table
            query_user_group = "SELECT user_id FROM user_group WHERE group_id = %s"
            cursor.execute(query_user_group % (group_id))
            user_ids_result = cursor.fetchall()
            # print(user_ids_result)
            # Extract user_ids and add to the output dictionary
            user_ids = [user_id[0] for user_id in user_ids_result]
            output["user_ids"] = user_ids
            # print("User IDs:", user_ids)

            # Fetch transactions for each user_id
            transactions = []
            for user_id in user_ids:
                query_transactions = "SELECT * FROM transactions WHERE user_id = %s"
                cursor.execute(query_transactions, (user_id,))
                transactions_result = cursor.fetchall()

                # Assuming transactions table has column names
                column_names_transactions = [desc[0] for desc in cursor.description]
                for transaction in transactions_result:
                    transaction_dict = dict(zip(column_names_transactions, transaction))
                    transactions.append(transaction_dict)

            # Add transactions to the output dictionary
            output["transactions"] = transactions

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # close connection
        cursor.close()
        conn.close()
        return output

def getUserDetails(user_id):
    output = {}
    try:
        # create a cursor
        # open connection
        conn = mysql.connector.connect(**db_creds.db_config)
        cursor = conn.cursor()

        # SQL query to get user information from user_information table
        query_user_info = "SELECT first_name, last_name, phone_number, email, country FROM user_information WHERE user_id = %s"
        cursor.execute(query_user_info % (user_id))
        user_info_result = cursor.fetchone()

        # Check if a user was found
        if user_info_result:
            # Assuming user_information table has column names
            column_names_user_info = [desc[0] for desc in cursor.description]

            # Map the column names to the corresponding values and add to output dictionary
            output.update(dict(zip(column_names_user_info, user_info_result)))

            # Fetch group_ids associated with the given user_id from user_group table
            query_user_groups = "SELECT group_id FROM user_group WHERE user_id = %s"
            cursor.execute(query_user_groups % (user_id))
            user_groups_result = cursor.fetchall()

            # Extract group_ids and add to the output dictionary
            group_ids = [group_id[0] for group_id in user_groups_result]
            output["group_ids"] = group_ids

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # close connection
        cursor.close()
        conn.close()
        print(output)
        return output


    # function calls function called get_transactions_user() returns user_id, start_date, end_date

def getGroupSummary(group_id):
    data = getGroupDetails(group_id)
    print(data["user_ids"])
    # Process the data to create a new representation
    init_json = {}
    init_json['table'] = []

    # Create a dictionary to store total_amount_paid and total_amount_owed for each user_id
    user_totals = {}

    # Iterate through transactions
    for transaction in data['transactions']:
        user_id = transaction['user_id']
        amount = float(transaction['amount'])

        # Initialize user_totals if not exists
        if user_id not in user_totals:
            user_totals[user_id] = {'total_amount_paid': 0, 'total_amount_owed': 0}

        # Update total_amount_paid for the user
        user_totals[user_id]['total_amount_paid'] += amount

    # Iterate through user_ids to calculate total_amount_owed
    for user_id in data['user_ids']:
        if user_id in user_totals:
            # Calculate total_amount_owed as the total amount paid by others
            user_totals[user_id]['total_amount_owed'] = sum(
                user_totals[other_user]['total_amount_paid']
                for other_user in data['user_ids']
                if other_user != user_id
            )

    # Create rows for the result JSON
    for user_id, totals in user_totals.items():
        init_json['table'].append({
            'user_id': user_id,
            'total_amount_paid': totals['total_amount_paid']
            # 'total_amount_owed': totals['total_amount_owed']
        })
    # Calculate the average amount paid per user
    total_users = len(init_json["table"])
    total_amount = sum(user["total_amount_paid"] for user in init_json["table"])
    average_amount = total_amount / total_users

    # Find users who need to pay and users who need to receive
    payers = sorted(
        [user for user in init_json["table"] if user["total_amount_paid"] > average_amount],
        key=lambda x: x["total_amount_paid"],
        reverse=True,
    )
    recipients = sorted(
        [user for user in init_json["table"] if user["total_amount_paid"] < average_amount],
        key=lambda x: x["total_amount_paid"],
    )

    # Create transactions to balance amounts
    transactions = []
    for payer in payers:
        amount_to_receive = payer["total_amount_paid"] - average_amount
        for recipient in recipients:
            amount_to_pay = average_amount - recipient["total_amount_paid"]
            transfer_amount = min(amount_to_receive, amount_to_pay)
            if transfer_amount > 0:
                transactions.append(
                    {
                        "payer": payer["user_id"],
                        "recipient": recipient["user_id"],
                        "amount": round(transfer_amount, 2),
                    }
                )
                amount_to_receive -= transfer_amount
                amount_to_pay -= transfer_amount

    print(init_json)
    print()
    print(transactions)
    swapped_json = {
    "transactions": [
        {"payer": transaction["recipient"], "recipient": transaction["payer"], "amount": transaction["amount"]}
        for transaction in transactions
        ]
    }
    print(swapped_json)

    
getGroupSummary(4)

# input_yuh = {
#   "vacation_title": "Summer Trip",
#   "group_password": "my_secure_password",
#   "vacation_start_datetime": "2023-06-01",
#   "vacation_end_datetime": "2023-06-10"
# }

# print(addGroup(input_yuh))