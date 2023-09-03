# фабрика базовых классов,
# от которых мы будем наследовать наши модели:
from sqlalchemy.ext.declarative import declarative_base

# нужен сам движок
# (отвечает за подключение, хранит в себе эти данные
# и правильно ими управляет...)
from sqlalchemy import create_engine

# from sqlalchemy.orm import session

# менеджер сессий (что-то вроде курсоров):
from sqlalchemy.orm import sessionmaker

# колонки и типы данных,
# а func - для проставления текущей Даты и Времени
from sqlalchemy import Column, Integer, String, DateTime, func


# ('тип БД://имя пользователя:пароль@адрес:порт/имя БД')
engine = create_engine(
    'postgresql://ad_agent:agent_password@127.0.0.1:5431/ad_site_pgdb'
)

# Session = session.sessionmaker(engine)

# базовый класс для сессий (ФАБРИКА СЕССИЙ):
Session = sessionmaker(engine)

# базовый класс для моделей:
Base = declarative_base(bind=engine)


# модель пользователя:
class User(Base):

    __tablename__ = 'ad_users'  # имя таблицы прописывается явно

    # колонки не создаются по умолчанию, как в Джанго - здесь сами делаем:

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
        )
    username = Column(
        String,
        nullable=False,
        unique=True,
        index=True
        )
    password = Column(
        String,
        nullable=False
        )
    email = Column(
        String,
        nullable=False,
        index=True
        )
    creation_time = Column(
        DateTime,
        server_default=func.now()
        )   # вызовет в postgres
            # метод now() - текущее время
            # postgres сам проставит время !!!


# модель объявления:
class Ad(Base):
    __tablename__ = 'ads'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
        )
    header = Column(
        String,
        nullable=False,
        index=True
        )
    description = Column(
        String
        )
    creation_time = Column(
        DateTime,
        server_default=func.now()
        )
    user_id = Column(
        Integer,
        nullable=False
    )


# первая миграция:
Base.metadata.create_all()
