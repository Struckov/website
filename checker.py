from flask import Flask, render_template, url_for, make_response
from os import listdir
import requests

app = Flask(__name__)
link = "http://127.0.0.1:8080/"


@app.route('/my_quizes')
def my_quizes():
    params = dict()

    id = 2
    params["nickname"] = id

    params["plus_url"] = url_for("static", filename=f"images/plus.png")
    quizes = listdir(path=url_for("static", filename=f"images/{id}/quizes")[1:])
    params['len_of_quizes'] = len(quizes)
    params["urls_to_quizes"] = []
    for item in quizes:
        text = "Название викторины"  # <---------------------------------------------------------
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
    params = dict()
    image = requests.get("https://html5book.ru/wp-content/uploads/2015/04/webbutton.png").content
    with open("static/images/test.png", "wb") as file:
        file.write(image)
    id = 2
    params["nickname"] = id
    return render_template('create.html', **params)


@app.route("/edit/<int:id_of_quiz>")
def edit(id_of_quiz):
    params = dict()
    params["title"] = str(id_of_quiz)
    params["num_of_question"] = "10"
    params["question"] = "Вопрос"
    params["ans1"] = "Ответ 1"
    params["ans2"] = "Ответ 2"
    params["ans3"] = "Ответ 3"
    params["True_ans"] = "Правильный Ответ"

    return render_template("edit.html", **params)


@app.route("/play")
def play():
    params = dict()
    params["quizes"] = ["Викторина 1", "Викторина 2", "Викторина 3"]
    return render_template("play.html", **params)


@app.route("/game")
def game():
    params = dict()
    params["order_num"] = 1
    params["question"] = "ВОПРОС"
    params["ans"] = ["qwemqw", "qlwknde", "qwertyuop", "bbu"]
    return render_template("game.html", **params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)

