from HiyaLib import *


# DBのテーブルを表現するクラスの基底クラス
class DBTable():

    # columns と column_names から要素をひとつずつ取り出したのがvalue , nameとして、
    # それを 生成したDBTable派生型のオブジェクトに setattr(object,name,value)する。
    # columns：カラムの値が格納されている。
    # column_names：カラム名が格納されている。
    # 返し値：recordオブジェクトに name属性に value を追加したものを返す。
    # （使用例）
    # t.from_tuple(self.mysql_cursor.fetchone(), t.sql_select_statement.split(","))
    # (必要性)　
    @classmethod
    def from_tuple(cls, columns: Tuple[Tuple], column_names: List[str]) -> "DBTable":

        # DBTable派生クラスのインスタンスを作成する。
        record = (cls)()

        # column_names と columns から要素をひとつずつ取り出して
        # name と value に入れる。
        # nameとvalueに対して、recordオブジェクトに name属性に value を追加する。
        for name, value in zip(column_names, columns):
            setattr(record, name, value)

        return record

    # Tuple[tuple]型の値 を List[map]型の値に変換する。
    # columns：Tuple[tuple]型の値（（例）((1,'abc),(2,'def)) ）を入れる。
    # 返し値：Tuple[tuple]型 から List[map]型 に変換して返す。
    # （使用例）
    # t.from_tuple_of_tuples(self.mysql_cursor.fetchall())
    # (必要性)　
    @classmethod
    def from_tuple_of_tuples(cls, columns: Tuple[tuple]) -> "List[map]":

        t = cls.sql_select_statement.split(",")

        return list(map(lambda x: cls.from_tuple(x, t), columns))


# DBのTODO_ITEMSテーブルの一つのrecordを表現する構造体
class ToDoItem(DBTable):

    # TODO_ITEMSテーブルの名前
    table_name = "todo_items"

    # TODO_ITEMSテーブルの各フィールド名
    sql_select_statement = "id,comment"

    # TODO_ITEMSテーブルのprimary key設定
    orm_primary_key = "id"

    def __init__(self):

        # auto_increment , primary
        self.id = -1

        # ここにToDoの内容が入っている
        self.comment = ""


# DBのSITE_USERSテーブルの一つのrecordを表現する構造体
class SiteUser(DBTable):

    # SITE_USERSテーブルの名前
    table_name = "site_users"

    # SITE_USERSテーブルの各フィールド名
    sql_select_statement = "id,id_name,password"

    # SITE_USERSテーブルのprimary key設定
    orm_primary_key = "id"

    def __init__(self):

        # auto_increment , primary
        self.id = -1

        # ここにユーザーIDの内容が入っている
        self.id_name = ""

        # ここにパスワードの内容が入っている
        self.password = ""


# MySQLに接続・切断を行うクラス
class MySQLConnector:
    def __init__(self):
        # MySQLのコネクタ
        self.__mysql_connection = None
        # MySQLのカーソル
        self.mysql_cursor = None

    def __enter__(self):

        # DB接続のための情報入力configをjson形式で読み込む。
        self.connect(ReadJsonFromFile('exclude/connect_config.json'))

        return self

    def __exit__(self, ex_type, ex_value, tb):
        self.disconnect()

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

    # SQLを実行してfetchall()した結果である List[DBTable]型 が返る。
    # 該当レコードがない場合は None が返る。[ToDo:ほんまか？]
    # t：取得したいデータがあるテーブルの一つのrecordを表現する構造体のクラス型を入れる。
    # sql_where：条件部分のみの SQL を入れる。デフォルトは""。
    # （例）"WHERE id = ?"
    # param：paramには、sql として渡したSQL文の "?" に入るそれぞれの値を tuple にして渡す。
    # 返し値：List[DBTable]型 が返る。
    # （使用例）
    # entries = db.select(Entry)
    def select(self, t: type, sql_where: str = "", param=()) -> "List[DBTable]":

        self.execute(power_join(
            [f"SELECT {t.sql_select_statement} FROM {t.table_name}", sql_where]), param)
        return t.from_tuple_of_tuples(self.mysql_cursor.fetchall())

    # SQLを実行して fetchone() した結果である tuple型 が返る。
    # 該当レコードがない場合は None が返る。[ToDo:ほんまか？]
    # t：取得したいデータがあるテーブルの一つのrecordを表現する構造体のクラス型を入れる。
    # sql_where：条件部分のみの SQL を入れる。デフォルトは "" 。
    # param：paramには、sql として渡したSQL文の "?" に入るそれぞれの値を tuple にして渡す。
    # 返し値：tuple型が返る。
    # （使用例）
    # result = db.select_one(SiteUser,"WHERE id = ?", id)
    def select_one(self, t: type, sql_where: str = "", param=()) -> tuple:

        self.execute(power_join(
            [f"SELECT {t.sql_select_statement} FROM {t.table_name}", sql_where]), param)
        return t.from_tuple(self.mysql_cursor.fetchone(), t.sql_select_statement.split(","))

    # DELETEを実行する関数
    # 該当レコードがない場合は None が返る。
    # t：取得したいデータがあるテーブルの一つのrecordを表現する構造体のクラス型を入れる。
    # （使用例）
    # db.delete(ToDoItem)
    def delete(self, t: DBTable):

        primary_key = t.orm_primary_key

        sql = [f"DELETE FROM {t.table_name}", f"WHERE {primary_key} = ?"]

        return self.execute(power_join(sql), getattr(t, primary_key))

    # UPDATEを実行する関数
    # 該当レコードがない場合は None が返る。[ToDo:ほんまか？]
    # t：取得したいデータがあるテーブルの一つのrecordを表現する構造体のクラス型を入れる。
    # sql_set：アップデート対象の部分のみ SQL を入れる。デフォルトは""。（記入例）"SET id=?"
    # sql_where：検索条件部分のみの SQL を入れる。デフォルトは""。（記入例）"WHERE id=3"
    # （例）" WHERE id = ?"
    # param：paramには、sql として渡したSQL文の "?" に入るそれぞれの値を tuple にして渡す。
    # 返し値：
    # （使用例）
    # db.update(SiteUser,"SET id=?, comment=?","WHERE id=3", comment)
    def update(self, t: type, sql_set: str = "", sql_where: str = "", param=()):

        sql = [f"UPDATE {t.table_name}", sql_set, sql_where]

        return self.execute(power_join(sql), param)

    # INSERTを実行する関数
    # 該当レコードがない場合は None が返る。[ToDo:ほんまか？]
    # t：取得したいデータがあるテーブルの一つのrecordを表現する構造体のクラス型を入れる。
    # sql_where：条件部分のみの SQL を入れる。デフォルトは""。
    # （例）"VALUES (?)"
    # param：paramには、sql として渡したSQL文の "?" に入るそれぞれの値を tuple にして渡す。
    # 返し値：
    # （使用例）
    # db.insert(SiteUser,"VALUES (?)", comment)
    # def insert(self, t: type, sql_where: str = "", param=()):

    #     sql = [
    #         f"INSERT INTO {t.table_name} ({t.sql_select_statement})", sql_where]

    #     return self.execute(power_join(sql), param)


