from typing import Type

from flask import jsonify, request
from flask.views import MethodView

from models import Session, User
from validate_scheme import CreateUser, PatchUser
from security import HttpError, hash_password

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


def validate(json_data: dict,
             model_class: Type[CreateUser] | Type[PatchUser]):
    try:
        model_item = model_class(**json_data)
        return model_item.model_dump(exclude_none=True) # чтобы не было None
    except ValidationError as err:
        # будет список ошибок, полей от библ. pydantic с подробным описанием
        raise HttpError(400, err.errors())


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

