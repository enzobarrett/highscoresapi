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

mycursor = mydb.cursor(buffered=True)
@app.route('/test')
def api_root():
    return 'Welcome\n'

@app.route('/')
def api_articles():
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

        test1 = 'select * from keytables where apikey like \'%s\'' % (key) 
        mycursor.execute(test1)
        row_count = mycursor.rowcount

        test2 = 'select * from keytables where name like \'%s\'' % (name)
        mycursor.execute(test2)
        row_count2 = mycursor.rowcount
        print(row_count)
        print(row_count2)
        if (row_count == 1):
            return True
        if (row_count2 == 1):
            return True
        else:
            return False
        
    apikey = ''.join(random.choice(string.lowercase) for x in range(5))
    tabname = ''.join(random.choice(string.lowercase) for x in range(5))
    while checkduplicate(apikey, tabname):
        print("generating new keys")
        apikey = ''.join(random.choice(string.lowercase) for x in range(5))
        tabname = ''.join(random.choice(string.lowercase) for x in range(5))
    mycursor.execute("create table %s (name VARCHAR(20), score VARCHAR(20))"% (tabname,))
    mycursor.execute("insert into keytables values (%s, %s)", (apikey, tabname,))
    mydb.commit()
    return apikey
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

