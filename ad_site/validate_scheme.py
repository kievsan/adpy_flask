import pydantic     # содержит СХЕМЫ ВАЛИДАЦИИ

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

