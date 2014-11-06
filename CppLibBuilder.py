import pymysql
from flask import Flask, jsonify, abort, make_response
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

app = Flask(__name__)

libs = [
    {
        'id': 1,
        'title': u'Project 1',
        'description': u'This is project 1',
        'version': '1.0'
    },
    {
        'id': 2,
        'title': u'Project 2',
        'description': u'This is project 2',
        'version': '0.1'
    }
]

@app.route('/api/libs', methods=['GET'])
def get_libs():
    return jsonify({'libs': libs})

@app.route('/api/libs/<int:lib_id>', methods=['GET'])
def get_lib(lib_id):
    lib = list(filter(lambda t: t['id'] == lib_id, libs))
    if len(lib) == 0:
        abort(404)
    return jsonify({'lib': lib[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)

# conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='mysql')
#
# cur = conn.cursor()
#
# cur.execute("SELECT Host,User FROM user")
#
# print(cur.description)
#
# for row in cur:
#    print(row)
#
# cur.close()
# conn.close()


#def test():
#    print("Hello world")

#test()