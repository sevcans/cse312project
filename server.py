from flask import Flask
from flask import render_template
from flask import Response, make_response, request, send_from_directory

app = Flask(__name__)


#when / is url returns index.html contents as home page and also calls on css/js files
@app.route("/", methods=['GET'])
def home():
    
    return render_template('index.html')    

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
