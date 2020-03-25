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

    # SQLを実行してfetchall()した結果であるList[DBRecord]型が返る。
    # 該当レコードがない場合はNoneが返る。
    # t：取得したいデータがあるテーブルの一つのrecordを表現する構造体のクラス型を入れる。
    # sql：条件部分のみのSQLを入れる。デフォルトは""。
    # （例）"WHERE id = ?"
    # param：paramには、sqlとして渡したSQL文の"?"に入るそれぞれの値をtupleにして渡す。
    # 返し値：List[DBRecord]型が返る。
    # （使用例）
    # entries = db.select(Entry)
    # List[DBRecord]
    def select(self, t: type, sql: str = "", param=()) -> list:
        sql = f"SELECT {t.sql_select_statement} FROM {t.table_name} {sql}"
        self.execute(sql, param)
        return t.from_tuple_of_tuples(self.mysql_cursor.fetchall())

    # SQLを実行してfetchone()した結果であるtuple型が返る。
    # 該当レコードがない場合はNoneが返る。
    # t：取得したいデータがあるテーブルの一つのrecordを表現する構造体のクラス型を入れる。
    # sql：条件部分のみのSQLを入れる。デフォルトは""。
    # param：paramには、sqlとして渡したSQL文の"?"に入るそれぞれの値をtupleにして渡す。
    # 返し値：tuple型が返る。
    # （使用例）
    # entry = db.select_one(Entry,"WHERE id = ?", id)
    def select_one(self, t: type, sql: str = "", param=()) -> tuple:
        sql = f"SELECT {t.sql_select_statement} FROM {t.table_name} {sql}"
        self.execute(sql, str(param))
        return t.from_tuple(self.mysql_cursor.fetchone(), t.sql_select_statement.split(","))


# MySQLConnectorのadaptor
class MySQLAdapter(MySQLConnector):
    def __enter__(self):

        # DB接続のための情報入力configをjson形式で読み込む。
        self.connect(ReadJsonFromFile('exclude/connect_config.json'))

        return self

    def __exit__(self, ex_type, ex_value, tb):
        self.disconnect()


# DBのテーブルを表現するクラスの基底クラス
class DBTable():

    # columns と column_names から要素をひとつずつ取り出して、それを record型オブジェクトとして、
    # setattr を適用してList化する関数
    # columns：tuple , カラムの値が格納されている。
    # 返し値：
    # （使用例）
    # list(map(cls.from_tuple, entries))
    @classmethod
    def from_tuple(cls, columns: tuple, column_names: List[str]):
            # ->Entry ※エラーのためコメントにする

        # 引数のクラス型をオブジェクト化する。
        record = (cls)()

        # sql_select_statement から "," くぎりで column_names に格納する。
        #column_names = cls.sql_select_statement.split(",")

        # テーブルに定義しているカラム数だけ回す。
        # for i in range(len(column_names)):
        #     # column_names から要素（カラム名）をひとつずつ取り出して入れる変数
        #     name = column_names[i]
        #     # columns から要素（値）をひとつずつ取り出して入れる変数
        #     value = columns[i]
        #     # nameとvalueに対してrecordにsetattr(name,value)する。
        #     setattr(record, name, value)
        for name, value in zip(column_names, columns):
            setattr(record, name, value)

        return record

    # Tuple[tuple]型の値 を List[DBRecord]型の値に変換する。
    # entries：Tuple[tuple]型の値（（例）((1,'abc),(2,'def)) ）を入れる。
    # 返し値：Tuple[tuple]型 から List[Entry]型 に変換して返す。
    # （使用例）
    # entries_ = db.select(Entry, "SELECT id, comment FROM todo_items")
    # entries = Entry.from_tuple_of_tuples(entries_)
    @classmethod
    def from_tuple_of_tuples(cls, entries: Tuple[tuple]) -> list:
        # -> List[DBTable]

        return list(map(cls.from_tuple, entries))


# DBのTODO_ITEMSテーブルの一つのrecordを表現する構造体
class ToDoItem(DBTable):

    # TODO_ITEMSテーブルの名前
    table_name = "todo_items"

    # TODO_ITEMSテーブルの各フォールド名
    sql_select_statement = "id,comment"


# DBのSITE_USERSテーブルの一つのrecordを表現する構造体
class SiteUser(DBTable):

    # SITE_USERSテーブルの名前
    table_name = "site_users"

    # SITE_USERSテーブルの各フォールド名
    sql_select_statement = "id,id_name,password"


app = FlaskBuilder(__name__)


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

    with MySQLAdapter() as db:
        return render_template('index.html', entries=db.select(ToDoItem))


# ログイン前画面表示
@app.route('/login', methods=['GET'])
def login_view():

    # ログイン画面に表示する。
    return render_template('login.html')


# ログイン処理
@app.route('/login', methods=['POST'])
def login():

    with MySQLAdapter() as db:

        # ログインフォームに入力されたユーザーIDとパスワード取得
        id_name, password = request_form('id_name', 'password')

        # DBからid_nameに対応するpasswordを取得する。
        site_user = db.select_one(SiteUser, "WHERE id_name = ?", id_name)

        # ユーザーIDがDB内に存在し、フォームから入力されたパスワードがDB内のものと一致すれば
        # セッションを登録する
        LoginOk = site_user is not None and check_password_hash(
            site_user.password, password)
        app.login(LoginOk)

        if not LoginOk:
            flash('ログイン失敗：ユーザーIDもしくはパスワードが正しくありません。')

        # session['logged_in']がTrueであれば、(ログインに成功しているので)ログイン後のページへリダイレクトする。
        # session['logged_in']がFalseであれば、(ログインに失敗しているので)ログインページにリダイレクトする。(再度表示する)
        return redirect(url_for('top' if LoginOk else 'login'))


# ログアウト処理
@app.route("/logout", methods=["GET"])
def logout():

    app.logout()

    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
#    app.run(host="0.0.0.0", port=80, debug=False)
