from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename 
import pymysql
import re
from flask_cors import CORS
import os
import jwt
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})


UPLOAD_FOLDER = 'C:/Users/Sanket/MS Subject/449 Backend/449-flask-midterm'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# ALLOWED_FILESIZES = {}



conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "root",
        db='449_db',
		cursorclass=pymysql.cursors.DictCursor
        )
cur = conn.cursor()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super-secret'

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "aniket" or password != "aniket":
        return jsonify({"msg": "Bad username or password"}), 401

    #access_token = create_access_token(identity=username)
    access_token = encode_token(username)
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
def protected(): 
    # Access the identity of the current user with get_jwt_identity
    try:
        token=request.headers.get('authorization')
        user=decode_token(token)
        return user
    except:
        return jsonify({"err":"DECODE ERROR"}),  401



@app.route('/')  
def home():
    return "This is the homepage"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload' , methods =['GET', 'POST'])
def upload():
    
    fs = request.files['myFile']
    print(fs.filename)
    # size = os.stat(fs).st_size
    # print(size)
    if fs and allowed_file(fs.filename):
        filename = secure_filename(fs.filename)
        print(filename)
        
        fs.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "file saved"
        
    return "File saved and uploaded"

def encode_token(username):
    return jwt.encode({"username":username},app.config['SECRET_KEY'],'HS256')

def decode_token(jwt_token):
    return jsonify(jwt.decode(jwt_token,app.config['SECRET_KEY'],algorithms=["HS256"])),200
   

if __name__ == "__main__":
    app.run(debug=True)