import mysql.connector
import db_creds
from datetime import datetime
from flask import Flask, jsonify, request
import hashlib
import uuid
from datetime import timedelta
from random import randint

def getGroupDetails(input):
    output = {}
    try:
        # create a cursor
        # open connection
        conn = mysql.connector.connect(**db_creds.db_config)
        cursor = conn.cursor()

        # SQL query to get all columns from the row with group_id = input["group_id"]
        query = "SELECT * FROM group_information WHERE group_id = %s"

        cursor.execute(query % (input['group_id']))

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
            cursor.execute(query_user_group, (input['group_id'],))
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

def getUserDetails(input):
    output = {}
    try:
        # create a cursor
        # open connection
        conn = mysql.connector.connect(**db_creds.db_config)
        cursor = conn.cursor()

        # SQL query to get user information from user_information table
        query_user_info = "SELECT first_name, last_name, phone_number, email, country FROM user_information WHERE user_id = %s"
        cursor.execute(query_user_info % (input["user_id"]))
        user_info_result = cursor.fetchone()

        # Check if a user was found
        if user_info_result:
            # Assuming user_information table has column names
            column_names_user_info = [desc[0] for desc in cursor.description]

            # Map the column names to the corresponding values and add to output dictionary
            output.update(dict(zip(column_names_user_info, user_info_result)))

            # Fetch group_ids associated with the given user_id from user_group table
            query_user_groups = "SELECT group_id FROM user_group WHERE user_id = %s"
            cursor.execute(query_user_groups, (input["user_id"],))
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
        return output

def updateGroupTransactions(input):
    user_ids = []
    start_date = None
    end_date = None
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

        bansh_data = get_transactions_usere(user_ids, start_date, end_date)
 
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # close connection
        cursor.close()
        conn.close()
        return 0


def get_transactions_usere(user_id, start_date, end_date):
    return "woohoo"

    # function calls function called get_transactions_user() returns user_id, start_date, end_date

data_json = {
    "group_id": 4
}
print(updateGroupTransactions(data_json))
