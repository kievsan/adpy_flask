from typing import Type

from flask import jsonify, request
from flask.views import MethodView

from models import Session, Ad
from validate_scheme import CreateAd
from security import HttpError

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


def validate(json_data: dict,
             model_class: Type[CreateAd]):
    try:
        model_item = model_class(**json_data)
        return model_item.model_dump(exclude_none=True)
    except ValidationError as err:
        raise HttpError(400, err.errors())


def get_ad(ad_id: int, session: Session) -> Ad:
    ad = session.get(Ad, ad_id)
    if ad is None:
        raise HttpError(404, message='ad not found')
    return ad


class AdView(MethodView):
    def get(self, ad_id: int):                # НАЙТИ
        with Session() as session:
            ad = get_ad(ad_id, session)
            return jsonify({
                "id": ad.id,
                "header": ad.header,
                "description": ad.description,
                "creation_time": ad.creation_time.isoformat(),
                "user_id": ad.user_id
            })

    def post(self):                             # ДОБАВИТЬ
        json_data = validate(request.json, CreateAd)
        with Session() as session:
            new_ad = Ad(**json_data)
            session.add(new_ad)
            try:
                session.commit()
            except IntegrityError as err:
                raise HttpError(
                    409,
                    f'ad already exists with the same data   {err}'
                )
            return jsonify({
                "status": "advertisement add success",
                "id": new_ad.id
            })

    def patch(self, ad_id: int):          # РЕДАКТИРОВАТЬ
        json_data = validate(request.json, CreateAd)
        with Session() as session:
            ad = get_ad(ad_id, session)
            for field, value in json_data.items():
                setattr(ad, field, value)
            try:
                session.commit()
            except IntegrityError as err:
                raise HttpError(409, 'username is busy')

            return jsonify({
                "status": "advertisement patch success",
                "id": ad.id
            })

    def delete(self, ad_id: int):         # УДАЛИТЬ
        with Session() as session:
            ad = get_ad(ad_id, session)
            session.delete(ad)
            session.commit()
            return jsonify({
                "id": ad.id,
                "header": ad.header,
                "creation_time": ad.creation_time.isoformat(),
                "user_id": ad.user_id
            })
