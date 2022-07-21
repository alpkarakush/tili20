from flask import Flask, render_template
import os, logging
from flask_mysqldb import MySQL

app = Flask(__name__)
app.debug = True
app.logger.setLevel(logging.INFO)

app.config['MYSQL_HOST'] = os.environ['DB_HOST']
# app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_ROOT_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']

mysql = MySQL(app)


@app.route("/", methods=['post', 'get'])
def main():
    app.logger.info(f"Getting a request")
    
    with mysql.connection.cursor() as cursor:
        cursor.execute('select * from words')
        words = cursor.fetchall()
        mysql.connection.commit()
    
    app.logger.info(f"result: {str(words)}")

    return render_template("index.html", data=words)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)