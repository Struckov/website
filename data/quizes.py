import sqlalchemy
from flask import Flask
from data import db_session

from .db_session import SqlAlchemyBase


class Quiz(SqlAlchemyBase):
    __tablename__ = 'quizes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)


app = Flask(__name__)


def main():
    app.run()


if __name__ == '__main__':
    db_session.global_init("db/quizes.db")
    main()
