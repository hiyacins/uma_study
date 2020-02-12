from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import mysql.connector

config = {
    'user': 'root',
    'password': 'hiya1023',
    'host': 'localhost',
    'port': 3306,
    'database': 'site_master'
}
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        # ログイン画面に遷移
        return render_template('index.html')

    # ログインフォームに入力されたユーザーIDとパスワードの取得
    user_id = request.form['user_id']
    password = request.form['password']
print(user_id)
print(password)
    # DB接続
    con = mysql.connector.connect(**config)
    cursor = con.cursor(buffered=True)

    # # ユーザー名とパスワードのチェック
    # error_message = None

    # user = cursor.execute(
    #     'SELECT * FROM site_master_login_tb WHERE userid = ?',
    #     (userid, )).fetchone()

    # if user is None:
    #     error_message = 'ユーザー名が正しくありません'
    # elif not check_password_hash(user['password'], password):
    #     error_message = 'パスワードが正しくありません'

    # if error_message is not None:
    #     # エラーがあればそれを表示したうえでログイン画面に遷移
    #     flash(error_message, category='alert alert-danger')
    #     return redirect(url_for('/'))

    # # エラーがなければ、セッションにユーザーIDを追加してインデックスページへ遷移
    # session.clear()
    # session['user_id'] = user['id']
    # flash('{}さんとしてログインしました'.format(userid), category='alert alert-info')
    return redirect(url_for('home'))

    # stmt = "select * from site_master_login_tb"
    # cursor.execute(stmt)
    # results = cursor.fetchall()
    # print(results)

    # return render_template('index.html')


@app.route("/home")
def home():
    # con = mysql.connector.connect(**config)
    # cursor = con.cursor(buffered=True)

    # stmt = "select * from site_master_login_tb"
    # cursor.execute(stmt)
    # results = cursor.fetchall()
    # print(results)

    return render_template('top.html')


## おまじない
if __name__ == "__main__":
    app.run(debug=True)