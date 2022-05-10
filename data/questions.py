import sqlalchemy
from flask import Flask

from data import db_session
from .db_session import SqlAlchemyBase

class Questions(SqlAlchemyBase):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    question = sqlalchemy.Column(sqlalchemy.String)
    answer1 = sqlalchemy.Column(sqlalchemy.String)
    answer2 = sqlalchemy.Column(sqlalchemy.String)
    answer3 = sqlalchemy.Column(sqlalchemy.String)
    rightanswer = sqlalchemy.Column(sqlalchemy.String, primary_key=True)


app = Flask(__name__)

def main():
    app.run()


if __name__ == '__main__':
    db_session.global_init("db/questions.db")
    main()
