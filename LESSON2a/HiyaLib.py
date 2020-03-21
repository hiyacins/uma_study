from flask import session
from functools import wraps
from io import TextIOWrapper
import json


# JSONファイル丸読みしてdict型データを返す。
# ファイルはutf-8であるものとする。
# filename：丸読みするJSONファイル
# 返し値：str型からdict型に変換して返す。
# (使用例)
# self.connect(ReadJsonFromFile("config.json"))
def ReadJsonFromFile(filename: str) -> dict:
    # json形式で読み込む。
    with open(filename, 'r', encoding="utf-8") as jsonFile:
        return json.load(jsonFile)


# utf-8でread openするIOFileWrapper
# filename: 読み込むファイル
# 返し値: str型からTextIOWrapper型に変換して返す。
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