app = FlaskBuilder(__name__)


# ToDoリストで追加されたコメントをDBに登録する。
@app.route('/add', methods=['POST'])
@login_required
def add_todo_item():

    # ToDoフォームのテキストボックスに入力されたテキストを取得する。
    comment = request_form('comment')

    # コメント欄のテキストボックスが空でなければ、SQLを実行する。
    # コメント欄のテキストボックスが空なら何もしない。
    if comment:
        with MySQLConnector() as db:

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

    with MySQLConnector() as db:

        todo_item = db.select_one(
            ToDoItem, "WHERE id = ?", id) if id else None

        db.delete(todo_item)

    flash('削除しました＼(^o^)／')

    return redirect(url_for('top'))


# DB内のToDoリストをすべて削除する。
@app.route('/all-delete', methods=['POST'])
@login_required
def all_delete_todo_items():

    with MySQLConnector() as db:

        # ToDoリストをすべて削除する。
        db.execute("DELETE FROM todo_items")

    flash('全部削除しました＼(^o^)／ｵﾜｯﾀ')

    return redirect(url_for('top'))


# ログイン成功後の画面(ホーム画面)
@app.route('/')
@login_required
def top():

    flash('ログインを成功しました＼(^o^)／')

    with MySQLConnector() as db:
        return render_template('index.html', entries=db.select(ToDoItem))


# ログイン前画面表示
@app.route('/login', methods=['GET'])
def login_view():

    # ログイン画面に表示する。
    return render_template('login.html')


# ログイン処理
@app.route('/login', methods=['POST'])
def login():

    with MySQLConnector() as db:

        # ログインフォームに入力されたユーザーIDとパスワード取得
        id_name, password = request_form('id_name', 'password')

        # ログインフォームに入力されたユーザーIDをパラメーターに、select_one関数で
        # DBのテーブルクラスを入れ、fetchoneをして、値を抽出する。
        # ただし、ログインフォームに入力されたユーザーIDが空のときは、Noneを返す。
        site_user = db.select_one(
            SiteUser, "WHERE id_name = ?", id_name) if id_name else None

        # ユーザーIDがDB内に存在し、フォームから入力されたパスワードがDB内のものと一致すれば
        # セッションを登録する
        LoginOk = site_user is not None and check_password_hash(
            site_user.password, password)
        app.login(LoginOk)

        if not LoginOk:
            flash('ログイン失敗：ユーザーIDもしくはパスワードが正しくありません。')

        # ログインに成功していれば、ログイン後のページへリダイレクトする。
        # ログインに失敗していれば、ログインページにリダイレクトする。(再度表示する)
        return redirect(url_for('top' if LoginOk else 'login'))


# ログアウト処理
@app.route("/logout", methods=["GET"])
def logout():

    app.logout()

    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
#    app.run(host="0.0.0.0", port=80, debug=False)
