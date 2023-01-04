
from flask import Flask,request,render_template,make_response
from flask_cors import CORS

from flask_mysqldb import MySQL
import MySQLdb.cursors

from datetime import datetime

app = Flask(__name__)
CORS(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'wagisha'
app.config['MYSQL_DB'] = 'airline'


mysql = MySQL(app)

default_passID = -1
default_flightID = -1

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html',ipaddress = request.remote_addr)

@app.route('/create-account')
def create():
    return render_template('create.html')

@app.route('/savedetails',methods=['POST'])
def savedetails():
    retString = "It is what is returned"

    try:
        userName = request.form['userName']
        userEmail = request.form['userEmail']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO passenger(passName,passEmail) value(%s,%s)',[userName,userEmail])
        mysql.connection.commit()
        cursor.close()
        retString = "User Inserted"

    except Exception as e:
        retString(e)

    finally:
        return render_template('error_response.html',error_response=retString)

@app.route('/delete-record')
def delete():
    return render_template('delete.html')

@app.route('/deleteRecord',methods=['POST'])
def deleteRecord():
    userName = request.form["UserName"]  
    userFlightID = request.form['FlightId']

    try:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT passID FROM passenger WHERE passName = %s',[userName])
        userID = cursor.fetchone()
        print(userID)
        cursor.execute("INSERT INTO ticket(passID,flightID,price) VALUES (%s,%s,%s)",(int(userID["passID"]),str(userFlightID),int(500)))
        mysql.connection.commit()
        cursor.close()
        msg = "TicketBooked"  
    except Exception as e:
        print(e)  
        msg = "Issue is there on server"  
    finally:  
        return render_template("error_response.html",error_response = msg)  

@app.route('/view_all')
def viewAll():
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM flight')
    rows= cursor.fetchall()
    cursor.close()

    return render_template('view.html',rows=rows)

if __name__ == "__main__":
    app.run(debug=True)