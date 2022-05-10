from flask import Flask
from data import db_session

app = Flask(__name__)


def main():
    app.run()


if __name__ == '__main__':
    # db_session.global_init("db/blogs.db")
    # db_session.global_init('db/quizes.db')
    db_session.global_init('db/questions.db')
