from flask import Flask, redirect, render_template, request, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

config = {
    'user': 'root',
    'password': 'hiya1023',
    'host': 'localhost',
    'port': 3306,
    'database': 'site_master'
}
app = Flask(__name__)
app.config[
    "SECRET_KEY"] = "b't\xd7.\xedOa\xd8\x88\x18\xc51H\xf5\x0b\xb1\x10\x99\xde\x11\xa9\x12\xe3\xd3S'"


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        # ログイン画面に遷移
        return render_template('index.html')

    # ログインフォームに入力されたユーザーIDとパスワードの取得
    id_name = request.form['id_name']
    #password = generate_password_hash(request.form['password'])
    password = request.form['password']
    print(id_name)
    print(password)

    # DB接続
    con = mysql.connector.connect(**config)
    cursor = con.cursor(buffered=True)
    print("DB接続")

    # ユーザー名とパスワードのチェック
    #message = None

    results = cursor.execute(
        'select * from site_master_login_tb where id_name = %s',
        (id_name, )).fetchone()
    # results = cursor.fetchone()
    # cursor.execute('select password from site_master_login_tb where id = 2')
    # rlt_pass = cursor.fetchone()
    # rlt_pass = rlt_pass.strip()
    # print(rlt_pass)
    #print(check_password_hash(rlt_pass, password))
    #passsalt = 'pbkdf2:sha256:150000$wPgnYJj9$571d6740d6d6f42db4af4c01648a146a0f15aaa039befcc3e48c5800974adb68'
    if results is None:
        #message = 'ユーザー名が正しくありません'
        flash("ログイン失敗", category="failed")
        print("NG_use")
        return render_template('index.html')
    #elif not check_password_hash(rlt_pass, password):
    elif not check_password_hash(site_master_login_tb['password'], password):
        flash("ログイン失敗", category="failed")
        print("NG_pass")
        return render_template('index.html')
    else:
        flash("ログインを成功しました＼(^o^)／", category="success")
        print("OK")
        return render_template('top.html')

    # elif not check_password_hash(results['password'], password):
    #     error_message = 'パスワードが正しくありません'
    #     return redirect(url_for('home'))
    print("END")


@app.route("/home")
def home():
    return render_template('top.html')


if __name__ == "__main__":
    app.run(debug=True)