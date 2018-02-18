#!flask/bin/python
from flask import Flask, jsonify, abort, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from sqlite3 import dbapi2 as sqlite3
from flask_basicauth import BasicAuth
from hashlib import md5
from datetime import datetime
'''import time'''
from werkzeug import check_password_hash, generate_password_hash

app = Flask(__name__)
basic_auth = BasicAuth(app)
# configuration
DATABASE = '/tmp/minitwit.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

# create our little application :)
app = Flask('mt_api')
app.config.from_object(__name__)
"""app.config.from_envvar('MINITWIT_SETTINGS', silent=True)"""


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

def populate_db():
    """Populates data for the database."""
    db = get_db()
    with app.open_resource('populateDB.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('populatedb')
def populatedb_command():
    """Populate data for the database tables."""
    populate_db()
    print('Populated the database.')

def get_credential(username):
    user_name = query_db('''select username from user where username = ?''', [username], one=True)
    pw_hash = query_db('''select pw_hash from user where username = ?''', [username], one=True)
    app.config['BASIC_AUTH_USERNAME'] = user_name[0]
    app.config['BASIC_AUTH_PASSWORD'] = pw_hash[0]

def make_error(status_code, message, reason):
    response = jsonify({
        "status": status_code,
        "message": message,
        "reason": reason
    })
    return response

'''return username of an user_id'''
def get_username(user_id):
    cur = query_db('select username from user where user_id = ?', [user_id], one = True)
    return cur[0] if cur else None

'''return pw_hash of an user_id'''
def get_pw(user_id):
    cur = query_db('select pw_hash from user where user_id = ?', [user_id], one = True)
    return cur[0] if cur else None

def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

'''return all messages from all users '''
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = query_db('''
            select message.text, user.username from message, user
            where message.author_id = user.user_id
            order by message.pub_date desc''',
            )
    print messages
    messages = map(dict, messages)
    print messages
    return jsonify(messages)

'''return all messages form the user <user_id>'''
@app.route('/messages/<user_id>', methods =['GET'])
def get_message_user(user_id):
    messages = query_db('''
        select message.text, user.username from message, user
        where message.author_id = user.user_id and user.user_id = ? ''',
        [user_id])
    print messages
    messages = map(dict, messages)

    return jsonify(messages)

'''return all users that are followers of the user <user_id>'''
@app.route('/users/<user_id>/followers', methods = ['GET'])
def user_followers(user_id):
    messages = query_db('''
        select u1.username as followee, u2.username as follower from user u1, follower f, user u2
        where u1.user_id = f.who_id and u2.user_id = f.whom_id and u1.user_id = ? ''',
        [user_id])
    print messages
    messages = map(dict, messages)

    return jsonify(messages)

'''return all users that the user <user_id> is following'''
@app.route('/users/<user_id>/follow', methods = ['GET'])
def user_follow(user_id):
    messages = query_db('''
        select u1.username as followee, u2.username as follower from user u1, follower f, user u2
        where u1.user_id = f.who_id and u2.user_id = f.whom_id and u1.user_id = ? ''',
        [user_id])

    messages = map(dict, messages)
    print messages
    return jsonify(messages)

'''Insert a message into table message: json data: author_id, text'''
@app.route('/messages/<user_id>/add_message', methods = ['POST'])
def add_message(user_id):
    if not request.json:
        return make_error(400, "Invalid data", "Other error")
    data = request.json

    if data:
        username = get_username(user_id)
        get_credential(username)
        if not basic_auth.check_credentials(data["username"], data["pw_hash"]):
            return make_error(401, 'Unauthorized', 'Invalid Username ad/or Password')

        db = get_db()
        db.execute('''insert into message (author_id, text)
        values (?, ?)''',
        [data["author_id"], data["text"]])
        db.commit()
    return jsonify(data)

'''Insert follow: json data: who_id, whom_id'''
@app.route('/users/<user_id>/add_follow', methods = ['POST'])
def add_follow(user_id):
    if not request.json:
        return make_error(400, "Invalid data", "Other error")
    data = request.json

    if data:
        db = get_db()
        db.execute('''insert into follower (who_id, whom_id)
            values (?, ?)''',
            [user_id, data["whom_id"]])
        db.commit()
    return jsonify(data)

'''User Sign up: json data: username, email, pw_hash, pw_hash2'''
@app.route('/users/Sign_up', methods = ['POST'])
def Sign_up():
    if not request.json:
        return make_error(400, "Invalid data", "Other error")
    data = request.json

    if data:
        if not data["username"] or not data["email"] or not data["pw_hash"] \
            or not data["pw_hash2"] or data["pw_hash"] != data["pw_hash2"]:
            return make_error(400,"Invalid data","Missing or incorrect username/email/password")
        pw = generate_password_hash(data["pw_hash"])
        db = get_db()
        db.execute('''insert into user (username, email, pw_hash)
            values (?, ?, ?)''',
            [data["username"], data["email"], pw])
        db.commit()
    return jsonify(data)

if __name__ == '__main__':

    app.run(debug=True)
