from flask import Flask, redirect, render_template, request, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector


# DB接続・切断に関するクラス
class MySQLConnector:
    # コネクタとカーソルを初期化
    def __init__(self):
        # コネクタの初期化
        self.__mysql_connection = None
        # カーソルの初期化
        self.mysql_cursor = None

    # DB接続
    # config: DB接続情報
    def connect(self, mysql_config: dict):
        # 二重接続回避
        self.disconnect()
        # SQLに接続します
        self.__mysql_connection = mysql.connector.connect(**mysql_config)
        # カーソルを取得する
        # オプションは今後必要なら引数化してもいいかも？
        self.mysql_cursor = self.__mysql_connection.cursor(prepared=True)

    # DB切断
    def disconnect(self):
        # カーソルとコネクトの切断
        if self.mysql_cursor is not None:
            self.mysql_cursor.close()
            self.mysql_cursor = None
        if self.__mysql_connection is not None:
            self.__mysql_connection.close()
            self.__mysql_connection = None

    # SQL実行
    # sql:sql文を入れる
    #     （例）"SELECT id,password FROM site_users WHERE id_name = ?"
    # param：paramには、sqlとして渡したSQL文の"?"に入るそれぞれの値をtupleにして渡す。
    #     （例）db.execute("SELECT id,password FROM site_users WHERE id_name = ?",("hoge"))
    def execute(self, sql: str, param: tuple = None):
        return self.__mysql_connection.execute(sql, param)


class MyConnector(MySQLConnector):

    def __enter__(self):
        # DB接続のための情報入力
        connect_config = {
            'user': 'root',
            'password': 'hiya1023',
            'host': 'localhost',
            'port': 3306,
            'database': 'site_users'
        }
        debug_print('----www-----')
        self.connect(connect_config)

    def __exit__(self, ex, extype, tb):
        self.disconnect()

    def execute_fetchone(self, sql, param: tuple = None)->tuple:
        self.execute(sql, param)
        return self.mysql_cursor.fetchone()


app = Flask(__name__)

# シークレットキーの設定
app.config["SECRET_KEY"] = "b't\xd7.\xedOa\xd8\x88\x18\xc51H\xf5\x0b\xb1\x10\x99\xde\x11\xa9\x12\xe3\xd3S'"


@app.route("/")
# ログイン成功後の画面(ホーム画面)
def top():
    # セッション情報がなければログイン画面にリダイレクトする
    if not session.get('logged_in'):
        return redirect(url_for('login'))
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
    # with MyConnector() as db:
    # ログインフォームに入力されたユーザーID取得
    id_name = request.form['id_name']
    debug_print(id_name)
    # ログインフォームに入力されたパスワードの取得
    password = request.form['password']
    # mysql_config = {
    #     'user': 'root',
    #     'password': 'hiya1023',
    #     'host': 'localhost',
    #     'port': 3306,
    #     'database': 'site_users'
    # }
    # # クラスをインスタンス化する
    db = MyConnector()
    # DB接続
    # db.connect(mysql_config)
    # DBからヒットしたid_nameからpasswordを抽出する
    result = db.execute_fetchone(
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
