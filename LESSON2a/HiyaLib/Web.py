from flask import redirect, url_for, request, session
from functools import wraps


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
# 返し値：入力フォームから取得したdict型データを返す。
# (使用例)
# request_form('comment')
def request_form(*val) -> str:

    # tupleに要素が1つだけあれば、tupleから文字列に変換する。
    if len(val) < 2:
        return request.form.get("".join(map(str, val)), "")

    rusult = list
    for name in range(len(val)):
        rusults = list(request.form.get(val[name], ""))
        #rusults = list(request.form.get("".join(map(str, val[name])), ""))

    return rusults
