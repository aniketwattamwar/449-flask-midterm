from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename 
import pymysql
import re
import json
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
        password = "Soham@12345",
        db='449_db',
		cursorclass=pymysql.cursors.DictCursor
        )
cur = conn.cursor()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWTManager(app)

# @app.errorhandler(HTTPException)
# def handle_exception(e):
#     """Return JSON instead of HTML for HTTP errors."""
#     # start with the correct headers and status code from the error
#     response = e.get_response()
#     # replace the body with JSON
#     response.data = json.dumps({
#         "code": e.code,
#         "name": e.name,
#         "description": e.description,
#     })
#     response.content_type = "application/json"
#     return response


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username and password:
        cur.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password))
        conn.commit()
        account = cur.fetchone()
        if account:
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)
        else:
            return jsonify({'error': 'Unauthorized access'}), 401
    else:
        return jsonify({'error': 'Bad request'}), 400
    

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


@app.errorhandler(400)
def handle_Error_400(e):
    return jsonify({'error': str(e)}), 400

@app.errorhandler(404)
def handle_Error_404(e):
    return jsonify({'error': str(e)}), 404


@app.errorhandler(401)
def handle_Error_401(e):
    return jsonify({'error': str(e)}), 401


if __name__ == "__main__":
    
    app.run(debug=True)