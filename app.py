from flask import Flask, jsonify, request, abort
import mysql.connector
from flask_cors import CORS
from mysql.connector import (connection)
app = Flask(__name__)
CORS(app)
db_config = {
    "host": "",
    "user": "",
    "password": "!23",
    "database": "",
}

def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/getWalkers')
def getWalkers():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = ("select name from pet_walkers")
    cursor.execute(query)
    names_list = []
    # response = cursor.fetchall
    for row in cursor:
        row = str(row)
        name = row.strip("('')").split(',')[0].split("'")[0]
        names_list.append(name)
    print(names_list[0])
    return names_list

@app.route('/', methods=["GET"])
def helloWorld():
    return "Hello World"


@app.route('/login', methods=["POST"])
# request must have body similar to {"username": "basel", "password": "password123", "account-type":"walker"}
# Request must have headers Content-Type : application/json
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    account_type = data.get("account-type")
    if(username == '' or password == '' or account_type == ''):
        abort(400,"Values are empty")
    cnx = get_db_connection()
    cursor = cnx.cursor()
    if(account_type == "walker"):
        query = (f" select * from pet_walkers where name = '{username}' and password = '{password}'")
    elif (account_type == "pet"):
        query = (f" select * from pets where name = '{username}' and password = '{password}'")
    elif(account_type not in ["walker", "pet"]):
        abort(400, "account type is not valid")
                 
    cursor.execute(query)
    rows = 0
    user_id = 0
    owner_name = ''
    owner_email = ''
    owner_phone_number = 0
    pet_name = ''
    for row in cursor:
        rows += 1
        user_id = row[0]
        if (account_type == "pet"):
            owner_name = row[1]
            owner_email = row[2]
            owner_phone_number = row[3]
            pet_name = row[5]

        if username in str(row):
            print("Account found, Login")
            response_data = {
                'status': 'Success',
                'message': 'Account Found',
                'properties': {
                    'user-id': user_id,
                    'owner_name': owner_name,
                    'owner_email': owner_email,
                    'owner_phone_number': owner_phone_number,
                    'pet_name': pet_name
                    }
                }
            return jsonify(response_data), 200


    if (rows == 0 ):
        return jsonify({'status': 'Failure', 'message':'Invalid username, password or account type'}), 200

@app.route('/addEvent', methods=["POST"])
# Built in away just need to parse through  ==> bookingFormData
def addEvent():
    print("hello world")
    data = request.get_json()
    cnx = get_db_connection()
    cursor = cnx.cursor()
    petName = data.get("petName")
    ownerName = data.get("ownerName")
    print("hello world 2")
    query = (f"Select ID from waqqlyDB.pets \n where name = '{ownerName}' \n and pet_name ='{petName}'")
    cursor.execute(query)
    pet_id = 0
    for ID in cursor:
        pet_id = ID[0]
    print("hello owlrd 3)")
    query = (f"Select id  from pet_walkers where name = '{data.get('walker')}'")
    walker_id = 0
    cursor.execute(query)
    for id in cursor:
        walker_id = id[0]

    print("hello world 3")
    query = f"""INSERT INTO events (owner_name, address, start_date_time, end_date_time, pet_name, owner_email, owner_phone_number, walker_id, pet_id)
    VALUES ('{data.get("ownerName")}', '{data.get("address")}', '{data.get("startTime")}', '{data.get("endTime")}', '{data.get("petName")}', '{data.get("email")}', '{data.get("phoneNumber")}', '{walker_id}', '{pet_id}');
    """

    cursor.execute(query)
    cnx.commit()
    print("hello world 4")
    return {"Code":200, "Message": "Event Added Succesfully"}

    
    

@app.route('/viewEvents', methods=["GET"])
# example request to endpoint http://127.0.0.1:5000/viewEvents?id=1&userType=walker
def getEvents():
    cnx = get_db_connection()
    cursor = cnx.cursor()

    user_id = request.args.get('id')
    user_type = request.args.get('userType')
    query = ''

    if user_type == "walker" :
        query = f"Select * from events where walker_id = {user_id}"

    elif user_type=="pet" :
        query = f"Select * from events where pet_id = {user_id}"

    cursor.execute(query)
    result = []

    for row in cursor:
        event_data = {
        'start_date_time': row[3],
        'end_date_time': row[4],
        'owner_name': row[1],
        'address': row[2],
        'owner_phone_number': row[7],
        'owner_email': row[6]
        }
        result.append(event_data)

    return jsonify(result)

@app.route('/createAccount', methods=["POST"])
def createAccount():
    data = request.get_json()
    accountType = data.get("accountType")
    name = data.get("name")
    email = data.get("email")
    phoneNumber = data.get("phoneNumber")
    password = data.get("password")
    petName = data.get("petName")
    petType = data.get("petType")

    if (accountType == "Walker"):
        query = f"Insert into pet_walkers (name, email, phone_number, password) values('{name}','{email}','{phoneNumber}','{password}')"
    elif(accountType == "Pet"):
        # query = f"Insert into pets (name, owner_email, owner_phone_number, password, pet_name, pet_type_id) values('{name}','{email}','{phoneNumber}','{password}', '{petName}','select id from pet_types where pet_type = '{petType}'')"
        query = f"INSERT INTO pets (name, owner_email, owner_phone_number, password, pet_name, pet_type_id) VALUES ('{name}', '{email}', '{phoneNumber}', '{password}', '{petName}', (SELECT id FROM pet_types WHERE pet_type = '{petType}'))"



    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()

    return {"Response" : 200, "Message": "Account Created"}




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    