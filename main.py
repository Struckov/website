from os import listdir
from os import mkdir
from random import shuffle
import validators

import requests
from flask import Flask, request, redirect, render_template, url_for, session

from data import db_session
from data.users import User
from data.quizes import Quiz
from data.questions import Questions

app = Flask(__name__)
link = "http://127.0.0.1:8080/"
delimiter = '☺☻♥,♣•♣♠♦♦♣♠☻◙'
db_session.global_init("db/blogs.db")
db_session.global_init("db/quizes.db")
db_session.global_init("db/questions.db")

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
my_login = ''


def main():
    db_sess = db_session.create_session()

    @app.route('/')
    def to_login():
        return redirect("/login")

    @app.route('/login')
    def login():
        req = request.args.get(key='login'), request.args.get(key='pass'), request.args.get(key='reg')
        if req == (None, None, None):
            return render_template('login.html')
        elif req[-1] == 'Регистрация':
            return redirect('/reg')
        else:
            login, password = request.args.get(key='login'), request.args.get(key='pass')
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.login == login).first() is not None and \
                    db_sess.query(User).filter(User.login == login).first().password == password:
                session['id'] = db_sess.query(User).filter(User.login == login).first().id
                return redirect('/profile')
            else:
                return render_template('repeat_login.html')

    @app.route('/reg')
    def flowers():
        req = request.args.get(key='login'), request.args.get(key='pass1'), request.args.get(key='pass2')
        db_sess = db_session.create_session()
        login, pass1, pass2 = req
        if req == (None, None, None):
            return render_template('register.html')
        elif db_sess.query(User).filter(User.login == login).first() is None and pass1 == pass2:
            user = User()
            user.login = login
            user.password = pass1
            db_sess.add(user)
            db_sess.commit()
            mkdir(f'static/images/{db_sess.query(User).filter(User.login == login).first().id}')
            mkdir(f'static/images/{db_sess.query(User).filter(User.login == login).first().id}/quizes')
            return redirect('/login')
        else:
            return render_template('repeat_register.html')

    @app.route('/profile')
    def profile():
        if check() is not None:
            return check()

        id = session['id']
        session['num'] = 1

        params = dict()

        db_sess = db_session.create_session()

        params["nickname"] = db_sess.query(User).filter(User.id == id).first().login
        params["about_me"] = db_sess.query(User).filter(User.id == id).first().about_me

        params["link"] = link + "profile/"

        # params["url_to_avatar"] = url_for("static", filename=f"images/standart_avatar.png")
        params["url_to_avatar"] = url_for("static", filename=f"images/standart_avatar.png")
        quizes = listdir(path=url_for("static", filename=f"images/{id}/quizes")[1:])
        params["len_of_quizes"] = len(quizes)
        params["urls_to_quizes"] = []
        for item in quizes:
            text = db_sess.query(Quiz).filter(Quiz.id == item).first().name  # <------- item - id викторины
            mas = [
                url_for("static", filename=f"images/{id}/quizes/{item}/main_image.png"),
                text,  # <- название викторины
                f"{link}edit/{item}"
            ]
            params["urls_to_quizes"].append(mas)

        params["url_to_pencil"] = url_for("static", filename="images/pencil.png")

        return render_template(f'profile.html', **params)

    @app.route('/my_quizes/')
    def my_quizes():
        if check() is not None:
            return check()

        params = dict()
        session['num'] = 1
        id = session["id"]
        params["nickname"] = id

        params["plus_url"] = url_for("static", filename=f"images/plus.png")
        quizes = listdir(path=url_for("static", filename=f"images/{id}/quizes")[1:])
        params['len_of_quizes'] = len(quizes)
        params["urls_to_quizes"] = []
        for item in quizes:
            text = db_sess.query(Quiz).filter(Quiz.id == item).first().name
            mas = [
                url_for("static", filename=f"images/{id}/quizes/{item}/main_image.png"),
                text,  # <- название викторины
                f"{link}edit/{item}"
            ]
            params["urls_to_quizes"].append(mas)

        params["url_to_pencil"] = url_for("static", filename="images/pencil.png")

        return render_template(f'my_quizes.html', **params)

    @app.route("/create")
    def create():
        if check() is not None:
            return check()

        req = request.args.get(key='name'), request.args.get(key='image_url')
        if req != (None, None):
            db_sess = db_session.create_session()
            quiz = Quiz()
            quiz.name = req[0]
            quiz.user_id = session["id"]
            db_sess.add(quiz)
            db_sess.commit()
            mkdir(f'static/images/{session["id"]}/quizes/{quiz.id}')
            if validators.url(req[1]):

                img_data = requests.get(req[1]).content
                with open(f'static/images/{session["id"]}/quizes/{quiz.id}/main_image.png', 'wb') as handler:
                    handler.write(img_data)
            return redirect(f'/edit/{quiz.id}')

        return render_template('create.html')

    @app.route("/edit/<int:id_of_quiz>")
    def edit(id_of_quiz):
        if check() is not None:
            return check()

        db_sess = db_session.create_session()
        if "num" not in session:
            session['num'] = 1
        n = str(session['num'])
        req = request.args.get(key='question'), request.args.get(key='ans1'),\
                   request.args.get(key='ans2'), request.args.get(key='ans3'), request.args.get(key='True_ans')
        requests2 = request.args.get(key='prev'), request.args.get(key='next')

        if requests2 != (None, None):
            if requests2[0] is not None and int(n) > 1:
                session['num'] -= 1
            elif requests2[1] is not None:
                for item in db_sess.query(Questions).filter(Questions.id == id_of_quiz).all():
                    if item.rightanswer.split(delimiter)[0] == n:
                        session['num'] += 1
                        break
            n = str(session['num'])

        elif req != tuple([None] * 5):
            questions = Questions()
            questions.id = id_of_quiz
            questions.question, questions.answer1, questions.answer2, questions.answer3, p = req
            questions.rightanswer = f'{n}{delimiter}{p}'
            db_sess.add(questions)
            db_sess.commit()
        params = dict()
        db_sess = db_session.create_session()
        params["title"] = db_sess.query(Quiz).filter(Quiz.id == id_of_quiz).first().name
        params["num_of_question"] = n
        for item in db_sess.query(Questions).filter(Questions.id == id_of_quiz).all():
            if item.rightanswer.split(delimiter)[0] == n and item.id == id_of_quiz:
                params["question"] = item.question
                params["ans1"] = item.answer1
                params["ans2"] = item.answer2
                params["ans3"] = item.answer3
                params["True_ans"] = item.rightanswer.split(delimiter)[1]
                break
        else:
            params["question"] = "Вопрос"
            params["ans1"] = "Ответ 1"
            params["ans2"] = "Ответ 2"
            params["ans3"] = "Ответ 3"
            params["True_ans"] = "Правильный Ответ"

        return render_template("edit.html", **params)

    @app.route("/play")
    def play():
        if check() is not None:
            return check()
        clear_session()

        params = dict()
        req = request.args.get("select"), request.args.get("num_of_people")
        if req != (None, None):
            session["num_of_people"] = int(req[1])
            id = db_sess.query(Quiz).filter(Quiz.name == req[0]).first().id
            session["id_of_quiz"] = id
            return redirect(f'/game')

        choice = []
        for i in db_sess.query(Quiz).filter(Quiz.user_id == session['id']).all():
            choice.append(i.name)
        params["quizes"] = choice
        return render_template("play.html", **params)

    @app.route("/game")
    def game():
        if check() is not None:
            return check()

        params = dict()
        id_of_quiz = session["id_of_quiz"]
        count_of_people = session["num_of_people"]

        if "question_num" in session:
            question_num = session["question_num"]
        else:
            question_num = 1

        if "player_now" in session:
            player_now = session["player_now"]
        else:
            player_now = 1

        if "answers" in session:
            answers = session["answers"]
        else:
            answers = [list() for _ in range(count_of_people)]

        req = request.args.get(key='but1'), request.args.get(key='but2'), request.args.get(key='but3'),\
                   request.args.get(key='but4')
        if req != (None, None, None, None):
            for item in req:
                if item is not None:
                    answers[player_now - 2].append(item)

        if question_num > len(db_sess.query(Questions).filter(Questions.id == id_of_quiz).all()):
            session["answers"] = answers
            session["player_now"] = player_now
            session["question_num"] = question_num
            return redirect('/end')

        mega_filter = None
        for item in db_sess.query(Questions).filter(Questions.id == id_of_quiz
                                                    and str(Questions.rightanswer)
                                                            .split(delimiter)[0] == str(question_num)).all():
            if item.id == id_of_quiz and str(item.rightanswer).split(delimiter)[0] == str(question_num):
                mega_filter = item

        true_answer = mega_filter.rightanswer.split(delimiter)[1]
        params["order_num"] = player_now
        params["question"] = mega_filter.question
        params["ans"] = [mega_filter.answer1, mega_filter.answer2, mega_filter.answer3, true_answer]
        shuffle(params['ans'])

        player_now += 1
        if player_now > count_of_people:
            question_num += 1
            player_now %= count_of_people

        session["answers"] = answers
        session["player_now"] = player_now
        session["question_num"] = question_num

        return render_template("game.html", **params)

    @app.route('/end')
    def end():
        mas = analiz_ans(session["answers"])
        params = dict()
        params["mas"] = mas
        if len(mas[0][1]) == 1:
            params["ans"] = f"Победитель - игрок номер {mas[0][1][0]}"
        else:
            string = "Победители - игроки номера "
            for item in mas[0][1]:
                string = string + str(item) + ", "
            params["ans"] = string[:-2]
        return render_template("end.html", **params)

    def analiz_ans(mas):
        true_answers = []
        for item in db_sess.query(Questions).filter(Questions.id == session["id_of_quiz"]).all():
            true_answers.append(item.rightanswer.split(delimiter)[1])

        local_mas = []
        for item in mas:
            count_of_true_answers = 0
            for ind, ans in enumerate(item):
                if ind >= len(true_answers):
                    print(true_answers)
                    print(ind)
                if true_answers[ind] == ans:
                    count_of_true_answers += 1
            local_mas.append(count_of_true_answers)

        new_mas = {}
        for ind in range(len(local_mas)):
            if local_mas[ind] in new_mas:
                new_mas[local_mas[ind]].append(ind + 1)
            else:
                new_mas[local_mas[ind]] = [ind + 1]
        new_mas = sorted([[item, sorted(new_mas[item])] for item in new_mas], key=lambda x: -x[0])
        return new_mas

    @app.route('/quit')
    def quit():
        session.clear()
        return redirect('/login')

    def clear_session():
        id = session["id"]
        session.clear()
        session["id"] = id

    app.run(port=8080, host='127.0.0.1', debug=True)


def check():
    return redirect('/login') if session.get('id', 0) == 0 else None


main()