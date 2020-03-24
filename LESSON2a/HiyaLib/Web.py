from flask import Flask, redirect, url_for, request, session
from functools import wraps
from HiyaLib.common import ReadJsonFromFile, FileReader


# ログインチェック関数
def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        # セッション情報がなければログイン画面にリダイレクトする。
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(*args, **kwargs)

    return inner


# 入力フォームからデータを取得する。
# s：フォームに入力されたデータ
# 返し値：入力フォームから取得した引数が1つならstr型で返す。
# 　　　　複数あるならlist型データを返す。
# (使用例)
# request_form('id','comment')
def request_form(*val) -> list:

    # tupleに要素が1つだけあれば、tupleから文字列に変換する。
    if len(val) == 1:
        return request.form.get("".join(map(str, val)), "")

    # tupleに要素が複数あるなら要素をList型に入れ替えたものを返す。
    return [request.form.get(e, "") for e in val]


# シークレットキーの設定のための関数
# app：Flaskクラスをインスタンス化したもの。
# file_path：シークレットキーファイルを読み込む。
# 返し値：読み込んだシークレットキーの内容を str型 で返す。
# （使用例）
#   set_secret_key(app, "exclude/secret_key.txt")
def set_secret_key(app: Flask, file_path: str)->str:
    with FileReader(file_path) as secret_key_file:
        app.config["SECRET_KEY"] = secret_key_file.readline().strip()
    return app.config["SECRET_KEY"]
