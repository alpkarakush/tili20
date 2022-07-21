import psycopg2
from flask import Flask, render_template
import os, logging

app = Flask(__name__)
app.debug = True
app.logger.setLevel(logging.INFO)

# con = psycopg2.connect(dbname=os.environ['DB_NAME'], 
#                        user=os.environ['DB_USERNAME'], 
#                        password=os.environ['DB_PASSWORD'], 
#                        host=os.environ['DB_HOST'], 
#                        port=os.environ['DB_PORT'])
# cursor = con.cursor()

@app.route("/", methods=['post', 'get'])
def main():
    # cursor.execute("select * from flats")
    # result = cursor.fetchall()
    # app.logger.info(f"result: {str(result)}")
    words = [{
                'word' : 'soz1',
                'definition' : 'def1'
            },{
                'word' : 'soz1',
                'definition' : 'def1'
            },{
                'word' : 'soz1',
                'definition' : 'def1'
            }]
    return render_template("index.html", data=words)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)