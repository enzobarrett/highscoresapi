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


def paid(table):
    mycursor.execute('SELECT paid FROM keytables WHERE name = %s', (table,))
    rv = mycursor.fetchall()
    for row in rv:
        paid = row[0]
    return paid


def get_table(key):
    tablecursor = mydb.cursor()
    tablecursor.execute('SELECT name FROM keytables WHERE apikey = %s', (key,))
    tablename = tablecursor.fetchall()
    table = 'e'
    for row in tablename:
        table = row[0]
    if (table == 'e'):
        tablecursor.close()
        return 'e'
    else:
        tablecursor.close()
        return table
def get_table2(key):
    tablecursor2 = mydb.cursor()
    tablecursor2.execute('SELECT name FROM keytables WHERE apikey = %s', (key,))
    tablename = tablecursor2.fetchall()
    table = 'e'
    for row in tablename:
        table = row[0]
    if (table == 'e'):
        tablecursor2.close()
        return 'e'
    else:
        tablecursor.close()
        return table
@app.route('/')
def gethighscorelist():
    #mycursor.execute('SELECT * FROM scores ORDER BY CAST(score AS unsigned) DESC limit 10')
    #row_headers = [ x[0] for x in mycursor.description ]
    #json_data = []
    #for result in rv:
    #   json_data.append(dict(zip(row_headers, result)))

    #return json.dumps(json_data)
    getTable = get_table(request.args['key'])
    print(getTable)
    if (getTable == 'e'):
        return Response("Error: not found", status=404)
    else:
        getcursor = mydb.cursor()
        getcursor.execute('SELECT * FROM %s ORDER BY CAST(score AS unsigned) DESC limit 5' % (getTable,))
        topscores = getcursor.fetchall()
        print("fetch get scores")
        row_headers = [ x[0] for x in getcursor.description ]
        getcursor.close()
        json_data = []
        for result in topscores:
            json_data.append(dict(zip(row_headers, result)))
        return json.dumps(json_data)
        #return str(paid(getTable))
@app.route('/gettop')
def gettop():
    getTable = get_table(request.args['key'])
    topcursor = mydb.cursor()
    topcursor.execute('select count(*) from %s' % (getTable))
    rv2 = topcursor.fetchall()
    topcursor.close()
    for row in rv2:
        numberintable = row[0]
        print(numberintable)
    if (numberintable < 5):
        return "goodtogo" 
    if (numberintable >= 5):
        usenumber = 4
    nthcursor = mydb.cursor()
    nthcursor.execute('select score from %s order by cast(score as unsigned) desc limit %s,1;' % (getTable, usenumber,))
    rv3 = nthcursor.fetchall()
    nthcursor.close()
    for row in rv3:
        return row[0]
@app.route('/insertscore')
def insert_score():
    getTable = get_table2(request.args['key'])
    if (getTable == 'e'):
        return Response("Error: not found", status=404)
    else:
        insertcursor = mydb.cursor()
        insertcursor.execute('insert into %s' % getTable + ' values (%s,%s)', (request.args['name'], request.args['score'],))
        mydb.commit()
        insertcursor.close()
        return Response("Success", status=200)
@app.route('/getnewkey')
def api_keygen():

    def checkduplicate(key, name):
        checkcursor = mydb.cursor(buffered=True)
        checkcursor.execute('select * from keytables where apikey like %s', (key,))
        row_count = checkcursor.rowcount
        checkcursor.execute('select * from keytables where name like %s', (name,))
        row_count2 = checkcursor.rowcount
        checkcursor.close()
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
    addkeycursor = mydb.cursor()
    addkeycursor.execute("create table %s (name VARCHAR(20), score VARCHAR(20))" % (tabname,))
    addkeycursor.execute("insert into keytables values (%s, %s, %s)", (apikey, tabname, 0))
    mydb.commit()
    addkeycursor.close()
    return apikey
if __name__ == '__main__':
    app.run()

