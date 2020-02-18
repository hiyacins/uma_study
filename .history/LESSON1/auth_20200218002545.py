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
app.config["SECRET_KEY"] = "b't\xd7.\xedOa\xd8\x88\x18\xc51H\xf5\x0b\xb1\x10\x99\xde\x11\xa9\x12\xe3\xd3S'"


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        # ログイン画面に遷移
        return render_template('index.html')

    # ログインフォームに入力されたユーザーIDとパスワードの取得
    id_name = request.form['id_name']
    #password = generate_password_hash(request.form['password'])
    #debug_print(password)
    password = request.form['password']
    pdebug_printrint(id_name)
    debug_print(password)

    # DB接続
    con = mysql.connector.connect(**config)
    #cursor = con.cursor(buffered=True)
    cursor = con.cursor(prepared=True)
    debug_print("DB接続")

    # ユーザー名とパスワードのチェック
    #message = None

    cursor.execute('select * from site_master_login_tb where id_name = ?',
                   (id_name, ))
    results = cursor.fetchone()
    debug_print(results)
    if results:
        cursor.execute('select * from site_master_login_tb where id_name = ?',
                       (id_name, ))
        for row in cursor.fetchall():
            debug_print(row[2])

    # #passsalt = 'pbkdf2:sha256:150000$wPgnYJj9$571d6740d6d6f42db4af4c01648a146a0f15aaa039befcc3e48c5800974adb68'

    if results is None:
        #message = 'ユーザー名が正しくありません'
        flash("ログイン失敗", category="failed")
        cursor.close()
        con.close()
        debug_print("NG_use")
        return render_template('index.html')
    elif not check_password_hash(row[2], password):
        flash("ログイン失敗", category="failed")
        cursor.close()
        con.close()
        debug_print("NG_pass")
        return render_template('index.html')
    else:
        #flash("ログインを成功しました＼(^o^)／", category="success")
        cursor.close()
        con.close()
        debug_print("OK")
        return home()


@app.route("/home", methods=["GET"])
def home():
    return render_template('top.html')

def debug_print(s):
  if True:
    print(s)

if __name__ == "__main__":
    app.run(debug=True)