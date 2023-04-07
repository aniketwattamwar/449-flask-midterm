from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename 
import pymysql
import re
from flask_cors import CORS
import os
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


UPLOAD_FOLDER = 'C:/Users/aniket.wattamwar/Documents/RA/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# ALLOWED_FILESIZES = {}



conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "adminadmin",
        db='449_db',
		cursorclass=pymysql.cursors.DictCursor
        )
cur = conn.cursor()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "aniket" or password != "aniket":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
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
    # size = os.stat(fs).st_size
    # print(size)
    if fs and allowed_file(fs.filename):
        filename = secure_filename(fs.filename)
        print(filename)
        
        fs.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "file saved"
        
    return "File saved and uploaded"



if __name__ == "__main__":
    
    app.run(debug=True)