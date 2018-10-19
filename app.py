import mysql.connector
from flask import Flask, url_for, request, render_template, Response
import json, random, string
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
random = random.SystemRandom()
mydb = mysql.connector.connect(
    host='localhost', 
    user='enzo', 
    passwd='password', 
    database='highscores'
)

mycursor = mydb.cursor(buffered=True)

def paid(table):
    mycursor.execute('SELECT paid FROM keytables WHERE name = %s', (table,))
    rv = mycursor.fetchall()
    for row in rv:
        paid = row[0]
    return paid
def get_table(key):
    mycursor.execute('SELECT name FROM keytables WHERE apikey = %s', (key,))
    rv = mycursor.fetchall()
    table = 'e'
    for row in rv:
        table = row[0]
    print("in get table table is" + table)
    if (table == 'e'):
        return 'e'
    else:
        return table

@app.route('/test')
def api_root():
    return 'Welcome\n'

@app.route('/')
def gethighscorelist():
    #mycursor.execute('SELECT * FROM scores ORDER BY CAST(score AS unsigned) DESC limit 10')
    #row_headers = [ x[0] for x in mycursor.description ]
    #json_data = []
    #for result in rv:
    #   json_data.append(dict(zip(row_headers, result)))

    #return json.dumps(json_data)
    print(request.args['key'])
    getTable = get_table(request.args['key'])
    print("done with get table")
    if (getTable == 'e'):
        return Response("Error: not found", status=404)
    else:
        ispaid = paid(getTable)
        if (ispaid == 0):
            mycursor.execute('SELECT * FROM %s ORDER BY CAST(score AS unsigned) DESC limit 5' % (getTable,))
            rv = mycursor.fetchall()
        else:
            mycursor.execute('SELECT * FROM %s ORDER BY CAST(score AS unsigned) DESC limit 10' % (getTable,))
            rv = mycursor.fetchall()
        row_headers = [ x[0] for x in mycursor.description ]
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
        #return str(paid(getTable))
@app.route('/gettop')
def gettop():
    getTable = get_table(request.args['key'])
    print(getTable)
    mycursor.execute('select count(*) from %s' % (getTable))
    rv2 = mycursor.fetchall()
    for row in rv2:
        numberintable = row[0]
        print(numberintable)
    if (numberintable < 5):
        return "goodtogo" 
    if (numberintable >= 5):
        usenumber = 4
    mycursor.execute('select score from %s order by cast(score as unsigned) desc limit %s,1;' % (getTable, usenumber,))
    rv = mycursor.fetchall()
    for row in rv:
        return row[0]
@app.route('/insertscore')
def insert_score():
    getTable = get_table(request.args['key'])
    if (getTable == 'e'):
        return Response("Error: not found", status=404)
    else:
        mycursor.execute('insert into %s' % getTable + ' values (%s,%s)', (request.args['name'], request.args['score'],))
        mydb.commit()
        return Response("Success", status=200)
@app.route('/getnewkey')
def api_keygen():

    def checkduplicate(key, name):

        mycursor.execute('select * from keytables where apikey like %s', (key,))
        row_count = mycursor.rowcount
        mycursor.execute('select * from keytables where name like %s', (name,))
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
    mycursor.execute("create table %s (name VARCHAR(20), score VARCHAR(20))" % (tabname,))
    mycursor.execute("insert into keytables values (%s, %s, %s)", (apikey, tabname, 0))
    mydb.commit()
    return apikey
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, threaded=True)

