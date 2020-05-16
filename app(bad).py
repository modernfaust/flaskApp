# -*- coding: utf-8 -*-
"""
Created on Wed May 13 21:03:35 2020

@author: Borges
"""

from flask import Flask, render_template, request, json
import pymysql
from werkzeug import generate_password_hash, check_password_hash

app=Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'jay'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jay'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    conn = mysql.connect()
    cursor = conn.cursor()
    
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    
    if _name and _email and _password:
        _hashed_password = generate_password_hash(_password)
        print("length hashed password: ", len(_hashed_password))
        cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !'})
        else:
            return json.dumps({'error':str(data[0])})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})



if __name__ == "__main__":
    app.run()
    