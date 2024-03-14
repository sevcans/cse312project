from flask import Flask
from flask import render_template
from flask import Response, make_response, request, send_from_directory, redirect, jsonify
from pymongo import MongoClient
import random
import hashlib
import urllib.parse
import time

app = Flask(__name__)

#DataBase
client = MongoClient("Server312",27017)
db = client["312Db"]
userdata = db["UserData"]

#Generate a Salt
def Saltgen(x):
    string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars=""
    for i in range(x):
        chars += (random.choice(string))
    return chars

#when / is url returns index.html contents as home page and also calls on css/js files
@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')
 
# Battle Page Rendering
@app.route("/battle", methods=['GET'])
def BattlePage():
    #Checks Cookie and Auth to if user exist
    if 'auth' in request.cookies and userdata.find_one({"auth_token": hashlib.sha256((request.cookies.get('auth')).encode('utf-8')).hexdigest()}):
        return render_template('battle.html', UserName = userdata.find_one({"auth_token": hashlib.sha256((request.cookies.get('auth')).encode('utf-8')).hexdigest()})['username']) 
    else:
        return redirect('/')

#Register for an account
@app.route("/register", methods=['POST'])
def register():
    #Get the credentials
    data = request.get_json()
    username = data.get('username')
    pw = data.get('password')
    pw_retype = data.get('retype')
    #Check for missing credentials
    if username == "" or pw == "" or pw_retype == "":
        return jsonify({'message': 'Credentials Missing'})
    #Check for Miss match password
    if pw != pw_retype:
        return jsonify({'message': 'Password Miss Match'})
    #Check if username already in use
    if userdata.find_one({"username": username}):
        return jsonify({'message': 'Username already in use'})
    #Generate user info
    salt = Saltgen(50)
    hashpass = hashlib.sha256((pw+salt).encode('utf-8')).hexdigest()
    token = hashlib.sha256((salt[15:40]).encode('utf-8')).hexdigest()
    user_info = {"username" : username, "password": hashpass,"salt": salt, "auth_token": token}
    #Insert in DB
    userdata.insert_one(user_info)
    return jsonify({'message': 'Registration successful'})
#Login
@app.route("/login", methods=['POST'])
def login():
    #Get the credentials from form
    data = request.get_json()
    username = data.get('username')
    pw = data.get('password')
    if username == "" or pw == "":
        return jsonify({'message': 'Credentials Missing'})
    #Search database
    if userdata.find_one({"username": username}):
       #Get the credentials from Database
       authpass = userdata.find_one({"username": username})['password']
       salt = userdata.find_one({"username": username})['salt']
       #Generate new token
       hashpass = hashlib.sha256((pw+salt).encode('utf-8')).hexdigest()
       #Check PW
       if authpass == hashpass:
        #Update auth token
        token = userdata.find_one({"username": username, "password":authpass})['salt'][15:40]
        response = make_response(jsonify({'message': 'Login successful'}))
        response.set_cookie('auth', token, httponly=True, max_age=7200)
        return response
       else:
           return jsonify({'message': 'Password or Username Incorrect'})
    else:
        return jsonify({'message': 'Password or Username Incorrect'})

#LogOut
@app.route("/logout", methods=['POST'])
def Logout():
    if 'auth' not in request.cookies:
        return jsonify({'message': 'You Have not Logged In'})
    else:
        response = make_response(jsonify({'message': 'Logged Out Successful'}))
        response.set_cookie('auth', '', expires=0)
        return response

# add n sniff after
@app.after_request
def add_nosniff(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'    
    return response
@app.route("/<path:folder>/<path:file>", methods=['GET'])
def style(folder, file):
    return send_from_directory(folder, file)


   
if __name__ =='__main__':
    app.run(host ='0.0.0.0', port=8080, debug=True)
