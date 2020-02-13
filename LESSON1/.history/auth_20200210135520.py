from flask import Flask
from flask import url_for
from flask import redirect
from flask import render_template
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login_site.db import _open()

from DataStore.MySQL import MySQL
dns = {
    'user': 'root',
    'host': 'localhost',
    'password': 'hiya1023',
    'database': 'site_master'
}
db = MySQL(**dns)

app = Flask(__name__)

# @app.route('/')
# def hello():
#     name = "Hello World"
#     return name


@app.route('/')
#@app.route('/login')
def login(name=None):
    """
    GET ：ログイン画面に遷移
    POST：ログイン処理を実施
    """
    if request.method == 'GET':
        # ログイン画面に遷移
        return render_template('index.html', name=name)


## おまじない
if __name__ == "__main__":
    app.run(debug=True)