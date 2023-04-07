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

#cur.execute("CREATE TABLE `449_db`.`users`(`id` INT NOT NULL, `username` VARCHAR(100) NULL, `password` VARCHAR(20) NULL, `email` VARCHAR(45) NULL, `organisation` VARCHAR(100) NULL, `address` VARCHAR(100) NULL, PRIMARY KEY (`id`)")        

@app.route('/login', methods = ['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods = ['GET','POST'])
def register():
    msg = ''
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        organisation = request.form["organisation"]
        address = request.form["address"]
        cur.execute('SELECT * FROM users WHERE username = % s', (username, ))
        record = cur.fetchone()
        if record:
            msg = 'already registered'
        else:
            cur.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s)', (username, password, email, organisation, address,))
            conn.commit()
            msg = 'successfull registration'
    return render_template('register.html')

@app.route('/update', methods = ['GET','POST'])
def update():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
                username = request.form['username']
                password = request.form['password']
                email = request.form['email']
                organisation = request.form['organisation']
                address = request.form['address']
                cur.execute('SELECT * FROM users WHERE username = % s', (username, ))
                record = cur.fetchone()
                if record:
                    msg = 'Record already exists!'
                else:
                    cur.execute("UPDATE users SET username = %s, password = %s, email = %s, organisation = %s, address = %s WHERE username = % s", (username, password, email, organisation, address))
                    conn.commit()
                    msg = 'updated'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('update.html')

#cur.execute("CREATE TABLE `449_db`.`users`(`id` INT NOT NULL, `username` VARCHAR(100) NULL, `password` VARCHAR(20) NULL, `email` VARCHAR(45) NULL, `organisation` VARCHAR(100) NULL, `address` VARCHAR(100) NULL, PRIMARY KEY (`id`)")        

@app.route('/login', methods = ['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods = ['GET','POST'])
def register():
    msg = ''
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        organisation = request.form["organisation"]
        address = request.form["address"]
        cur.execute('SELECT * FROM users WHERE username = % s', (username, ))
        record = cur.fetchone()
        if record:
            msg = 'already registered'
        else:
            cur.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s)', (username, password, email, organisation, address,))
            conn.commit()
            msg = 'successfull registration'
    return render_template('register.html')

@app.route('/update', methods = ['GET','POST'])
def update():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
                username = request.form['username']
                password = request.form['password']
                email = request.form['email']
                organisation = request.form['organisation']
                address = request.form['address']
                cur.execute('SELECT * FROM users WHERE username = % s', (username, ))
                record = cur.fetchone()
                if record:
                    msg = 'Record already exists!'
                else:
                    cur.execute("UPDATE users SET username = %s, password = %s, email = %s, organisation = %s, address = %s WHERE username = % s", (username, password, email, organisation, address))
                    conn.commit()
                    msg = 'updated'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('update.html')

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