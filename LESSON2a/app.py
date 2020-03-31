from HiyaLib import *
import unittest


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

    # TODO_ITEMSテーブルのupdateカラムを設定
    orm_update_str = "comment=?"

    # TODO_ITEMSテーブルのinsertカラムの値を設定
    orm_insert_value = "?"

    # TODO_ITEMSテーブルのカラム名をlist設定
    orm_insert_colum = "id, comment"

    # TODO_ITEMSテーブルのカラム名をlistで設定
    orm_column_names = ["id", "comment"]

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

    # SITE_USERSテーブルのupdateカラムを設定
    orm_update_str = "id_name=?,password=?"

    # SITE_USERSテーブルのinsertカラムの値を設定
    orm_insert_value = "?,?"

    # SITE_USERSテーブルのinsertカラム名を設定
    orm_insert_colum = "id_name, password"

    # SITE_USERSテーブルのカラム名をlistで設定
    orm_column_names = ["id", "id_name", "password"]

    def __init__(self):

        # auto_increment , primary
        self.id = -1

        # ここにユーザーIDの内容が入っている
        self.id_name = ""

        # ここにパスワードの内容が入っている
        self.password = ""


# unittest用テーブル
# DBのTEST_TABLEの一つのrecordを表現する構造体
class TestTable(DBTable):

    # TEST_TABLEの名前
    table_name = "test_tables"

    # TEST_TABLEの各フィールド名
    sql_select_statement = "id,comment"

    # TEST_TABLEのprimary key設定
    orm_primary_key = "id"

    # TEST_TABLEのupdateカラムを設定
    orm_update_str = "comment=?"

    # TEST_TABLEのinsertカラムの値を設定
    orm_insert_value = "?"

    # TEST_TABLEのカラム名をlistで設定
    orm_insert_colum = "id, comment"

    # TEST_TABLEのカラム名をlistで設定
    orm_column_names = ["id", "comment"]

    def __init__(self):

        # auto_increment , primary
        self.id = -1

        # ここにTestcommentの内容が入っている
        self.comment = ""


# unittest用テーブル
# DBのTEST_TABLEテーブルの一つのrecordを表現する構造体
class TestTable2(DBTable):

    # TEST_TABLEの名前
    table_name = "test_tables2"

    # TEST_TABLEの各フィールド名
    sql_select_statement = "id,id_name,password"

    # TEST_TABLEのprimary key設定
    orm_primary_key = "id"

    # TEST_TABLEのupdateカラムを設定
    orm_update_str = "id_name=?,password=?"

    # TEST_TABLEのinsertカラムの値を設定
    orm_insert_value = "?,?"

    # TEST_TABLEのカラム名をlistで設定
    orm_insert_colum = "id_name, password"

    # TEST_TABLEのカラム名をlistで設定
    orm_column_names = ["id", "id_name", "password"]

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
    # 　 または、クラスのオブジェクト DBTable を入れる。
    # （使用例）
    # ※DBTable型のとき
    # 　db.delete(todo_item)
    # ※ToDoItemクラス型のとき
    # 　db.delete(ToDoItem)
    # (必要性)　ToDoリストの個別削除と全件削除を実現したいため作成。個別削除では、DBTableを引数に取るが、
    # 全件削除では、ToDoItemクラス型を使う。Pythonでは、異なる型を引数にとってもコンパイル時にチェックされていないので
    # 関数内で処理することにする。
    def delete(self, t):

        # t が type型 のときは、全件削除する。
        if type(t) is type:
            return self.execute(f"DELETE FROM {t.table_name}", param=())

        primary_key = t.orm_primary_key

        return self.execute(power_join([f"DELETE FROM {t.table_name}", f"WHERE {primary_key} = ?"]), getattr(t, primary_key))

    # UPDATEを実行する関数
    # 該当レコードがない場合は None が返る。
    # t：取得したいデータがあるテーブルの一つのrecordを表現する構造体のクラス型を入れる。
    # param：paramには、sql として渡したSQL文の "?" に入るそれぞれの値を tuple にして渡す。
    #        ※更新データの書き方として最後にprimary keyの値を書くこと。
    # （使用例）
    # db.update(ToDoItem, ('数学', 1))
    def update(self, t: type, update_param: tuple):

        # updateカラム取得
        update_strs = t.orm_update_str

        # primary_key を取得
        primary_key = t.orm_primary_key

        return self.execute(power_join([f"UPDATE {t.table_name} SET {update_strs} WHERE {primary_key} = ?"]), tuple(param))

    # INSERTを実行する関数
    # 該当レコードがない場合は None が返る。
    # t：取得したいデータがあるテーブルの一つのrecordを表現する構造体のクラス型を入れる。
    # param：paramには、sql として渡したSQL文の VALUE(?) に入るそれぞれの値を tuple にして渡す。
    # （使用例）
    # db.insert(ToDoItem, '数学')
    def insert(self, t: type, param: tuple):

        # insert対象のカラム取得
        insert_colum = t.orm_insert_colum

        # insert対象の値（"?"で表す）を取得
        insert_value = t.orm_insert_value

        return self.execute(power_join([f"INSERT INTO {t.table_name} ({insert_colum}) VALUES ({insert_value})"]), param)


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
            db.insert(ToDoItem, comment)

    return redirect(url_for('top'))


# ToDoリストに追加されたコメントをDBから1件だけ削除する。
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
        db.delete(ToDoItem)

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


# unittest.TestCaseの子クラス
class App_Test(unittest.TestCase):

    # update関数のunitテスト
    def test_update(self):
        # ここにテスト項目を書いていく。
        test_table = ('算数', 1)

        with MySQLConnector() as db:

            db.update(TestTable, test_table)

    # insert関数のunitテスト
    def test_insert(self):
        # ここにテスト項目を書いていく。
        with MySQLConnector() as db:

            # コメントをDBに登録する。
            db.insert(TestTable2, ('yama', '838861'))


if __name__ == "__main__":
    #    app.run(port=5000, debug=True)
    #    app.run(host="0.0.0.0", port=80, debug=False)
    unittest.main()
