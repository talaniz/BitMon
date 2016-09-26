import flask
from flask import Response
from flask import request
import sqlite3
import datetime
from uuid import uuid4 as uuid

app = flask.Flask(__name__)

####Define some functions that may be needed in more than one place.
def get_player_position(ckuser):
    cxn = sqlite3.connect('bitmon.db')
    cur = cxn.cursor()
    position = []
    cur.execute("SELECT xpos FROM players WHERE username='{0}'".format(ckuser))
    position.append(cur.fetchone()[0])
    cur.execute("SELECT ypos FROM players WHERE username='{0}'".format(ckuser))
    position.append(cur.fetchone()[0])
    cxn.close()
    return position

def check_if_user_exists(ckuser):
    cxn = sqlite3.connect('bitmon.db')
    cur = cxn.cursor()
    cur.execute("SELECT username FROM players")
    for row in cur.fetchall():
        if ckuser == row[0]:
            cxn.close()
            return 1
    cxn.close()
    return 0

def check_pass(ckuser,ckpassword):
    cxn = sqlite3.connect('bitmon.db')
    cur = cxn.cursor()
    cur.execute("SELECT * from players WHERE username='{0}'".format(ckuser))
    truepass = cur.fetchone()[2]
    cxn.close()
    if ckpassword == truepass:
        return 1
    else:
        return 0

def check_if_has_monsters(user):
    cxn = sqlite3.connect('bitmon.db')
    cur = cxn.cursor()
    table_name = user + '_monsters'
    cur.execute("SELECT name FROM sqlite_master where type='table' AND name='{0}'".format(table_name))
    if cur.fetchone():
        cxn.close()
        return 1
    cxn.close()
    return 0

def check_type_advantage(type1,type2):
    string = "{0}-{1}".format(type1,type2)
    types = { "Nova-Earth" : 2, "Earth-Nova" : 0.5, "Nova-Wind" : 0.5, "Wind-Nova" : 2, "Earth-Wind" : 0.5, "Wind-Earth" : 2, "Nova-Nova" : 1, "Earth-Earth" : 1, "Wind-Wind" : 1 }
    return types[string]

####Flask App Routes - The bulk of what makes it work.

@app.route('/startercheck')
def starter_check():
    user = request.args.get('user')
    check = check_if_has_monsters(user)
    return check

@app.route('/')
def show_log():
    with open('log.html','r') as f:
        page = f.read()
        return page

@app.route('/register')
def register():
    cxn = sqlite3.connect('bitmon.db')
    cur = cxn.cursor()
    user = request.args.get('user')
    passwd = request.args.get('pass')
    ipaddr = request.args.get('ipaddr')
    email = request.args.get('email')
    curtime = datetime.datetime.now()
    check = check_if_user_exists(user)
    if check != 0:
        with open('log.html','a') as f:
            f.write("\n<br />{0} tried to register {1} at {2}, but it was taken.".format(ipaddr,user,curtime))
        cxn.close()
        return "That username is already taken!"
    cur.execute('SELECT * FROM players')
    id = int(len(cur.fetchall())) + 1
    cur.execute("INSERT INTO players VALUES({0}, '{1}', '{2}', '{3}', 5000, 1, 0, 0, 0)".format(id, user, passwd, email)) 
    cxn.commit()
    table_name = "{0}_inventory".format(user)
    cur.execute("CREATE TABLE {0} ( item TEXT, desc TEXT, qty INT )".format(table_name))
    cur.execute("INSERT INTO {0} VALUES('Basic Trap','A basic monster trap used to capture BitMon.', 10)".format(table_name))
    cxn.commit()
    cxn.close()
    with open('log.html','a') as f:
        f.write("\n<br />{0} was registered from IP {1} at {2}.".format(user,ipaddr,curtime))
    return "Successfully registered!"

@app.route('/client')
def client():
    with open('client.py') as f: client = f.read()
    return Response(client, mimetype='application/octet-stream')

@app.route('/login')
def login():
    username = request.args.get('user')
    password = request.args.get('pass')
    ipaddr = request.args.get('ipaddr')
    curtime = datetime.datetime.now()
    usercheck = check_if_user_exists(username)
    if usercheck == 0:
        with open('log.html','a') as f:
            f.write("\n<br />{0} tried to log-in with username {1} at {2}, but it did not exist.".format(ipaddr, username, curtime))
        return "There is no user with that name registered!"
    if check_pass(username,password) == 1:
        with open('log.html','a') as f:
            f.write("\n<br />{0} logged in from {1} at {2}.".format(username, ipaddr, curtime))
        return "Success!"
    else:
        with open('log.html','a') as f:
            f.write("\n<br />{0} tried to log in from {1} at {2}, but they failed.".format(username, ipaddr, curtime))
        return "Incorrect password!"

@app.route('/selectstarter')
def select_starter():
    user = request.args.get('user')
    password = request.args.get('pass')
    ipaddr = request.args.get('ipaddr')
    curtime = datetime.datetime.now()
    selection = request.args.get('starter')
    if check_pass(user,password) == 0:
        return "Something appears to have gone wrong. Did you modify the client file?"
    if check_if_has_monsters(user) == 1:
        return "You already selected your first monster!"
    cxn = sqlite3.connect('bitmon.db')
    cur = cxn.cursor()
    table_name = user + "_monsters"
    cur.execute("CREATE TABLE {0} (uuid TEXT, name TEXT, type TEXT, level INT, atk INT, def INT, exp INT)".format(table_name))
    cxn.commit()
    muuid = str(uuid())
    if selection == "Yursba":
        cur.execute("INSERT INTO {0} VALUES('{1}', 'Yursba', 'Nova', 1, 17, 12, 0)".format(table_name,muuid))
        cxn.commit()
        cxn.close()
    if selection == "Grumsden":
        cur.execute("INSERT INTO {0} VALUES('{1}', 'Grumsden', 'Wind', 1, 15, 13, 0)".format(table_name,muuid))
        cxn.commit()
        cxn.close()
    if selection == "Hermyle":
        cur.execute("INSERT INTO {0} VALUES('{1}', 'Hermyle', 'Earth', 1, 20, 5, 0)".format(table_name,muuid))
        cxn.commit()
        cxn.close()
    with open('log.html','a') as f:
        f.write("\n<br />{0}: {1} selected {2} as their starter at {3}".format(ipaddr,user,selection,curtime))
    return "You have chosen {0} as your starter!".format(selection)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8383)
