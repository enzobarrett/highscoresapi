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

@app.route('/')
def get():
    return "yoyoyo"

@app.route('/get')
def gethighscorelist():
    checkstring = "SHOW TABLES LIKE %s"  
    checkcursor = mydb.cursor(buffered=True)
    checkcursor.execute(checkstring, (request.args['key'],))
    rowcount = checkcursor.rowcount
    checkcursor.close()
    if (rowcount > 0): 
        getstring = 'SELECT * FROM {}'.format(request.args['key']) + ' ORDER BY CAST(score AS unsigned) DESC limit 5'
        print(getstring)
        getcursor = mydb.cursor()
        getcursor.execute(getstring)
        topscores = getcursor.fetchall()
        getcursor.close()
        print(topscores)
        json_data = []
        field_names = [u'name', u'score']
        for result in topscores:
            json_data.append(dict(zip(field_names, result)))
        return Response(json.dumps(json_data), status=200)
    else: 
        return "notfound"
@app.route('/gettop')
def gettop():
    checkstring = "SHOW TABLES LIKE %s"  
    checkcursor = mydb.cursor(buffered=True)
    checkcursor.execute(checkstring, (request.args['key'],))
    rowcount = checkcursor.rowcount
    checkcursor.close()
    if (rowcount > 0): 
        gettopstring = 'select count(*) from {}'.format(request.args['key'])
        topcursor = mydb.cursor()
        topcursor.execute(gettopstring)
        rv2 = topcursor.fetchall()
        topcursor.close()
        for row in rv2:
            numberintable = row[0]
        if (numberintable < 5):
            return "goodtogo"
        if (numberintable >= 5):
            usenumber = 4
        nthstring = 'select score from {}'.format(request.args['key']) + ' order by cast(score as unsigned) desc limit ' + str(usenumber) + ',1;'
        nthcursor = mydb.cursor()
        nthcursor.execute(nthstring)
        rv3 = nthcursor.fetchall()
        nthcursor.close()
        for row in rv3:
            return row[0]
    else: 
        return "notfound"
@app.route('/insertscore')
def insert_score():
    checkstring = "SHOW TABLES LIKE %s"  
    checkcursor = mydb.cursor(buffered=True)
    checkcursor.execute(checkstring, (request.args['key'],), multi=False)
    rowcount = checkcursor.rowcount
    checkcursor.close()
    if (rowcount > 0): 
        string = 'insert into {}'.format(request.args['key']) + ' values (%s,%s)'
        insertcursor = mydb.cursor(buffered=True)
        insertcursor.execute(string, (request.args['name'], request.args['score'],))
        mydb.commit()
        insertcursor.close()
        return Response("success", status=200)
    else: 
        return "notfound"
@app.route('/getnewkey')
def api_keygen():
    def checkduplicate(key, name):
        checkcursor = mydb.cursor(buffered=True)
        checkcursor.execute('select * from keytables where apikey like %s', (key,))
        row_count = checkcursor.rowcount
        checkcursor.close()
        checkcursor2 = mydb.cursor(buffered=True)
        checkcursor2.execute('select * from keytables where name like %s', (name,))
        row_count2 = checkcursor2.rowcount
        checkcursor2.close()
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
    addkeycursor = mydb.cursor(buffered=True)
    addkeycursor.execute("create table %s (name VARCHAR(20), score VARCHAR(20))" % (apikey,))
    addkeycursor.close()
    mydb.commit()
    return apikey
    
if __name__ == '__main__':
    app.run(threaded=False)
