from flask import Flask, redirect, render_template, request, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)

# DB接続・切断に関するクラス


class MySQLConnector:
    # 初期化
    def __init__(self):
        self.db_connect = ""
        self.cursor = ""

    # DB接続
    def connect(self):
        # DB接続情報
        db_config = {
            'user': 'root',
            'password': 'hiya1023',
            'host': 'localhost',
            'port': 3306,
            'database': 'site_users'
        }
        self.db_connect = mysql.connector.connect(**db_config)
        # cursor = con.cursor(buffered=True), prepared=True
        self.cursor = self.db_connect.cursor(prepared=True)

    # DB切断
    def disconnect(self):
        # カーソルとコネクトの切断
        self.cursor.close()
        self.db_connect.close()

    #
    # SQL実行してDBにparamが存在すればtrueを返す。
    # sql:sql文を入れる
    # param：照合したいテーブルのフィールド名
    def execute(self, sql, param=None):
        self.cursor.execute(sql, (param, ))
        # fetchone()で1件取り出し
        return self.cursor.fetchone()


# シークレットキーの設定
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
    db = MySQLConnector()
    db.connect()
    debug_print("DB接続")

    # ユーザー名とパスワードのチェックはここに書く
    #
    message = None
    # DBからユーザーIDを抽出する
    results = db.execute(
        "SELECT * FROM site_users WHERE id_name = ?", id_name)
    # デバッグ出力：bytearray(b'pbkdf2:sha256:150000$rtNJvHvC$37feec29a8f8fbaff527a1a8f5ea51cc144f5a9d2ffb3455a9b31f36e38f6bb9')
    debug_print(results[2])

    # ToDo: SQLで抽出した結果をresultsに格納しているが、bytearrayで出力してしまうので、データの成形が必要
    # results2 = results.translate(str.maketrans("", "", "bytearray(b'')"))
    # debug_print(results2)

    # ユーザーIDがDB内になければ、ログイン失敗する
    if results is None:
        message = 'ログイン失敗：ユーザー名が正しくありません'
        debug_print("NG_use")
        return render_template('index.html', message=message)

    # ここでpasswordの照合して合わなければログイン失敗
    if not check_password_hash("pbkdf2:sha256:150000$rtNJvHvC$37feec29a8f8fbaff527a1a8f5ea51cc144f5a9d2ffb3455a9b31f36e38f6bb9", password):
        # if not check_password_hash(results[2], password):
        message = 'ログイン失敗：パスワードが正しくありません'
        debug_print("NG_pass")
        return render_template('index.html', message=message)

    # DB切断する
    db.disconnect()

    # セッション初期化
    # session.clear()
    # ログインIDにIDを付与する
    # session['id_name'] = results[0]

    debug_print("OK")
    # ログイン後のページへリダイレクト
    return redirect(url_for('home'))


@app.route("/home", methods=["GET"])
# ログイン成功後の画面
def home():
    message = 'ログインを成功しました＼(^o^)／'
    return render_template('top.html', message=message)


@app.route("/signout", methods=["GET"])
# ToDo:ログアウト処理
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
