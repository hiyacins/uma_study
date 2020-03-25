from flask import Flask, redirect, url_for, request, session
from functools import wraps
from HiyaLib.common import ReadJsonFromFile, FileReader


# Flaskクラスのbuilder
# シークレットキーの設定も行う。
# name：現在のファイルのモジュール名
# 返し値：Flaskクラスのインスタンスを返す。
# （使用例）
# app = FlaskBuilder(__name__)
def FlaskBuilder(name: str) -> Flask:

    app = Flask(name)

    # シークレットキーの設定のための関数
    with FileReader("exclude/secret_key.txt") as secret_key_file:
        app.config["SECRET_KEY"] = secret_key_file.readline().strip()

    # セッションログイン
    app.login = lambda loginOk: session['logged_in']=loginOk
    session['logged_in'] = loginOk

    # ログアウト
    # セッション情報をクリアする。
    app.logout = lambda: session.clear()

    return app


# デコレーター構文で用いる。ログインチェックの必要な関数にデコレーターとして付与する。
# （例）
def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        # セッション情報がなければログイン画面にリダイレクトする。
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(*args, **kwargs)

    return inner


# 入力フォームからデータを取得する。
# val：フォームに入力されたデータ
# 返し値：入力フォームから取得した引数が1つならstr型で返す。
# 　　　　複数あるならlist型データを返す。
# (使用例)
# request_form('id','comment')
def request_form(*val):

    num = len(val)
    if num == 0:
        raise ValueError("request_formの引数が0")
    elif num == 1:
        # tupleに要素が1つだけあれば、tupleから文字列に変換する。
        return request.form.get("".join(map(str, val)), "")

    # tupleに要素が複数あるなら要素をList型に入れ替えたものを返す。
    return [request.form.get(e, "") for e in val]
