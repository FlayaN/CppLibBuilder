import mysql.connector
from flask import Flask, jsonify, abort, make_response
from flask.ext.httpauth import HTTPBasicAuth


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
        cur = conn.cursor()

        cur.execute("SELECT Name,Description, Version FROM Libs")
        list = cur.fetchall()

        cur.close()
        conn.close()

        return list
    def getLibrary(self, lib_id):
        conn = mysql.connector.connect(**connection_config)
        cur = conn.cursor()

        cur.execute("SELECT Name,Description, Version FROM Libs WHERE Id=%s", (lib_id,))
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
app = Flask(__name__)

@app.route('/api/libs', methods=['GET'])
def get_libraries():
    list = db.getLibraries()
    if len(list) == 0:
        abort(404)
    return jsonify(libs = list)

@app.route('/api/libs/<int:lib_id>', methods=['GET'])
def get_library(lib_id):
    lib = db.getLibrary(lib_id)
    if lib is None:
        abort(404)
    return jsonify(lib=lib)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)