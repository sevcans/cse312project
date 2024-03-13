from flask import Flask
from flask import render_template
from flask import Response, make_response, request, send_from_directory, redirect
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
#Generate a Cookie
def Cookiegen(x):
    string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars=""
    for i in range(x):
        chars += (random.choice(string))
    return chars

#when / is url returns index.html contents as home page and also calls on css/js files
@app.route("/", methods=['GET'])
def home():
    if request.args.get('LoginMessage'):
        return render_template('index.html', LoginMessage = request.args.get('LoginMessage'))
    elif request.args.get('RegisterMessage'):
        return render_template('index.html', RegisterMessage = request.args.get('RegisterMessage'))
    elif request.args.get('LogOutMessage'):
        return render_template('index.html',LogOutMessage = request.args.get('LogOutMessage')) 
    else:
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
    username = request.form['email_reg']
    pw = request.form['password_reg']
    pw_retype = request.form['password_reg_retype']
    #Check for Miss match password
    if pw != pw_retype:
        return redirect(f'/?RegisterMessage={"Password Miss Match"}')
    #Check if username already in use
    if userdata.find_one({"username": username}):
        return redirect(f'/?RegisterMessage={"Username already in use"}')
    #Generate user info
    salt = Saltgen(16)
    hashpass = hashlib.sha256((pw+salt).encode('utf-8')).hexdigest()
    user_info = {"username" : username, "password": hashpass,"salt": salt, "auth_token": ''}
    #Insert in DB
    userdata.insert_one(user_info)
    return redirect(f'/?RegisterMessage={"Registration Successful"}')

#Login
@app.route("/login", methods=['POST'])
def login():
    #Get the credentials from form
    username = request.form['username_login']
    pw = request.form['password_login']
    #Search database
    if userdata.find_one({"username": username}):
       #Get the credentials from Database
       authpass = userdata.find_one({"username": username})['password']
       salt = userdata.find_one({"username": username})['salt']
       #Generate new token
       token = Cookiegen(50)
       hashpass = hashlib.sha256((pw+salt).encode('utf-8')).hexdigest()
       auth = hashlib.sha256((token).encode('utf-8')).hexdigest()
       #Check PW
       if authpass == hashpass:
        #Update auth token
        userdata.update_one({"username": username},{"$set": {"auth_token": auth}})
        response = make_response(redirect('/battle'))
        response.set_cookie('auth', token, httponly=True, max_age=7200)
        return response
       else:
           return redirect(f'/?LoginMessage={"Password or Username Incorrect"}')
    else:
        return redirect(f'/?LoginMessage={"Password or Username Incorrect"}')

#LogOut
@app.route("/logout", methods=['POST'])
def Logout():
    if 'auth' not in request.cookies:
        return redirect('/')
    else:
        response = redirect(f'/?LogOutMessage={"Logged Out Successful"}')
        response.set_cookie('auth', '', expires=0)
        return response
  
@app.route("/battle/logout", methods=['POST'])
def BattleLogOUt():
    response = redirect(f'/?LogOutMessage={"Logged Out Successful"}')
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
    app.run(host ='0.0.0.0', port=8080)
