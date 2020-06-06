from HiyaLib import *
import unittest

app = FlaskBuilder(__name__)

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
    return render_template('index.html')


# ログイン処理
@app.route('/login', methods=['POST'])
def login():

    # with MySQLConnector() as db:

    #     # ログインフォームに入力されたユーザーIDとパスワード取得
    #     id_name, password = request_form('id_name', 'password')

    #     # ログインフォームに入力されたユーザーIDをパラメーターに、select_one関数で
    #     # DBのテーブルクラスを入れ、fetchoneをして、値を抽出する。
    #     # ただし、ログインフォームに入力されたユーザーIDが空のときは、Noneを返す。
    #     site_user = db.select_one(
    #         SiteUser, "WHERE id_name = ?", id_name) if id_name else None

    #     # ユーザーIDがDB内に存在し、フォームから入力されたパスワードがDB内のものと一致すれば
    #     # セッションを登録する
    #     LoginOk = site_user is not None and check_password_hash(
    #         site_user.password, password)
    #     app.login(LoginOk)

    #     if not LoginOk:
    #         flash('ログイン失敗：ユーザーIDもしくはパスワードが正しくありません。')

        # ログインに成功していれば、ログイン後のページへリダイレクトする。
        # ログインに失敗していれば、ログインページにリダイレクトする。(再度表示する)
    return redirect(url_for('top' if LoginOk else 'index'))


# ログアウト処理
@app.route("/logout", methods=["GET"])
def logout():

    app.logout()

    return redirect(url_for('login'))


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

######################################
# unittest.TestCaseの子クラス
# -- unittestはここに書く


class App_Test(unittest.TestCase):

    # insert関数のunitテスト
    def test_insert(self):
        # ここにテスト項目を書いていく。
        with MySQLConnector() as db:

            ######################################
            # insert 基本 テスト
            ######################################
            testitems = TestTable2()
            testitems.id_name = '-tama-'
            testitems.password = '0073-735963'
            db.insert(testitems)

            # ######################################
            # # insert → update のテスト
            # ######################################
            # testitems = TestTable()
            # testitems.comment = 'かり_んとう'
            # # commentをDBに登録する。
            # db.insert(testitems)

            # # insert した auto_increment_id を取得する。
            # #auto_increment_id = db.select_ex(TestTable)
            # auto_increment_id = db.execute("SELECT LAST_INSERT_ID()")
            # testitems = db.select_one(
            #     TestTable, "WHERE id = ?", auto_increment_id)
            # testitems.comment = '国語'
            # db.update(testitems)

    # # update関数のunitテスト#
    # def test_update(self):
    #     # ここにテスト項目を書いていく。
    #     #test_table = ('算数', 1)

    #     with MySQLConnector() as db:

    #         ######################################
    #         # update 基本 テスト
    #         ######################################
    #         testitem = db.select_one(TestTable2, "WHERE id = ?", 1)
    #         # testitem.comment = '国語'
    #         testitem.id_name = 'umauma_'
    #         testitem.password = 'affili777_'

    #         db.update(testitem)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
    # app.run(host="0.0.0.0", port=80, debug=False)
    # unittest.main()
