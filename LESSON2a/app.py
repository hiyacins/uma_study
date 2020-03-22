from HiyaLib import *


# MySQLに接続・切断を行うクラス
class MySQLConnector:
    def __init__(self):
        # MySQLのコネクタ
        self.__mysql_connection = None
        # MySQLのカーソル
        self.mysql_cursor = None

    # dict型で接続情報を渡す。
    # config: DB接続情報
    # 例
    # config = {
    #    'user': 'root',
    #    'password': '****',
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
    # sql:実行するSQL文を入れる。
    #     （例）"SELECT id FROM site_users WHERE id = ?"
    # param：paramには、sqlとして渡したSQL文の"?"に入る、それぞれの値をtupleにして渡す。
    #        paramがデフォルト値のときは、第2引数を省略する。
    #     （例1）db.execute("SELECT id FROM site_users WHERE id = ?", id)
    #     （例2）db.execute("SELECT id FROM site_users")
    def execute(self, sql: str, param=()):

        # param が tuple以外のstr,intなどのとき、paramをtupleでくるむ(tupleの１つ目の要素がparamであるtuple化する)。
        if not type(param) is tuple:
            param = (param,)
        return self.mysql_cursor.execute(sql, param)

    # SQLを実行してfetchone()した結果であるtupleが返る。
    # 該当レコードがない場合はNoneが返る。
    # sql:sql文を入れる。
    #     （例）"SELECT id FROM site_users WHERE id = ?"
    # param：paramには、sqlとして渡したSQL文の"?"に入るそれぞれの値をtupleにして渡す。
    #     （例）db.execute_fetchone("SELECT id FROM site_users WHERE id = ?", id)
    # 返し値：
    def execute_fetchone(self, sql: str, param=()) -> tuple:
        self.execute(sql, param)
        return self.mysql_cursor.fetchone()

    # SQLを実行してfetchall()した結果であるTuple[Tuple]型が返る。
    # 該当レコードがない場合はNoneが返る。
    # sql:sql文を入れる。
    #     （例）"SELECT id,password FROM site_users WHERE id_name = ?"
    # param：paramには、sqlとして渡したSQL文の"?"に入るそれぞれの値をtupleにして渡す。
    #     （例）db.execute_fetchall("SELECT id,password FROM site_users WHERE id_name = ?","hoge")
    # 返し値：
    def execute_fetchall(self, sql: str, param=()) -> Tuple[Tuple]:
        self.execute(sql, param)
        return self.mysql_cursor.fetchall()

    #
    def select(self, t: type, sql: str, param=()) -> list:  # List[DBRecord]
        self.execute(sql, param)
        elements = self.mysql_cursor.fetchall()
        return t.from_tuple_of_tuples(elements)


# MySQLConnectorのadaptor
class MySQLAdapter(MySQLConnector):
    def __enter__(self):

        # DB接続のための情報入力configをjson形式で読み込む。
        self.connect(ReadJsonFromFile('exclude/connect_config.json'))

        return self

    def __exit__(self, ex_type, ex_value, tb):
        self.disconnect()


# Tuple[Tuple]型からList[DBRecord]型に変換するためのクラス
class DBRecord():
    def __init__(self, id: int, comment: str):
        # id : int
        # auto incremental id
        self.id = id

        # comment : str
        # ToDoの内容
        self.comment = comment

    # Tuple型の値 を DBRecord型の値に変換する。
    # entries_：Tuple型の値（（例）(1,'abc')）を入れる。
    # 返し値：Tuple型 から DBRecord型 に変換して返す。
    # （使用例）
    # entries.append(cls.from_tuple(entry))
    @classmethod
    def from_tuple(cls, entry: tuple):  # ->DBRecord ※エラーのためコメントにする

        return DBRecord(entry[0], entry[1])

    # Tuple[tuple]型の値 を List[DBRecord]型の値に変換する。
    # entries：Tuple[tuple]型の値（（例）((1,'abc),(2,'def)) ）を入れる。
    # 返し値：Tuple[tuple]型 から List[Entry]型 に変換して返す。
    # （使用例）
    # entries_ = db.select(Entry, "SELECT id, comment FROM todo_items")
    # entries = Entry.from_tuple_of_tuples(entries_)
    @classmethod
    def from_tuple_of_tuples(cls, entries: Tuple[tuple]) -> list:
        # -> List[DBRecord]

        return list(map(cls.from_tuple, entries))


# DBのTODO_ITEMSテーブルの一つのrecordを表現する構造体
class Entry(DBRecord):
    # def __init__(self, id: int, comment: str):
    #     # # id : int
    #     # # auto incremental id
    #     # self.id = id

    #     # # comment : str
    #     # # ToDoの内容
    #     # self.comment = comment
    pass


# ToDoリストで追加されたコメントをDBから取り出す。
def load_todo_items() -> List[Entry]:

    with MySQLAdapter() as db:

        # DBに登録されているコメントをすべて取り出し entries に入れる。
        entries = db.select(Entry, "SELECT id, comment FROM todo_items")

    return entries


app = Flask(__name__)


# シークレットキーの設定
with FileReader("exclude/secret_key.txt") as secret_key_file:
    app.config["SECRET_KEY"] = secret_key_file.readline().strip()


# ToDoリストで追加されたコメントをDBに登録する。
@app.route('/add', methods=['POST'])
@login_required
def add_todo_item():

    # ToDoフォームに入力されたcomment取得する。
    comment = request_form('comment')

    # commentに入力があればSQLを実行する。
    # commentに入力がなければ何もしないで load_todo_items関数 読み込み。
    if comment:
        with MySQLAdapter() as db:

            # コメントをDBに登録する。
            db.execute(
                "INSERT INTO todo_items (comment) VALUES (?)", comment)

    return redirect(url_for('top'))


# ToDoリストに追加されたコメントをDBから削除する。
# id : int
# 削除するコメントのid
@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_todo_item(id: int):

    with MySQLAdapter() as db:

        # 任意のidのコメントをDBから削除する。
        db.execute(
            "DELETE FROM todo_items WHERE id = ?", id)

    flash('削除しました＼(^o^)／')

    return redirect(url_for('top'))


# データベース内のToDoリストをすべて削除する。
@app.route('/all-delete', methods=['POST'])
@login_required
def all_delete_todo_items():

    with MySQLAdapter() as db:

        # ToDoリストをすべて削除する。
        db.execute("DELETE FROM todo_items")

    flash('全部削除しました＼(^o^)／ｵﾜｯﾀ')

    return redirect(url_for('top'))


# ログイン成功後の画面(ホーム画面)
@app.route('/')
@login_required
def top():

    flash('ログインを成功しました＼(^o^)／')

    entries = load_todo_items()

    return render_template('index.html', entries=entries)


# ログイン前画面表示
@app.route('/login', methods=['GET'])
def login_view():

    # ログイン画面に表示している。
    return render_template('login.html')


# ログイン処理
@app.route('/login', methods=['POST'])
def login():

    with MySQLAdapter() as db:
        # ログインフォームに入力されたユーザーID取得
        id_name = request_form('id_name')

        # ログインフォームに入力されたパスワードの取得
        password = request_form('password')

        # DBからid_nameに対応するpasswordを取得する。
        result = db.execute_fetchone(
            "SELECT password FROM site_users WHERE id_name = ?", id_name)

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


# ログアウト処理
@app.route("/logout", methods=["GET"])
def logout():

    # セッション情報をクリアにする。
    session.clear()

    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
#    app.run(host="0.0.0.0", port=80, debug=False)
