from flask import Flask, request, render_template
import pymysql
import re
from flask_cors import CORS
import os
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

conn = pymysql.connect(
        host='localhost',
        user='root',
        #Use your own pasword when connecting to the database 
        password = "Soham@12345",
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

@app.route('/')  
def home():
    return "This is the homepage"

@app.route('/upload' , methods =['GET', 'POST'])
def upload():
    
    fs = request.files.get('myFile')
    print(fs.filename)

    return "File Uploaded"



if __name__ == "__main__":
    
    app.run(debug=True)