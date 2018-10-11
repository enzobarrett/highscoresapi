import mysql.connector
from flask import Flask, url_for
app = Flask(__name__)
import json, random, string
random = random.SystemRandom()
mydb = mysql.connector.connect(
    host='localhost', 
    user='enzo', 
    passwd='password', 
    database='highscores'
)

@app.route('/test')
def api_root():
    return 'Welcome\n'

@app.route('/')
def api_articles():
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM scores ORDER BY CAST(score AS unsigned) DESC limit 10')
    row_headers = [ x[0] for x in mycursor.description ]
    rv = mycursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    return json.dumps(json_data)


@app.route('/getnewkey')
def api_article():
    def checkduplicate(key, name):
        mycursor.execute("""select * from keytables where apikey like %s""" (key))

        mycursor.execute(
    mycursor = mydb.cursor()    
    apikey = ''.join(random.choice(string.lowercase) for x in range(5)
    tabname = ''.join(random.choice(string.lowercase) for x in range(5)
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

