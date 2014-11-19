import mysql.connector
from flask import Flask, jsonify, abort, make_response
from flask.ext.httpauth import HTTPBasicAuth
from flask import url_for

connection_config = {
    'host': 'localhost',
    'database': 'test',
    'port': 3306,
    'user': 'root',
    'password': 'alpine',
}

class DataBaseManager(object):
    def getLibraries(self):
        conn = mysql.connector.connect(**connection_config)
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT Id, Name, Description, Version FROM Libs")
        list = cur.fetchall()

        cur.close()
        conn.close()

        return list

    def getLibrary(self, lib_id):
        conn = mysql.connector.connect(**connection_config)
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT Id, Name, Description, Version FROM Libs WHERE Id=%s", (lib_id,))
        lib = cur.fetchone()

        cur.close()
        conn.close()

        return lib

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'pass'
    return None

db = DataBaseManager()
app = Flask(__name__, static_url_path = '')

def make_public_lib(lib):
    new_lib = {}
    for field in lib:
        if field == 'Id':
            new_lib['uri'] = url_for('get_library', lib_id=lib['Id'], _external=True)
        else:
            new_lib[field] = lib[field]
    return new_lib

@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')

@app.route('/api/libs', methods=['GET'])
def get_libraries():
    list = db.getLibraries()
    if len(list) == 0:
        abort(404)
    new_list = []
    for i in list:
        new_list.append(make_public_lib(i))
    return jsonify(libs=new_list)

@app.route('/api/libs/<int:lib_id>', methods=['GET'])
@auth.login_required
def get_library(lib_id):
    lib = db.getLibrary(lib_id)
    if lib is None:
        abort(404)
    return jsonify(lib=lib)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

if __name__ == '__main__':
    app.run(debug=True)