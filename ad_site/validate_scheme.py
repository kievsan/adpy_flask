import pydantic     # содержит СХЕМЫ ВАЛИДАЦИИ

import requests as requests

from typing import Optional


class CreateUser(pydantic.BaseModel):   # здесь будет валидация пользователя
                                        # (того, что пойдет в post)
    username: str       # два обязательных поля:
    password: str       # то, что должен прислать клиент!

    # Можно добавить валидации, напр, проверять сложность пароля

    @pydantic.field_validator('password')   # валидируемое поле
    def validate_password(cls, value):      # password - так можем давать название методам валидации
        if len(value) < 8:                  # cls - класс, value - значение
            raise ValueError('passwortd short!')    # нужно выбросить исключение именно ValueError,
                                                    # и библ. pydantic его правльно обработает!
        return value                        # возвращаем уже валидированное значение
                                            # (иногда здесь хешируют пароль, но лучше делать отдельно!)


class PatchUser(pydantic.BaseModel):
    username: Optional[str] = None          # поля опциональны
    password: Optional[str] = None          # (не обязательно все обновлять...)

    @pydantic.field_validator('password')   # валидируемое поле
    def validate_password(cls, value):      # password - так можем давать название методам валидации
        if len(value) < 8:                  # cls - класс, value - значение
            raise ValueError('passwortd short!')    # нужно выбросить исключение именно ValueError,
                                                    # и библ. pydantic его правльно обработает!
        return value                        # возвращаем уже валидированное значение
                                            # (иногда здесь хешируют пароль, но лучше делать отдельно!)


class CreateAd(pydantic.BaseModel):   # валидация рекламы

    # header: str
    user_id: int

    @pydantic.field_validator('user_id')
    def validate_password(cls, value):
        url = f'http://127.0.0.1:5000/user/{value}'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError('user not found...')
        return value

