from flask import session
from functools import wraps
from io import TextIOWrapper
import json


# JSONファイル丸読みして返す。
# ファイルはutf-8であるものとする。
# (使用例)
# with ReadJsonFromFile("config.json") as f:
#   line = json.load(f)
def ReadJsonFromFile(filename: str) -> str:
    return open(filename, 'r', encoding="utf-8")


# utf-8でread openするIOFileWrapper
# filename: 読み込むファイル
# (使用例)
# with FileReader("config.txt") as f:
#   line = f.readline()
def FileReader(filename: str) -> TextIOWrapper:
    return open(filename, 'r', encoding="utf-8")


# ログインチェック関数
def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        # セッション情報がなければログイン画面にリダイレクトする。
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(*args, **kwargs)

    return inner
