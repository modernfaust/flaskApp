from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL

import pymysql
import werkzeug

mysql=MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Hardnigga12323'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
	return render_template('index.html')
	
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
	
@app.route('/signUp',methods=['POST', 'GET'])
def signUp():
# read the posted values from the UI
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        # validate the received values
        if _name and _email and _password:
                
            # All Good, let's call MySQL
            conn = mysql.connect(host='localhost', user='root', passwd='Hardnigga12323', db='bucketlist')
            cursor = conn.cursor()
            _hashed_password = werkzeug.security.generate_password_hash(_password)
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
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()
 
if __name__ == "__main__":
#app.run(host='0.0.0.0')
    app.run()