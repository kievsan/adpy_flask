from flask import Flask, jsonify

from ads import AdView
from security import HttpError
from users import UserView

app = Flask(__name__)


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    # http-ответ клиенту:
    response = jsonify({
        "status": error.status_code,
        "message": error.message
    })
    response.status_code = error.status_code
    return response


app.add_url_rule('/user/<int:user_id>',
                 view_func=UserView.as_view('user_existed'),
                 methods=['GET', 'PATCH', 'DELETE']
                 )
app.add_url_rule('/user/',
                 view_func=UserView.as_view('user_new'),
                 methods=['POST']
                 )

app.add_url_rule('/ad/<int:ad_id>',
                 view_func=AdView.as_view('ad_existed'),
                 methods=['GET', 'PATCH', 'DELETE']
                 )
app.add_url_rule('/ad/',
                 view_func=AdView.as_view('ad_new'),
                 methods=['POST']
                 )


def hello():
    return jsonify({
        "add-site": "Hello! REST API for ad-site is working yet!"
    })


app.add_url_rule('/',
                 view_func=hello,
                 methods=['POST', 'GET', 'PATCH', 'DELETE'])  # CRUD

if __name__ == '__main__':
    app.run()
