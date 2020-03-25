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


# 文字列があるときは、先頭に半角空白を付け、 文字列がないときは、空文字を返す関数
# s：文字列を入れる変数
# 返し値：引数に文字列があるとき、半角空白と文字列を返す。文字列がないときは、 ""を返す。
# （使用例）
# sql = f"SELECT {t.sql_select_statement} FROM {t.table_name}{Space(sql_where)}"
def Space(s: str) -> str:
    if s == "":
        return ""

    return " " + s
