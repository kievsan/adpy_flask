from hashlib import md5


def hash_password(password: str) -> str:
    # преобразуем в байты
    password: bytes = password.encode()
    # байты положили в md5, привели к строке
    hashed_password = md5(password).hexdigest()
    return hashed_password


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