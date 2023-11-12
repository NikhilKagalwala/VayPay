import mysql.connector
import db_creds
from datetime import datetime
from flask import Flask, jsonify, request
import hashlib
import uuid
from datetime import timedelta
from random import randint

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
            hash(input["data"]["password_hash"]),
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
  
def validateLogin(input):
    existing_user_id = None
    try:
        # create a cursor
        # open connection
        conn = mysql.connector.connect(**db_creds.db_config)
        cursor = conn.cursor()

        # Check if the login already exists in the user_information table
        check_query = "SELECT user_id FROM user_information WHERE email = %s AND password_hash = %s"
        cursor.execute(check_query, (input["email"], hash(input["password_hash"])))
        existing_user_id = cursor.fetchone()[0] 

        # add checks for 
            # newly active vacations
            # ended vacation

    finally:
        # close connection
        cursor.close()
        conn.close()
        # If the login already exists, return the user_id
        return existing_user_id
            
def addGroup(input):
    group_id = None
    try:
        # open connection
        conn = mysql.connector.connect(**db_creds.db_config)
        cursor = conn.cursor()

        # insert new row
        insert_stmt = (
            "INSERT INTO group_information (vacation_title, group_password, vacation_start_datetime, vacation_end_datetime, group_created_datetime, invite_code, active, user_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        )
        group_created_datetime = datetime.now()
        start_date = datetime.strptime(input["vacation_start_datetime"], "%Y-%m-%d")
        end_date = datetime.strptime(input["vacation_end_datetime"], "%Y-%m-%d") + timedelta(days=1, seconds=-1)
        active = 1
        if (group_created_datetime >= start_date and group_created_datetime <= end_date):
            active = 1
        uniqueid = randint(100000, 999999)
        cursor.execute(insert_stmt, (
            input["vacation_title"],
            hash(input["group_password"]),
            start_date,
            end_date,
            group_created_datetime,
            str(uniqueid),  # generate group invitation code
            active
        ))

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
        
        

    finally:
        # close connection
        cursor.close()
        conn.close()

        # If the login already exists, return the user_id
        if group_id:
            return group_id
        else:
            return "Invalid group credentials"

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


