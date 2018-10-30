import pymysql.cursors
from flask import Flask, url_for, request, render_template, Response
import json, random, string
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
random = random.SystemRandom()
mydb = pymysql.connect(
    host='localhost',
    user='enzo',
    passwd='password',
    database='highscores'
)


@app.route('/')
def gethighscorelist():
    getstring = 'SELECT * FROM ' + str(request.args['key']) + ' ORDER BY CAST(score AS unsigned) DESC limit 5'
    getcursor = mydb.cursor()
    getcursor.execute(getstring)
    getcursor.close()
    topscores = getcursor.fetchall()
    print(topscores)
    json_data = []
    #field_names = [i[0] for i in getcursor.description]
    field_names = [u'name', u'score']
    print(field_names)
    for result in topscores:
        json_data.append(dict(zip(field_names, result)))
    print("about to return")
    print(json_data)
    return Response(json.dumps(json_data), status=200)
    #return str(paid(getTable))
@app.route('/gettop')
def gettop():
    gettopstring = 'select count(*) from ' + str(request.args['key'])
    topcursor = mydb.cursor()
    topcursor.execute(gettopstring)
    topcursor.close()
    rv2 = topcursor.fetchall()
    for row in rv2:
        numberintable = row[0]
    if (numberintable < 5):
        return "goodtogo"
    if (numberintable >= 5):
        usenumber = 4
    nthstring = 'select score from ' + request.args['key'] + ' order by cast(score as unsigned) desc limit ' + str(usenumber) + ',1;'
    nthcursor = mydb.cursor()
    nthcursor.execute(nthstring)
    nthcursor.close()
    rv3 = nthcursor.fetchall()
    for row in rv3:
        return row[0]
@app.route('/insertscore')
def insert_score():
    string = 'insert into ' + request.args['key'] + ' values (%s,%s)'
    insertcursor = mydb.cursor()
    insertcursor.execute(string, (request.args['name'], request.args['score'],))
    insertcursor.close()
    return Response("success", status=200)
    mydb.commit()
@app.route('/getnewkey')
def api_keygen():
    def checkduplicate(key, name):
        checkcursor = mydb.cursor()
        checkcursor.execute('select * from keytables where apikey like %s', (key,))
        checkcursor.close()
        row_count = checkcursor.rowcount
        checkcursor2 = mydb.cursor()
        checkcursor2.execute('select * from keytables where name like %s', (name,))
        checkcursor2.close()
        row_count2 = checkcursor2.rowcount
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
    addkeycursor.execute("create table %s (name VARCHAR(20), score VARCHAR(20))" % (apikey,))
    addkeycursor.close()
    mydb.commit()
    return apikey
@app.route('/checktable')
def checktable():
    checkstring = "SHOW TABLES LIKE " + str(request.args['table'])
    checkcursor = mydb.cursor()
    checkcursor.execute(checkstring)
    checkcursor.close()
    if (checkcursor.rowcount > 0): 
        return "found"
    else: 
        return "notfound"
    
if __name__ == '__main__':
    app.run(threaded=False)
