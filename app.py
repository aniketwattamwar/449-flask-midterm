from flask import Flask, request, jsonify
import json
from werkzeug.utils import secure_filename 
import pymysql
import re
import json
from flask_cors import CORS
import os
import jwt
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})


UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_FILESIZE = 5000000

#database connection
conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "Soham@12345",
        db='449_db',
		cursorclass=pymysql.cursors.DictCursor
        )
cur = conn.cursor()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super-secret'

#endpoints

@app.route("/login", methods=["POST", "GET"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username and password:
        cur.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password))
        conn.commit()
        account = cur.fetchone()
        if account:
            access_token = encode_token(username)
            return jsonify(access_token=access_token)
        else:
            return jsonify({'error': 'Unauthorized access'}), 401
    else:
        return jsonify({'error': 'Bad request'}), 400
    

@app.route("/protected", methods=["GET"])
def protected(): 
    try:
        token=request.headers.get('authorization')
        if token:
            user=decode_token(token)
            return user
        else:
            return jsonify({'error': 'Bad request'}), 400
    except:
        return jsonify({"error":"UnAuthorized User"}),  401


@app.route('/')  
def home():
    return "This is the homepage"


@app.route('/upload' , methods =['GET', 'POST'])
def upload():
    try:
        token = request.headers.get('authorization')
        user = decode_token(token)
        if user:

            fs = request.files['myFile']

            if fs and allowed_file(fs.filename):
                filename = secure_filename(fs.filename)
                fs.seek(0,2)
                file_length = fs.tell()
                fs.seek(0)
                if file_length < ALLOWED_FILESIZE:
                    fs.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    return "File saved and uploaded"
                else:
                    return jsonify({'error':"too large file. Upload a smaller file."}), 400
            else:
                return jsonify({'error':"File type is not supported"}), 400
        else:
            return jsonify({'error': 'Unauthorized access'}), 401
    except:
        return jsonify({'error': 'Bad request'}), 400

@app.route('/public',methods=["POST","GET"])
def public():
    cur=conn.cursor()
    cur.execute("SELECT * FROM students")
    details = cur.fetchall()
    return details

#functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_token(username):
    return jwt.encode({"username":username},app.config['SECRET_KEY'],'HS256')

def decode_token(jwt_token):
    return jsonify(jwt.decode(jwt_token,app.config['SECRET_KEY'],algorithms=["HS256"])),200

#error_handlers
@app.errorhandler(400)
def handle_Error_400(e):
    return jsonify({'error': str(e)}), 400

# @app.errorhandler(404)
# def handle_Error_404(e):
#     return jsonify({'error': str(e)}), 404


@app.errorhandler(401)
def handle_Error_401(e):
    return jsonify({'error': str(e)}), 401


if __name__ == "__main__":
    app.run(debug=True)