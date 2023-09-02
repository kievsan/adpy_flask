from flask import Flask, jsonify

app = Flask(__name__)


def hello():
    return jsonify({
        "add-site": "Hello! REST API for ad-site is working yet!"
    })
app.add_url_rule('/',
                 view_func=hello,
                 methods=['POST', 'GET', 'PATCH', 'DELETE'])    # CRUD

if __name__ == '__main__':
    app.run()
