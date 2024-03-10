from flask import Flask
from flask import render_template
from flask import Response, make_response, request, send_from_directory
from pymongo import MongoClient
import random
import hashlib
import urllib.parse

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

#Register for an account
@app.route("/register", methods=['POST'])
def register():
    #Get the credentials
    username = request.form['email_reg']
    pw = request.form['password_reg']
    pw_retype = request.form['password_reg_retype']
    #Check for Miss match password
    if pw != pw_retype:
        return render_template('index.html', RegisterMessage="Password Miss Match")
    #Check if username already in use
    if userdata.find_one({"username": username}):
        return render_template('index.html', RegisterMessage="Username already in use")
    #Generate user info
    salt = Saltgen(16)
    hashpass = hashlib.sha256((pw+salt).encode('utf-8')).hexdigest()
    token = hashlib.sha256((username + salt).encode('utf-8')).hexdigest()
    user_info = {"username" : username, "password": hashpass,"salt":salt, "aut_token": token}
    #Insert in DB
    userdata.insert_one(user_info)
    return render_template('index.html', RegisterMessage="Registration Successful")

#Login
@app.route("/login", methods=['POST'])
def login():
    #Get the credentials
    username = request.form['username_login']
    pw = request.form['password_login']
    #Search database
    if userdata.find_one({"username": username}):
       authpass = userdata.find_one({"username": username})['password']
       salt = userdata.find_one({"username": username})['salt']
       token = userdata.find_one({"username": username})['aut_token']
       hashpass = hashlib.sha256((pw+salt).encode('utf-8')).hexdigest()
       if authpass == hashpass:
        response = make_response(render_template('index.html', LoginMessage="Login Successful"))
        response.set_cookie('auth', str(token), httponly=True, max_age=7200)
        return response
       else:
           return render_template('index.html', LoginMessage="Password or Username Incorrect")
    else:
        return render_template('index.html', LoginMessage="Password or Username Incorrect")

#LogOut
@app.route("/logout", methods=['POST'])
def Logout():
    response = make_response(render_template('index.html', LogOutMessage="Logged Out"))
    response.set_cookie('auth', '', expires=0)
    return response

# add no sniff after
@app.after_request
def add_nosniff(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'    
    return response
@app.route("/<path:folder>/<path:file>", methods=['GET'])
def style(folder, file):
    return send_from_directory(folder, file)


   
if __name__ =='__main__':
    app.run(host ='0.0.0.0', port=8080)
