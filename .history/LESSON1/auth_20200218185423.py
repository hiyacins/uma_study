from flask import Flask, redirect, render_template, request, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import string

app = Flask(__name__)
# シークレットキーの設定


# DB接続・切断に関するクラス
class MySQLConnector:

    def __init__(self):
        self.connect = ""
        self.cursor = ""

    # DB接続
    def connect(self):
        # DB接続情報
        self.config = {
            'user': 'root',
            'password': 'hiya1023',
            'host': 'localhost',
            'port': 3306,
            'database': 'site_users'
        }
        self.mysql.connector.connect(**config)
        #cursor = con.cursor(buffered=True)
        self.cursor(prepared=True)

    # DB接断
    def disconnect():
        self.cursor.close()
        self.connector.close()

    # クエリ実行
    def execute(sql, param=None):
        pass


app.config["SECRET_KEY"] = "b't\xd7.\xedOa\xd8\x88\x18\xc51H\xf5\x0b\xb1\x10\x99\xde\x11\xa9\x12\xe3\xd3S'"


@app.route('/', methods=["GET", "POST"])
# ログイン前画面　ログイン失敗時もここ
def login():
    if request.method == 'GET':
        # ログイン画面に遷移
        return render_template('index.html')

    # ログインフォームに入力されたユーザーIDとパスワードの取得
    id_name = request.form['id_name']
    password = request.form['password']
    debug_print(id_name)
    debug_print(password)

    # DB接続
    db = MySQLConnector

    debug_print("DB接続")

    # ユーザー名とパスワードのチェック
    #message = None
    results = db.execute(
        "SELECT * FROM site_users WHERE id_name = ?", (id_name, ))
    #results = db.fetchone()
    debug_print(db.fetchone())

    # table = str.maketrans("", "", "bytearray(b'')")
    # results2 = results.translate(str.maketrans("", "", string.punctuation))
    # debug_print(results2)

    #
    if results is None:
        #message = 'ユーザー名が正しくありません'
        flash("ログイン失敗", category="failed")
        debug_print("NG_use")
        return render_template('index.html')

    #
    if not check_password_hash(results, password):
        flash("ログイン失敗", category="failed")
        debug_print(results)
        debug_print("NG_pass")
        return render_template('index.html')

    #flash("ログインを成功しました＼(^o^)／", category="success")
    # db.close()
    # dbconnect.close()
    # session.clear()
    # session['id_name'] = user['id']
    debug_print("OK")
    return redirect(url_for('home'))


@app.route("/home", methods=["GET"])
# ログイン成功後の画面
def home():
    return render_template('top.html')


@app.route("/signout", methods=["GET"])
# ログアウト処理
def signout():
    # セッションをカラにする
    session.clear()
    return redirect(url_for('login'))


# デバッグ用の文字を出力する
# s:文字列
def debug_print(s):
    if True:
        print(s)


if __name__ == "__main__":
    app.run(debug=True)