import os
import psycopg2
import psycopg2.extras
from flask import Flask, request, render_template, g, current_app
from flask.cli import with_appcontext
import click

app = Flask(__name__)

####################################################

@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/dump")
def dump_entries():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select id, date, title, content from entries order by date')
    rows = cursor.fetchall()
    output = ""
    for r in rows:
        debug(str(dict(r)))
        output += str(dict(r))
        output += "\n"
    return "<pre>" + output + "</pre>"

@app.route("/browse")
def browse():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select id, date, title, content from entries order by date')
    rowlist = cursor.fetchall()
    return render_template('browse.html', entries=rowlist)

#####################################################
  
def connect_db():
    debug("Connecting to DB.")
    conn = psycopg2.connect(host="localhost", user="postgres", password="w22121967", dbname="practise", cursor_factory=psycopg2.extras.DictCursor)
    return conn
    
def get_db():
    if "db" not in g:
        g.db = connect_db()

    return g.db
    
@app.route("/initdb")
def init_db():
    conn = get_db()
    cur = conn.cursor()
    with current_app.open_resource("schema.sql") as file: # open the file
        alltext = file.read() # read all the text
        cur.execute(alltext) # execute all the SQL in the file
    conn.commit()
    print("Initialized the database.")

@app.route('/populate')
def populate_db():
    conn = get_db()
    cur = conn.cursor()
    with current_app.open_resource("populate.sql") as file: # open the file
        alltext = file.read() # read all the text
        cur.execute(alltext) # execute all the SQL in the file
    conn.commit()
    print("Populated DB with sample data.")
    dump_entries()

def debug(s):
    if app.config['DEBUG']:
        print(s)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)