from flask import Flask, jsonify, request
import post_calls
import get_calls

app = Flask(__name__)

# arguments: group_id
# return: {'group_id': 4, 'vacation_title': 'Pooppp', 'group_password': '-3312385852641259372', 'vacation_start_datetime': datetime.datetime(2023, 12, 11, 0, 0), 'vacation_end_datetime': datetime.datetime(2023, 12, 15, 23, 59, 59), 'group_created_datetime': datetime.datetime(2023, 11, 12, 8, 32, 4), 'invite_code': '538547', 'active': 1, 'user_ids': [18, 19], 'transactions': [{'transaction_id': 1, 'transaction_date': datetime.datetime(2023, 11, 12, 0, 0), 'amount': Decimal('43.23'), 'user_id': 18, 'location': 'Your mamas', 'merchant': 'Walmart', 'method': 'In Person', 'credit_card_id': 1}]}
@app.route('/api/getGroupDetails', methods=['GET'])
def get_getGroupDetails():
    data = get_calls.get_getGroupDetails()
    return data

# arguments: user_id
# return: {'first_name': 'Suyash', 'last_name': 'Tewari', 'phone_number': '123456789', 'email': 'st@gmail.com', 'country': 'US', 'group_ids': [3, 4]}
@app.route('/api/getUserDetails', methods=['GET'])
def get_getUserDetails():
    input = request.json
    output = get_calls.getUserDetails(input)
    return output

# arguments: first_name, last_name, phone_number, country, email, password_hash
# return: user_id
@app.route('/api/addUser', methods=['POST'])
def post_addUser():
    input_data = request.json
    output = post_calls.addUser(input_data)
    if output:
        return jsonify(output)
    return jsonify({"error": "Error registering user"}), 400

# arguments: email, password_hash
# return: user_id or "Invalid login credentials"
@app.route('/api/validateLogin', methods=['POST'])
def post_validateLogin():
    input_data = request.json
    output = post_calls.validateLogin(input_data)
    if output:
        return jsonify(output)
    return jsonify({"error": "Invalid login credentials"}), 400

# arguments: vacation_title, group_password, vacation_start_time, vacation_end_time
# return: group_id
@app.route('/api/addGroup', methods=['POST'])
def post_addGroup():  # Rename this function
    input_data = request.json
    print(input_data)
    # return jsonify(0)
    output = post_calls.addGroup(input_data)
    print("done")
    print(output)
    if output:
        return jsonify(output)
    return jsonify({"error": "Error adding group"}), 400

# arguments: credit_card_id, credit_card_number, credit_card_name, user_id
# return: group_id or "Invalid group credentials"
@app.route('/api/validateJoinGroup', methods=['POST'])
def post_validateJoinGroup():  # Rename this function
    input_data = request.json
    output = post_calls.validateJoinGroup(input_data)
    if output:
        return jsonify(output)
    return jsonify({"error": "Invalid group credentials"}), 400


# arguments: credit_card_id, credit_card_number, credit_card_name, user_id
# return: ?
@app.route('/api/addCreditCard', methods=['POST'])
def post_addCreditCard(): 
    input_data = request.json
    output = post_calls.addCreditCard(input_data)
    if (output):
        return jsonify({"message": "Sucessfully added card"})
    return jsonify({"error": "Error adding card"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
