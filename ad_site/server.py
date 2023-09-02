from flask import Flask, jsonify

from typing import Type

from pydantic import ValidationError

from validate_scheme import CreateUser, PatchUser


app = Flask(__name__)


def validate(json_data: dict,
             model_class: Type[CreateUser] | Type[PatchUser]):
    try:
        model_item = model_class(**json_data)
        return model_item.model_dump(exclude_none=True) # чтобы не было None
    except ValidationError as err:
        # будет список ошибок, полей от библ. pydantic с подробным описанием
        raise HttpError(400, err.errors())


class HttpError(Exception):     #  свой класс ошибок
    def __init__(
            self,
            status_code: int,
            message: dict | list | str
            ):
        # должен передать какую-то полезную инфу,
        # которую планируем передавать пользователю
        # Как правило, это status_code и message

        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    # http-ответ клиенту:
    response = jsonify({
        "status": error.status_code,
        "message": error.message
    })
    response.status_code = error.status_code
    return response





def hello():
    return jsonify({
        "add-site": "Hello! REST API for ad-site is working yet!"
    })
app.add_url_rule('/',
                 view_func=hello,
                 methods=['POST', 'GET', 'PATCH', 'DELETE'])    # CRUD

if __name__ == '__main__':
    app.run()
