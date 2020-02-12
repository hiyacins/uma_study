from flask import Flask, jsonify
from flask import render_template
from flask import request
import mysql.connector

config = {
    'user': 'root',
    'password': 'hiya1023',
    'host': 'localhost',
    'port': 3306,
    'database': 'site_master'
}
app = Flask(__name__)


@app.route('/')
def login():
    # ログインフォームに入力されたユーザーIDとパスワードの取得
    userid = request.form['userid']
    password = request.form['password']

    # DB接続
    con = mysql.connector.connect(**config)
    cursor = con.cursor(buffered=True)

    # ユーザー名とパスワードのチェック
    error_message = None

    stmt = "select * from site_master_login_tb"
    cursor.execute(stmt)
    results = cursor.fetchall()
    print(results)

    return render_template('index.html')


@app.route("/home", methods=["GET", "POST"])
def home():
    con = mysql.connector.connect(**config)
    cursor = con.cursor(buffered=True)

    stmt = "select * from site_master_login_tb"
    cursor.execute(stmt)
    results = cursor.fetchall()
    print(results)

    return render_template('top.html')


## おまじない
if __name__ == "__main__":
    app.run(debug=True)