from flask import Flask, redirect, render_template, request, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from functools import wraps


# DB接続・切断に関するクラス
class MySQLConnector:
    def __init__(self):
        debug_print("initです")
        # コネクタの初期化
        self.mysql_connection = None
        # カーソルの初期化
        self.mysql_cursor = None

    # DB接続
    # config: DB接続情報
    def connect(self, connect_config: dict):
        debug_print("connectです")
        # 二重接続回避
        self.disconnect()
        # SQLに接続します
        self.mysql_connection = mysql.connector.connect(**connect_config)
        # カーソルを取得する
        # オプションは今後必要なら引数化してもいいかも？
        self.mysql_cursor = self.mysql_connection.cursor(prepared=True)
        debug_print(self.mysql_cursor)
        debug_print("connect抜けます")

    # DB切断
    def disconnect(self):
        debug_print("disconnectです")
        # カーソルとコネクトの切断
        if self.mysql_cursor is not None:
            self.mysql_cursor.close()
            self.mysql_cursor = None
        if self.mysql_connection is not None:
            self.mysql_connection.close()
            self.mysql_connection = None

    # SQL実行
    # sql:sql文を入れる
    #     （例）"SELECT id,password FROM site_users WHERE id_name = ?"
    # param：paramには、sqlとして渡したSQL文の"?"に入るそれぞれの値をtupleにして渡す。
    #     （例）db.execute("SELECT id,password FROM site_users WHERE id_name = ?",("hoge"))
    def execute(sql: str, param: tuple = None):
        debug_print("executeです")
        return self.mysql_cursor.execute(sql, param)

    # executeしたものをfetchoneする
    # sql:sql文を入れる
    #     （例）"SELECT id,password FROM site_users WHERE id_name = ?"
    # param：paramには、sqlとして渡したSQL文の"?"に入るそれぞれの値をtupleにして渡す。
    #     （例）db.execute_fetchone("SELECT id,password FROM site_users WHERE id_name = ?",("hoge"))
    def execute_fetchone(sql: str, param: tuple = None) -> tuple:
        debug_print("execute_fetchoneです")
        # self.execute(sql, param)
        self.mysql_cursor.execute(sql, param)
        return self.mysql_cursor.fetchone()


class MyConnector(MySQLConnector):
    def __enter__(self):
        debug_print("enterです")
        # DB接続のための情報入力
        connect_config = {
            'user': 'root',
            'password': 'hiya1023',
            'host': 'localhost',
            'port': 3306,
            'database': 'site_users'
        }
        self.connect(connect_config)

    def __exit__(self, ex_type, ex_value, tb):
        debug_print("exitです")
        self.disconnect()


app = Flask(__name__)

# シークレットキーの設定
app.config["SECRET_KEY"] = "b't\xd7.\xedOa\xd8\x88\x18\xc51H\xf5\x0b\xb1\x10\x99\xde\x11\xa9\x12\xe3\xd3S'"


# ログインチェック関数
def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        # セッション情報がなければログイン画面にリダイレクトする
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return inner


@app.route("/")
@login_required
# ログイン成功後の画面(ホーム画面)
def top():
    flash('ログインを成功しました＼(^o^)／')
    return render_template('index.html')


@app.route('/login', methods=['GET'])
# ログイン前画面表示
def login_view():
    # ログイン画面に表示している
    return render_template('login.html')


@app.route('/login', methods=['POST'])
# ログイン処理
def login():
    with MyConnector() as db:
        debug_print("With実行です")
        # ログインフォームに入力されたユーザーID取得
        id_name = request.form['id_name']
        debug_print(id_name)
        # ログインフォームに入力されたパスワードの取得
        password = request.form['password']
        debug_print(password)
        # DBからヒットしたid_nameからpasswordを抽出する
        # debug_print(self.mysql_cursor)
        result = mysql_cursor.execute_fetchone(
            "SELECT password FROM site_users WHERE id_name = ?", (id_name,))
        debug_print('---------------')
        debug_print(result)
        # ユーザーIDがDB内にあれば、それぞれ変数に代入する
        if result is None:
            flash('ログイン失敗：ユーザーIDとパスワードが正しくありません')
            return redirect(url_for('login'))
        # 抽出したレコードのpassword
        result_password = result[0]
        # ここでpasswordの照合して合わなければログイン失敗
        if not check_password_hash(result_password, password):
            flash('ログイン失敗：パスワードが正しくありません')
            return redirect(url_for('login'))
        # セッション初期化
        session.clear()
        # セッションに登録する
        session['logged_in'] = True
        # ログイン後のページへリダイレクト
        return redirect(url_for('top'))


@app.route("/logout", methods=["GET"])
# ログアウト処理
def logout():
    # セッション情報をカラにする
    session.clear()
    return redirect(url_for('login'))


# デバッグ用の文字を出力する
# s:文字列
def debug_print(s):
    if True:
        print(s)


if __name__ == "__main__":
    app.run(debug=True)
