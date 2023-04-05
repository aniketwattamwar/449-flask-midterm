from flask import Flask, request
import pymysql
import re
from flask_cors import CORS
import os
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "root",
        db='449_db',
		cursorclass=pymysql.cursors.DictCursor
        )
cur = conn.cursor()


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