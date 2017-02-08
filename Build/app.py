from flask import Flask
from flask import Response
from flask import request
from redis import Redis
from datetime import datetime
import MySQLdb
import sys
import redis 
import time
import hashlib
import os
import json

app = Flask(__name__)
startTime = datetime.now()
R_SERVER = redis.Redis(host=os.environ.get('REDIS_HOST', 'redis'), port=6379)
db = MySQLdb.connect("mysql","root","password")
cursor = db.cursor()

@app.route('/init')
def init():
    cursor.execute("DROP DATABASE IF EXISTS AZUREDB")
    cursor.execute("CREATE DATABASE AZUREDB")
    cursor.execute("USE AZUREDB")
    sql = """CREATE TABLE courses(id INT, coursenumber varchar(48), 
                  coursetitle varchar(256), notes varchar(256));  
     """
    cursor.execute(sql)
    db.commit()
    return "DB Initialization done\n" 

@app.route("/courses/add", methods=['POST'])
def add_courses():

    req_json = request.get_json()   
    cursor.execute("INSERT INTO courses (id, coursenumber, coursetitle, notes) VALUES (%s,%s,%s,%s)", 
          (req_json['uid'], req_json['coursenumber'], req_json['coursetitle'], req_json['notes']))
    db.commit()
    return Response("Added", status=200, mimetype='application/json')

@app.route('/courses/<uid>')
def get_courses(uid):
    hash = hashlib.sha224(str(uid)).hexdigest()
    key = "sql_cache:" + hash
    
    returnval = ""
    if (R_SERVER.get(key)):
        return R_SERVER.get(key) + "(from cache)" 
    else:
        cursor.execute("select coursenumber, coursetitle, notes from courses where ID=" + str(uid))
        data = cursor.fetchall()
        if data:
            R_SERVER.set(key,data)
            R_SERVER.expire(key, 36)
            return R_SERVER.get(key) + "\nSuccess\n"
        else:
            return "Record not found"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
