import sqlalchemy
from flask import Flask
from .db_session import SqlAlchemyBase
from . import db_session


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    about_me = sqlalchemy.Column(sqlalchemy.String, default='')


app = Flask(__name__)


def main():
    app.run()


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    main()
