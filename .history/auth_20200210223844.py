from flask import Flask
from flask import render_template
from flask import request
from flask_sample.database import init_db

app = Flask(__name__)
app.config.from_object('config.Config')


@app.route('/')
def login():
    return render_template('index.html')


@app.route("/home", methods=["POST"])
def home():
    return render_template('top.html')


## おまじない
if __name__ == "__main__":
    app.run(debug=True)