from flask import Flask, redirect, render_template, request, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from functools import wraps


# MySQLに接続・切断を行うクラス
class MySQLConnector:
    def __init__(self):
        # MySQLのコネクタ
        self.__mysql_connection = None
        # MySQLのカーソル
        self.mysql_cursor = None

    # DBに接続する。
    # config: DB接続情報
    # 例
    # config = {
    #    'user': 'root',
    #    'password': 'hiya1023',
    #    'host': 'localhost',
    #    'port': 3306,
    #    'charset': 'utf8',
    #    'database': 'tables'
    # }
    def connect(self, connect_config: dict):
        # 二重接続回避
        self.disconnect()
        # SQLに接続します。
        self.__mysql_connection = mysql.connector.connect(**connect_config)
        # カーソルを取得する。
        # オプションは今後必要なら引数化してもいいかも？
        self.mysql_cursor = self.__mysql_connection.cursor(prepared=True)

    # DB切断する。
    def disconnect(self):
        # MySQLのカーソル切断
        if self.mysql_cursor is not None:
            self.mysql_cursor.close()
            self.mysql_cursor = None
        # MySQLのコネクトの切断
        if self.__mysql_connection is not None:
            self.__mysql_connection.close()
            self.__mysql_connection = None

    # SQL実行
    # sql:sql文を入れる。
    #     （例）"SELECT id,password FROM site_users WHERE id_name = ?"
    # param：paramには、sqlとして渡したSQL文の"?"に入るそれぞれの値をtupleにして渡す。
    #     （例）db.execute("SELECT id,password FROM site_users WHERE id_name = ?",("hoge"))
    def execute(self, sql: str, param: tuple = None):
        return self.mysql_cursor.execute(sql, param)

    # SQLを実行してfetchone()した結果であるtupleが返る。
    # 該当レコードがない場合はNoneが返る。
    # sql:sql文を入れる。
    #     （例）"SELECT id,password FROM site_users WHERE id_name = ?"
    # param：paramには、sqlとして渡したSQL文の"?"に入るそれぞれの値をtupleにして渡す。
    #     （例）db.execute_fetchone("SELECT id,password FROM site_users WHERE id_name = ?",("hoge"))
    def execute_fetchone(self, sql: str, param: tuple = None) -> tuple:
        self.execute(sql, param)
        return self.mysql_cursor.fetchone()


# MySQLConnectorのadaptor
class MySQLAdapter(MySQLConnector):
    def __enter__(self):
        # DB接続のための情報入力
        connect_config = {
            'user': 'root',
            'password': 'hiya1023',
            'host': 'localhost',
            'port': 3306,
            'charset': 'utf8',
            'database': 'tables'
        }
        self.connect(connect_config)
        return self

    def __exit__(self, ex_type, ex_value, tb):
        self.disconnect()


app = Flask(__name__)

# シークレットキーの設定
app.config[
    "SECRET_KEY"] = "b't\xd7.\xedOa\xd8\x88\x18\xc51H\xf5\x0b\xb1\x10\x99\xde\x11\xa9\x12\xe3\xd3S'"


# ログインチェック関数
def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        # セッション情報がなければログイン画面にリダイレクトする。
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
    # ログイン画面に表示している。
    return render_template('login.html')


@app.route('/login', methods=['POST'])
# ログイン処理
def login():
    # ユーザーID取得のための変数初期化
    id_name = ""
    # パスワード取得のための変数初期化
    password = ""

    with MySQLAdapter() as db:
        # ログインフォームに入力されたユーザーID取得
        id_name = request.form['id_name']

        # ログインフォームに入力されたパスワードの取得
        password = request.form['password']

        # DBからid_nameに対応するpasswordを取得する。
        result = db.execute_fetchone(
            "SELECT password FROM site_users WHERE id_name = ?", (id_name, ))

        # ユーザーIDがDB内に存在し、フォームから入力されたパスワードがDB内のものと一致すれば
        # セッションを登録する
        LoginOk = result is not None and check_password_hash(
            result[0], password)
        session['logged_in'] = LoginOk

        if not LoginOk:
            flash('ログイン失敗：ユーザーIDもしくはパスワードが正しくありません。')

        # セッションがTrueであれば、ログイン後のページへリダイレクトする。
        # セッションがFalseであれば、ログイン前のページにリダイレクトする。
        return redirect(url_for('top' if LoginOk else 'login'))


@app.route("/logout", methods=["GET"])
# ログアウト処理
def logout():
    # セッション情報をクリアにする。
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="10.22.0.47", port=80, debug=True)
