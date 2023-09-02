from flask import Flask, jsonify, request
from flask.views import MethodView

from typing import Type
from hashlib import md5

from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from models import Session, User
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


def hash_password(password: str) -> str:
    # преобразуем в байты
    password: bytes = password.encode()
    # байты положили в md5, привели к строке
    hashed_password = md5(password).hexdigest()
    return hashed_password


def get_user(user_id: int, session: Session) -> User:
    user = session.get(User, user_id)
    if user is None:
        raise HttpError(404, message='user not found')
    return user


class UserView(MethodView):
    # type hitting - подсказка, какой тип переменной ожидается
    def get(self, user_id: int):                # НАЙТИ
        with Session() as session:
            user = get_user(user_id, session)
            return jsonify({
                "id": user.id,
                "username": user.username,
                "creation_time": user.creation_time.isoformat()
            })

    def post(self):                             # ДОБАВИТЬ
        json_data = validate(request.json, CreateUser)
        pwd: str = json_data["password"]           # извлекаем пароль (строку) для хэширования
        json_data["password"] = hash_password(pwd) # кладем хэш (строку) обратно в json

        with Session() as session:
            new_user = User(**json_data)    # используем символы распаковки json
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError as err:
                raise HttpError(
                    409,
                    'user already exists with the same username'
                )
            return jsonify({
                "status": "add success",
                "id": new_user.id
            })

    def patch(self, user_id: int):          # РЕДАКТИРОВАТЬ
        json_data = validate(request.json, PatchUser)
        # если пароль пришел, то хэшируем его:
        if 'password' in json_data:
            json_data["password"] = hash_password(json_data["password"])

        with Session() as session:
            user = get_user(user_id, session)
            for field, value in json_data.items():
                setattr(user, field, value)
            try:
                session.commit()
            except IntegrityError as err:
                raise HttpError(409, 'username is busy')

            return jsonify({
                "status": "patch success",
                "id": user.id
            })

    def delete(self, user_id: int):         # УДАЛИТЬ
        with Session() as session:
            user = get_user(user_id, session)
            session.delete(user)
            session.commit()
            # можно в модель добавить метод
            # подготовки нужного словарика для ответа
            return jsonify({
                "status": "delete success",
                "id": user.id,
                "username": user.username,
                "creation_time": user.creation_time.isoformat()
                # "creation_time": int(user.creation_time.timestamp()) # прошло секунд
            })


app.add_url_rule('/user/<int:user_id>',
                 view_func=UserView.as_view('user_existed'),
                 methods=['GET', 'PATCH', 'DELETE']
                 )
app.add_url_rule('/user/',
                 view_func=UserView.as_view('user_new'),
                 methods=['POST']
                 )


def hello():
    return jsonify({
        "add-site": "Hello! REST API for ad-site is working yet!"
    })
app.add_url_rule('/',
                 view_func=hello,
                 methods=['POST', 'GET', 'PATCH', 'DELETE'])    # CRUD


if __name__ == '__main__':
    app.run()
