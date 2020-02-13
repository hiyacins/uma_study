from flask import Flask
from flask import render_template
from flask import request
import os


# from db import MySQL
# dns = {
#     'user': 'root',
#     'host': 'localhost',
#     'password': 'hiya1023',
#     'database': 'site_master'
# }
# db = MySQL(**dns)
# Flask
class SystemConfig:
    DEBUG = True
    SECRET_KEY = os.urandom(24)  #追記

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/database?charset=utf8mb4'.format(
        **{
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'hiya1023'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'site_master')
        })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


Config = SystemConfig

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('index.html')


@app.route("/home", methods=["POST"])
def home():
    return render_template('top.html')


## おまじない
if __name__ == "__main__":
    app.run(debug=True)