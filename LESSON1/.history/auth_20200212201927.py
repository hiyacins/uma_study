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
app.config["SECRET_KEY"] = "tokutoku777"


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
    print(generate_password_hash(request.form['password']))

    # DB接続
    con = mysql.connector.connect(**config)
    cursor = con.cursor(buffered=True)
    print("DB接続")

    # ユーザー名とパスワードのチェック
    #message = None

    cursor.execute('select * from site_master_login_tb where id_name = %s',
                   (id_name, ))
    results = cursor.fetchone()
    cursor.execute('select password from site_master_login_tb where id = 2')
    rlt_pass = cursor.fetchone()

    print(rlt_pass)
    #print(check_password_hash(rlt_pass, password))

    if results is None:
        #message = 'ユーザー名が正しくありません'
        flash("ログイン失敗", category="failed")
        print("NG_use")
        return render_template('index.html')
    elif not check_password_hash(self.password, password):
        #elif (rlt_pass != password):
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