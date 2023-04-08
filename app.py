from flask import Flask, request, jsonify
import json
from werkzeug.utils import secure_filename 
import pymysql
import re
from flask_cors import CORS
import os
import jwt
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})



UPLOAD_FOLDER = 'C:/Users/aniket.wattamwar/Documents/RA/'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png'}
ALLOWED_FILESIZE = 5000000
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
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


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

    if fs and allowed_file(fs.filename):
        filename = secure_filename(fs.filename)
        fs.seek(0,2)
        file_length = fs.tell()
        print(file_length)
        if file_length < ALLOWED_FILESIZE:
            fs.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "file saved since within the limit"
        else:
            return "too large file. Upload a smaller file."
        
    return "File saved and uploaded"

@app.route('/public',methods=["POST","GET"])
def public():
    cur=conn.cursor()
    cur.execute("SELECT * FROM students")
    details = cur.fetchall()
    return details

def encode_token(username):
    return jwt.encode({"username":username},app.config['SECRET_KEY'],'HS256')

def decode_token(jwt_token):
    return jsonify(jwt.decode(jwt_token,app.config['SECRET_KEY'],algorithms=["HS256"])),200
   

if __name__ == "__main__":
    app.run(debug=True)