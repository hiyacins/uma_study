from flask import Flask, redirect, render_template, request, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)


# DB接続・切断に関するクラス
class MySQLConnector:
    # コネクタとカーソルを初期化
    def __init__(self):
        self.mysql_connection = None
        self.mysql_cursor = None

    # DB接続
    # config: DB接続情報
    def connect(self, mysql_config: dict):
        # 二重接続回避
        self.disconnect()
        # SQLに接続します
        self.mysql_connection = mysql.connector.connect(**mysql_config)
        # カーソルを定義する
        # オプションは今後必要なら引数化してもいいかも？
        self.mysql_cursor = self.mysql_connection.cursor(prepared=True)

    # DB切断
    def disconnect(self):
        # カーソルとコネクトの切断
        # mysql_cursor mysql_connectionがNoneの時はclose出来ない（型エラーになる）
        if self.mysql_cursor is not None:
            self.mysql_cursor.close()
            # closeしたらすぐにNone代入
            self.mysql_cursor = None
        if self.mysql_connection is not None:
            self.mysql_connection.close()
            # closeしたらすぐにNone代入
            self.mysql_connection = None

    # SQL実行
    # sql:sql文を入れる
    #     （例）"SELECT id,password FROM site_users WHERE id_name = ?"
    # param：フィールド名
    def execute(self, sql: str, param: tuple = None) -> tuple:
        self.mysql_cursor.execute(sql, param)


# シークレットキーの設定
app.config["SECRET_KEY"] = "b't\xd7.\xedOa\xd8\x88\x18\xc51H\xf5\x0b\xb1\x10\x99\xde\x11\xa9\x12\xe3\xd3S'"


@app.route("/")
# ログイン成功後の画面(ホーム画面)
def top():
    message = 'ログインを成功しました＼(^o^)／'
    # セッション情報がなければログイン画面にリダイレクトする
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('index.html', message=message)


@app.route('/login', methods=["GET", "POST"])
# ログイン前画面　ログイン失敗時もここ
def login():
    if request.method == 'GET':
        # ログイン画面に遷移
        return render_template('login.html')

    # ログインフォームに入力されたユーザーIDとパスワードの取得
    id_name = request.form['id_name']
    password = request.form['password']
    debug_print(id_name)
    debug_print(password)

    # DB接続のための情報入力
    mysql_config = {
        'user': 'root',
        'password': 'hiya1023',
        'host': 'localhost',
        'port': 3306,
        'database': 'site_users'
    }
    # クラスをインスタンス化する
    db = MySQLConnector()
    # DB接続
    db.connect(mysql_config)
    debug_print("DB接続")

    # -- ユーザー名とパスワードのチェックはここに書く --
    # メッセージ初期化
    message = None

    # DBからID、ユーザーID、passwordを抽出する
    # フォームに入力されたIDはDBに存在するのか？
    db.execute(
        "SELECT password FROM site_users WHERE id_name = ?", (id_name,))
    # fetchone()で1件取り出し
    results = db.mysql_cursor.fetchone()

    # ユーザーIDがDB内にあれば、それぞれ変数に代入する
    if results is not None:
        # 抽出したレコードのpassword
        result_password = results[0]
    else:
        message = 'ログイン失敗：ユーザーIDとパスワードが正しくありません'
        # DB切断する
        db.disconnect()
        return render_template('login.html', message=message)

    debug_print(result_password)

    # ここでpasswordの照合して合わなければログイン失敗
    if not check_password_hash(result_password, password):
        message = 'ログイン失敗：パスワードが正しくありません'
        debug_print("NG_pass")
        # DB切断する
        db.disconnect()
        return render_template('login.html', message=message)

    # DB切断する
    db.disconnect()

    # セッション初期化
    session.clear()
    # ToDo: result_idの処理
    # セッションにログインIDを追加する
    session['id_name'] = result_id

    debug_print(type(session['id_name']))
    debug_print("OK")
    # ログイン後のページへリダイレクト
    return redirect(url_for('top'))


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
