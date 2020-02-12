from flask import Flask, redirect, render_template, request, session, url_for, flash
import mysql.connector

config = {
    'user': 'root',
    'password': 'hiya1023',
    'host': 'localhost',
    'port': 3306,
    'database': 'site_master'
}
app = Flask(__name__)
app.config["SECRET_KEY"] = "tokutoku777"


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        # ログイン画面に遷移
        return render_template('index.html')

    # ログインフォームに入力されたユーザーIDとパスワードの取得
    id_name = request.form['id_name']
    password = request.form['password']
    print(id_name)
    print(password)

    # DB接続
    con = mysql.connector.connect(**config)
    cursor = con.cursor(buffered=True)
    print("DB接続")

    # ユーザー名とパスワードのチェック
    error_message = None

    cursor.execute('select * from site_master_login_tb where id_name = %s',
                   (id_name, ))
    results = cursor.fetchone()
    print(results)
    print(request.form['id_name'])

    # if results == request.form['id_name']:
    #     error_message = 'ユーザー名が正しくありません'
    #     return render_template('index.html')
    # else:
    #     return redirect(url_for('home'))

    # elif not check_password_hash(user['password'], password):
    #     error_message = 'パスワードが正しくありません'
    if results is None:
        #message = 'ユーザー名が正しくありません'
        flash("ログイン失敗", "failed")
        return render_template('index.html')
    else:
        #message = 'ユーザー名が正しくありません'
        flash("ログインを成功しました＼(^o^)／", "success")
        print("OK")
        return render_template('top.html')

    # elif not check_password_hash(results['password'], password):
    #     error_message = 'パスワードが正しくありません'
    #     return redirect(url_for('home'))
    print("END")

    # if error_message is not None:
    #     # エラーがあればそれを表示したうえでログイン画面に遷移
    #     flash(error_message, category='alert alert-danger')
    #     return redirect(url_for('/'))

    # # エラーがなければ、セッションにユーザーIDを追加してインデックスページへ遷移
    # session.clear()
    # session['user_id'] = user['id']
    # flash('{}さんとしてログインしました'.format(userid), category='alert alert-info')
    # return redirect(url_for('home'))

    # stmt = "select * from site_master_login_tb"
    # cursor.execute(stmt)
    # results = cursor.fetchall()
    # print(results)

    # return render_template('index.html')


@app.route("/home")
def home():
    return render_template('top.html')


if __name__ == "__main__":
    app.run(debug=True)