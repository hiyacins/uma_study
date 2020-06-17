# from flask import Flask, render_template
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
    # columns：Tuple[tuple]型の値（（例）((1,'abc'),(2,'def')) ）を入れる。
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

    # TODO_ITEMSテーブルのprimary key設定[ToDo:リスト化]
    orm_primary_key = "id"

    # TODO_ITEMSテーブルのupdateカラムを設定
    orm_update_str = "comment=?"

    # TODO_ITEMSテーブルのinsertカラムの値を設定
    orm_insert_value = "?"

    # TODO_ITEMSテーブルのカラム名を設定
    orm_insert_colum = "comment"

    # TODO_ITEMSテーブルのカラム名をlistで設定
    orm_column_names = ["id", "comment"]

    def __init__(self):

        # auto_increment , primary
        self.id = -1

        # ここにToDoの内容が入っている
        self.comment = ""

    # このオブジェクトをserializeする
    # (このオブジェクトをdict化して返す)
    def serialize(self):
        return {
            "id": self.id,
            "comment": self.comment
        }


# DBのSITE_USERSテーブルの一つのrecordを表現する構造体
class SiteUser(DBTable):

    # SITE_USERSテーブルの名前
    table_name = "site_users"

    # SITE_USERSテーブルの各フィールド名
    sql_select_statement = "id,id_name,password"

    # SITE_USERSテーブルのprimary key設定[ToDo:リスト化]
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

    # このオブジェクトをserializeする
    # (このオブジェクトをdict化して返す)
    def serialize(self):
        return {
            "id": self.id,
            "id_name": self.id_name,
            "password": self.password
        }


# unittest用テーブル
# DBのTEST_TABLEの一つのrecordを表現する構造体
class TestTable(DBTable):

    # TEST_TABLEの名前
    table_name = "test_tables"

    # TEST_TABLEの各フィールド名
    sql_select_statement = "id,comment"

    # TEST_TABLEのprimary key設定
    orm_primary_key = "id"

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
        if not ((type(param) is tuple) or (type(param) is list) or (type(param) is dict)):
            param = (param,)

        return self.mysql_cursor.execute(sql, param)

    # SQLを実行してfetchall()した結果である List[DBTable]型 が返る。
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

    # insert → update を行う時、insertで登録した、最後のidを取得する関数
    # 返し値：int型が返る。
    # （使用例）
    # id = db.select_last_id()
    def select_last_id(self) -> int:

        return self.mysql_cursor.lastrowid

    # DELETEを実行する関数
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
    # t：クラスのオブジェクト DBTable を入れる。
    # （使用例）
    # items = select_one(ToDoItem, ...)
    # items.comment='国語'
    # db.update(items)
    def update(self, t: DBTable):

        # primary_key を取得
        primary_key = t.orm_primary_key

        # updateカラム取得
        update_statements = t.sql_select_statement

        update_param = []
        update_str = ""

        # 取得したupdateカラムはstr型なので、list型に変換して要素をmember_nameに詰め替える。
        for member_name in update_statements.split(','):

            # primary_key は update 対象にしない。
            if member_name != primary_key:

                # updateしたいカラムを取り出し、"=?,"を付ける。
                update_str += member_name + "=?,"

                # updateしたいカラムの値をlistで取り出す。
                update_param.append(getattr(t, member_name))

        # 最後にprimary_key を追加する。
        update_param.append(getattr(t, primary_key))
        sql = [
            f"UPDATE {t.table_name} SET {update_str.rstrip(',')} WHERE {primary_key} = ?"]

        return self.execute(power_join(sql), update_param)

    # INSERTを実行する関数
    # t：クラスのオブジェクト DBTable を入れる。
    # （使用例）
    # item = ToDoItem()
    # item.id_name = 'hiya'
    # item.password = 'uma3141592'
    # db.insert(item)
    def insert(self, t: DBTable):

        # primary_key を取得
        primary_key = t.orm_primary_key

        # insertカラム取得
        insert_statements = t.sql_select_statement

        insert_param = []
        insert_str = ''
        insert_value = ''

        # 取得したupdateカラムはstr型なので、list型に変換して要素をmember_nameに詰め替える。
        for member_name in insert_statements.split(','):

            # primary_key は update 対象にしない。
            if member_name != primary_key:

                # updateしたいカラムを取り出す。
                insert_str += member_name + ","

                # updateしたいカラムを"?"で置換する。
                insert_value += "?,"

                # updateしたいカラムの値をlistで取り出す。
                insert_param.append(getattr(t, member_name))

        sql = [
            f"INSERT INTO {t.table_name} ({insert_str.rstrip(',')}) VALUES ({insert_value.rstrip(',')})"]

        return self.execute(power_join(sql), insert_param)


app = FlaskBuilder(__name__)


# ===================
#    Web API
# ===================
# Todoリストを全件取得する。
@app.route('/get_all_todos', methods=['GET'])
def get_all_todos():

    with MySQLConnector() as db:
        db_datas = db.select(ToDoItem)

        return jsonify([e.serialize() for e in db_datas])


# ToDoリストに1件追加する。
@app.route('/add', methods=['POST'])
# @login_required
def add_todo_item():
    todoitem = ToDoItem()

    # ToDoフォームのテキストボックスに入力されたテキストを取得する。
    todoitem.comment = request.json['comment']

    # コメント欄のテキストボックスが空でなければ、SQLを実行する。
    # コメント欄のテキストボックスが空なら何もしない。
    if todoitem.comment:
        with MySQLConnector() as db:

            # コメントをDBに登録する。
            db.insert(todoitem)
            # auto_incrementされたidを取得する。
            todoitem.id = db.select_last_id()

        return jsonify(todoitem.serialize()), 200


# ToDoリストに追加されたコメントをDBから1件だけ削除する。
# id : int
# 削除するコメントのid
@app.route('/delete/<int:id>', methods=['POST'])
# @login_required
def delete_todo_item(id: int):
    with MySQLConnector() as db:

        todo_item = db.select_one(
            ToDoItem, "WHERE id = ?", id)

        db.delete(todo_item)
    return jsonify(''), 200


# DB内のToDoリストをすべて削除する。
@app.route('/all_delete', methods=['POST'])
# @login_required
def all_delete_todo_items():
    with MySQLConnector() as db:

        # Todoリストをすべて削除する。
        db.delete(ToDoItem)
    return jsonify(''), 200


# ログイン成功後の画面(ホーム画面)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
# @login_required
def top(path):

    return render_template('index.html')


# ログイン前画面表示
@app.route('/login', methods=['GET'])
def login_view():
    # ログイン画面に表示する。
    return render_template('index.html')


# ログイン処理
@app.route('/login', methods=['POST'])
def login():

    with MySQLConnector() as db:

        # ログインフォームに入力されたユーザーIDとパスワード取得
        id_name = request.json['id_name']
        password = request.json['password']

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
        # return redirect(url_for('top' if LoginOk else 'index'))

        return jsonify(LognOk), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
