import socket
from flask import Flask, request
from healthcheck import HealthCheck, EnvironmentDump
from flask_mysqldb import MySQL
import os

application = Flask(__name__)
# wrap the flask app and give a heathcheck url
health = HealthCheck(application, "/healthcheck")
envdump = EnvironmentDump(application, "/environment")

# If there is a mysql backend, then use it.
mysql_backend = True
try:
    application.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
    application.config['MYSQL_PASSWORD']= os.environ.get('MYSQL_PASSWORD')
    application.config['MYSQL_DB']= os.environ.get('MYSQL_DATABASE')
    application.config['MYSQL_SERVICE_HOST']= os.environ.get('MYSQL_SERVICE_HOST')
except:
    mysql_backend = False

if mysql_backend:
    mysql = MySQL(application)

@application.route("/")
def hello():
    # FIXME: return json?
    return "Hello from {} to {}".format(socket.gethostname(), request.remote_addr)

@application.route("/pagecount")
def page_count():
    # NOTE: Strangely env vars like MYSQL_USER seem to be defaulted to something
    # whether or not they have been provided to the application purposely, but
    # for example MYSQL_USER is set to null: "MYSQL_USER": null
    if mysql_backend and application.config['MYSQL_USER']:

        try:
            cursor = mysql.connection.cursor()
        except:
            return "Connection fail"

        try: 
            cursor.execute('''SELECT counter FROM hits LIMIT 1''')         
        except:
            cursor.execute('CREATE TABLE IF NOT EXISTS hits ( counter INT NOT NULL )')
            cursor.execute('INSERT INTO hits VALUES(1);')
            mysql.connection.commit()
            return "0"           
        
        cursor.execute('''SELECT counter FROM hits LIMIT 1''')         
        rv = cursor.fetchone()
        cursor.execute('''UPDATE hits SET counter = counter + 1''')
        mysql.connection.commit()
        # FIXME: return json?
        return str(rv[0])
    else:
        return "0"

# Not sure if this is needed or if /healthcheck is magic
def check_health():
    return True, "ok"

def mysql_health():
    if mysql_backend and application.config['MYSQL_USER']:
        try:
            cursor = mysql.connection.cursor()
            mysql_healthy = True 
            mysql_msg = "MySQL connection succeeded"
        except:
            mysql_healthy = False
            mysql_msg = "MySQL connection failed"
    else:
        mysql_healthy = True 
        mysql_msg = "No MySQL backend specified"
        
    return mysql_healthy, mysql_msg
    
health.add_check(check_health)
health.add_check(mysql_health)

if __name__ == "__main__":
    application.run()
