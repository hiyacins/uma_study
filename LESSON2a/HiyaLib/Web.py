from flask import Flask, redirect, url_for, request, session
from functools import wraps
from HiyaLib.common import ReadJsonFromFile, FileReader


# Flaskクラスのbuilder
# シークレットキーの設定も行う。
# appでログインするためにlogin関数を生やしています。
# appでログアウトするためにlogout関数を生やしています。
# name：現在のファイルのモジュール名
# 返し値：Flaskクラスのインスタンスを返す。
# （使用例）
# app = FlaskBuilder(__name__)
def FlaskBuilder(name: str) -> Flask:

    app = Flask(name)

    # シークレットキーの設定のための関数
    with FileReader("exclude/secret_key.txt") as secret_key_file:
        app.config["SECRET_KEY"] = secret_key_file.readline().strip()

    # ログインが成功しているとき、セッション情報を登録する。
    # ログインが失敗しているとき、登録しない。
    # loginOk：ログイン認証の真偽値を入れる変数
    # （使用例）
    # app.login(loginOk)
    def login(loginOk: bool):
        session["logged_in"] = loginOk

    # ログインが成功のとき、セッション情報を登録する。
    app.login = login

    # ログアウトするとき、セッション情報をクリアする。
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


# request.form からデータを取得する。
# val：request.form.get(name)のnameを指定する。複数指定可能。
# 返し値：request.form.get(name)の値をstr型で返す。
# 　　　　※ nameを複数指定した場合は、返し値は、List[str]になる。
# (使用例)
# request_form('id','id_name','password')
def request_form(*val: Tuple[str...]):

    num = len(val)

    if num == 0:
        raise ValueError("request_formの引数が0個")
    elif num == 1:
        # tupleに要素が1つだけあれば、tupleから文字列に変換する。
        return [request.form.get(e, "") for e in val if e]

    # tupleに要素が複数あるなら要素をList型に入れ替えたものを返す。
    return [request.form.get(e, "") for e in val]
