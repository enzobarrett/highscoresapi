import mysql.connector
from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/key=fp6ppmnjew')
def api_articles():
    return "High Schores\n"

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

if __name__ == '__main__':
    app.run()
