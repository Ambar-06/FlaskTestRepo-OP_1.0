from flask import Flask, jsonify, request, current_app
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from pydantic import ValidationError
from dotenv import load_dotenv

import traceback

import jwt
import hashlib
import datetime
from datetime import timedelta

from db.queries import *
from db.schema import *

load_dotenv() 

JWT_SECRETS = os.environ.get('JWT_SECRETS')

app = Flask(__name__)
app.config['SECRET_KEY'] = JWT_SECRETS
jwt = JWTManager(app)


users = {
    os.environ.get('TOKEN_EMAIL'): os.environ.get('TOKEN_SECRET')
}

@app.route('/generateToken', methods=['POST'])
def generateToken_f():
    request_data = request.get_json()

    try:
        validated_data = user_login_token_schema(**request_data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
        
    Email = validated_data.Email
    TokenKey = validated_data.Key

    if Email in users and users[Email] == TokenKey:
        access_token = create_access_token(identity=Email)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
@app.route('/generate_long_lived_token', methods=['POST'])
def generate_long_lived_token():
    request_data = request.get_json()
    try:
        validated_data = long_live_access_token_schema(**request_data)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400
    
    Token = validated_data.access_token

    expiration = datetime.datetime.utcnow() + timedelta(days=365) 
    access_token = create_access_token(identity=Token, expires_delta=expiration - datetime.datetime.utcnow())
    
    return jsonify({'access_token': access_token}), 200


@app.route("/AddUser", methods=['POST'])
@jwt_required()
def AddUser_f():
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
        if not token:
            json_data = {
                'status_code': 401,
                "message": "Authentication Token is missing!",
                "data": '',
                "error": "Unauthorized"
            }
            return jsonify(json_data), 401
    else:
        json_data = {
            'status_code': 401,
            "message": "Authentication Token is missing!",
            "data": '',
            "error": "Unauthorized"
        }
        return jsonify(json_data), 401
    try:
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({'error': 'Invalid token'}), 401
        request_data = request.get_json()

        try:
            validated_data = user_info_add_schema(**request_data)
        except ValidationError as e:
            return jsonify({'error': e.errors()}), 400
        
        UserName = validated_data.UserName if validated_data.UserName else ''
        FirstName = validated_data.FirstName
        LastName = validated_data.LastName
        Password = validated_data.Password
        Email = validated_data.Email
        Mobile = validated_data.Mobile
        Source = validated_data.Source if validated_data.Source else ''
        Device = validated_data.Device if validated_data.Device else ''

        password_encoded = Password.encode() 

        password_hashed = hashlib.md5(password_encoded).hexdigest()
        
        data = {
            "UserName" : UserName,
            "FirstName" : FirstName,
            "LastName" : LastName,
            "Password" : password_hashed, 
            "Email" : Email,
            "Mobile" : Mobile,
            "Source" : Source,
            "Device" : Device,
            "IsDeleted" : "0",
            "CreatedAt" : datetime.datetime.now(),
            "CreatedBy" : "system",
            "UpdatedAt" : datetime.datetime.now(),
            "UpdatedBy" : "system"
        }
        values_tuple = tuple(data.values())
        resp = addUser_q(values_tuple)
        print(resp)

        if 1:
            json_data = {
                'status_code': 200,
                'status': 'Success',
                'data': '',
                'message': 'Data Saved Successfully',
            }
            return jsonify(json_data), 200
        else:
            json_data = {
                'status_code': 400,
                'status': 'Error',
                'data': '',
                'message': 'Invalid Data or Error in Processing',
            }
            return jsonify(json_data), 400
    except Exception as e:
        print("Error --------:", e)
        traceback.print_exc()
        json_data = {
            'status_code': 400,
            'status': 'Fail',
            'data': e,
            'message': 'landed in exception',
        }
        return jsonify(json_data), 400

@app.route("/UpdateUser", methods=['POST'])
@jwt_required()
def UpdateUser_f():
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
        if not token:
            json_data = {
                'status_code': 401,
                "message": "Authentication Token is missing!",
                "data": '',
                "error": "Unauthorized"
            }
            return jsonify(json_data), 401
    else:
        json_data = {
            'status_code': 401,
            "message": "Authentication Token is missing!",
            "data": '',
            "error": "Unauthorized"
        }
        return jsonify(json_data), 401
    try:
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({'error': 'Invalid token'}), 401
        request_data = request.get_json()

        try:
            validated_data = user_info_update_schema(**request_data)
        except ValidationError as e:
            return jsonify({'error': e.errors()}), 400
        
        UserToken = validated_data.UserToken
        UserData = get_user_q(UserToken)
        UserId = UserData['UserId']
        UserName = validated_data.UserName if validated_data.UserName else UserData.get('UserName')
        FirstName = validated_data.FirstName if validated_data.FirstName != None else UserData.get('FirstName')
        LastName = validated_data.LastName if validated_data.LastName else UserData.get('LastName')
        Email = validated_data.Email if validated_data.Email else UserData.get('Email')
        Mobile = validated_data.Mobile if validated_data.Mobile else UserData.get('Mobile')
        Source = validated_data.Source if validated_data.Source else UserData.get('Source')
        Device = validated_data.Device if validated_data.Device else UserData.get('Device')
        
        data = {
            "UserName" : UserName,
            "FirstName" : FirstName,
            "LastName" : LastName,
            "Email" : Email,
            "Mobile" : Mobile,
            "Source" : Source,
            "Device" : Device,
            "IsDeleted" : "0",
            "CreatedAt" : datetime.datetime.now(),
            "CreatedBy" : "system",
            "UpdatedAt" : datetime.datetime.now(),
            "UpdatedBy" : "system",
            "UserId" : UserId
        }
        values_tuple = tuple(data.values())
        resp = updateUser_q(values_tuple)
        print(resp)

        if 1:
            json_data = {
                'status_code': 200,
                'status': 'Success',
                'data': '',
                'message': 'Data Updated Successfully',
            }
            return jsonify(json_data), 200
        else:
            json_data = {
                'status_code': 400,
                'status': 'Error',
                'data': '',
                'message': 'Invalid Data or Error in Processing',
            }
            return jsonify(json_data), 400
    except Exception as e:
        print("Error --------:", e)
        traceback.print_exc()
        json_data = {
            'status_code': 400,
            'status': 'Fail',
            'data': e,
            'message': 'landed in exception',
        }
        return jsonify(json_data), 400
    

@app.route("/GetUsers", methods=['POST'])
@jwt_required()
def GetUsers_f():
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
        if not token:
            json_data = {
                'status_code': 401,
                "message": "Authentication Token is missing!",
                "data": '',
                "error": "Unauthorized"
            }
            return jsonify(json_data), 401
    else:
        json_data = {
            'status_code': 401,
            "message": "Authentication Token is missing!",
            "data": '',
            "error": "Unauthorized"
        }
        return jsonify(json_data), 401
    
    try:
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({'error': 'Invalid token'}), 401
        usersData = getUsers_q()
        
        if usersData:
            json_data = {
                'status_code': 200,
                'status': 'Success',
                'data': usersData,
                'message': 'Data Found Successfully',
            }
            return jsonify(json_data), 200
        else:
            json_data = {
                'status_code': 200,
                'status': 'Fail',
                'data': '',
                'message': 'No Data Found.',
            }
            return jsonify(json_data), 200
    except Exception as e:
        print("Error --------:", e)
        traceback.print_exc()
        json_data = {
            'status_code': 400,
            'status': 'Fail',
            'data': e,
            'message': 'landed in exception',
        }
        return jsonify(json_data), 400
    

@app.route("/me", methods=['POST'])
@jwt_required()
def GetCurrentUser_f():
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
        if not token:
            json_data = {
                'status_code': 401,
                "message": "Authentication Token is missing!",
                "data": '',
                "error": "Unauthorized"
            }
            return jsonify(json_data), 401
    else:
        json_data = {
            'status_code': 401,
            "message": "Authentication Token is missing!",
            "data": '',
            "error": "Unauthorized"
        }
        return jsonify(json_data), 401
    try:
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({'error': 'Invalid token'}), 401
        request_data = request.get_json()

        try:
            validated_data = current_user_info_schema(**request_data)
        except ValidationError as e:
            return jsonify({'error': e.errors()}), 400
        
        UserToken = validated_data.UserToken

        UserData = get_user_q(UserToken)
        print(UserData, '*-*-*-*-*-*-*-*-*')
        UserId = UserData['UserId']
        if UserData:
            json_data = {
                'status_code': 200,
                'status': 'Success',
                'data': UserData,
                'message': 'Data Found Successfully',
            }
            return jsonify(json_data), 200
        else:
            json_data = {
                'status_code': 200,
                'status': 'Fail',
                'data': '',
                'message': 'No Data Found.',
            }
            return jsonify(json_data), 400
    except Exception as e:
        print("Error --------:", e)
        traceback.print_exc()
        json_data = {
            'status_code': 400,
            'status': 'Fail',
            'data': e,
            'message': 'landed in exception',
        }
        return jsonify(json_data), 400
    

if __name__ == "__main__":
    app.run(debug=True)