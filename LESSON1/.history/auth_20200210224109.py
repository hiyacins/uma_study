from flask import Flask
from flask import render_template
from flask import request
from db import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    init_db(app)

    return app


app = create_app()


@app.route('/')
def login():
    return render_template('index.html')


@app.route("/home", methods=["POST"])
def home():
    return render_template('top.html')


## おまじない
if __name__ == "__main__":
    app.run(debug=True)