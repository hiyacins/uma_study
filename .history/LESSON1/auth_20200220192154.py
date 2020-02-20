from flask import Flask, redirect, render_template, request, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)


# DB接続・切断に関するクラス
class MySQLConnector:
    # 初期化
    def __init__(self):
        self.mysql_connection = None
        self.mysql_cursor = None

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
        self.disconnect()
        self.mysql_connection = mysql.connector.connect(**db_config)
        self.mysql_cursor = self.mysql_connection.cursor(prepared=True)

    # DB切断
    def disconnect(self):
        # カーソルとコネクトの切断
        # self.mysql_cursor.close()
        # self.mysql_connection.close()
        pass

        #
        # SQL実行してDBにparamが存在すればtrueを返す。
        # sql:sql文を入れる
        # param：照合したいテーブルのフィールド名
    def execute(self, sql, param=None):
        self.mysql_cursor.execute(sql, param)
        # fetchone()で1件取り出し
        return self.mysql_cursor.fetchone()


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

    # --　ｓユーザー名とパスワードのチェックはここに書く
    # メッセージ初期化
    message = None

    # DBからユーザーIDを抽出する
    result_id_name = db.execute(
        "SELECT id,id_name,password FROM site_users WHERE id_name = ?", (id_name,))
    debug_print(result_id_name)

    # ユーザーIDがDB内になければ、ログイン失敗する
    if result_id_name is None:
        message = 'ログイン失敗：ユーザー名が正しくありません'
        debug_print("NG_use")
        return render_template('index.html', message=message)

    # DBからユーザーIDを抽出する
    # result_password = db.execute(
    #     "SELECT password FROM site_users WHERE password = ?", (password,))
    # debug_print(result_password)
    # ここでpasswordの照合して合わなければログイン失敗
    if not check_password_hash(result_id_name['password'], password):
        message = 'ログイン失敗：パスワードが正しくありません'
        debug_print("NG_pass")
        return render_template('index.html', message=message)

    # DB切断する
    db.disconnect()

    # セッション初期化
    session.clear()
    # ToDo: result[1]の処理
    # セッションにログインIDを追加する
    #session['id_name'] = results[1]

    # debug_print(session['id_name'])
    debug_print("OK")
    # ログイン後のページへリダイレクト
    return redirect(url_for('home'))


@app.route("/home", methods=["GET"])
# ログイン成功後の画面
def home():
    message = 'ログインを成功しました＼(^o^)／'
    # debug_print(session['id_name'])
    return render_template('top.html', message=message)


@app.route("/logout", methods=["GET"])
# ToDo:ログアウト処理
def logout():
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
