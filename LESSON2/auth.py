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

        # MySQLConnectorはデフォルトでは更新系のSQL文の発行後にcommit()が必要になるのでAutoCommitをTrueに変更しておく。
        self.__mysql_connection.autocommit = True

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

    # SQLを実行してfetchall()した結果であるtupleが返る。
    # 該当レコードがない場合はNoneが返る。
    # sql:sql文を入れる。
    #     （例）"SELECT id,password FROM site_users WHERE id_name = ?"
    # param：paramには、sqlとして渡したSQL文の"?"に入るそれぞれの値をtupleにして渡す。
    #     （例）db.execute_fetchall("SELECT id,password FROM site_users WHERE id_name = ?",("hoge"))
    def execute_fetchall(self, sql: str, param: tuple = None) -> tuple:
        self.execute(sql, param)
        return self.mysql_cursor.fetchall()


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
with open('skey.cfg', 'r') as secret_key_file:
    app.config["SECRET_KEY"] = str(secret_key_file)


# ログインチェック関数
def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        # セッション情報がなければログイン画面にリダイレクトする。
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(*args, **kwargs)

    return inner


# ToDoリストで追加されたコメントをDBに登録する。
@app.route('/', methods=['POST'])
@login_required
def add_todo_items():

    # 入力がなければ何もしないで load_todo_items関数 読み込み。
    if request.form.get('comment') == "":
        return load_todo_items()

    with MySQLAdapter() as db:

        # ToDoフォームに入力されたコメント取得
        comment = request.form.get('comment')
        # コメントをDBに登録する。
        db.execute(
            "INSERT INTO todo_items (comment) VALUES (?)", (comment,))

    return load_todo_items()


# ToDoリストで追加されたコメントをDBから取り出す。
@app.route('/')
@login_required
def load_todo_items():
    with MySQLAdapter() as db:

        # DBに登録されているコメントをすべて取り出し entries に入れる。
        entries = db.execute_fetchall(
            "SELECT * FROM todo_items", ())

    return render_template('/index.html', entries=entries)


# ToDoリストに追加されたコメントをDBから削除する。
# id : 削除するコメントのid
@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_todo_items(id):

    flash('削除しました＼(^o^)／')

    with MySQLAdapter() as db:

       # 任意のidのコメントをDBから削除する。
        db.execute(
            "DELETE FROM todo_items WHERE id = ?", (id,))

    return redirect(url_for('load_todo_items'))


# データベース内のToDoリストをすべて削除する。
@app.route('/all-delete', methods=['POST'])
@login_required
def all_delete_todo_items():

    flash('全部削除しました＼(^o^)／ｵﾜｯﾀ')

    with MySQLAdapter() as db:

        # ToDoリストをすべて削除する。
        db.execute(
            "DELETE FROM todo_items", ())

    return redirect(url_for('load_todo_items'))


@app.route('/')
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

        # session['logged_in']がTrueであれば、(ログインに成功しているので)ログイン後のページへリダイレクトする。
        # session['logged_in']がFalseであれば、(ログインに失敗しているので)ログインページにリダイレクトする。(再度表示する)
        return redirect(url_for('top' if LoginOk else 'login'))


@app.route("/logout", methods=["GET"])
# ログアウト処理
def logout():

    # セッション情報をクリアにする。
    session.clear()

    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
#    app.run(host="0.0.0.0", port=80, debug=False)
