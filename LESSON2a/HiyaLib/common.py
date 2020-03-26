from io import TextIOWrapper
import json


# JSONファイル丸読みしてdict型データを返す。
# ファイルの文字エンコードはutf-8であるものとする。
# filename：丸読みするJSONファイル
# 返し値：dict型に変換して返す。
# (使用例)
# self.connect(ReadJsonFromFile("config.json"))
def ReadJsonFromFile(filename: str) -> dict:
    # json形式で読み込む。
    with open(filename, 'r', encoding="utf-8") as jsonFile:
        return json.load(jsonFile)


# utf-8でread openするIOFileWrapper
# filename: 読み込むファイル
# 返し値: TextIOWrapper型に変換して返す。
# (使用例)
# with FileReader("config.txt") as f:
#   line = f.readline()
def FileReader(filename: str) -> TextIOWrapper:
    return open(filename, 'r', encoding="utf-8")


# 文字列sがあるときは、先頭に半角空白を付け、文字列sがないときは、空文字を返す関数
# s：文字列sを入れる変数。ただし、文字列sにNoneをいれてはいけない。
# 返し値：引数に文字列sがあるとき、半角空白と文字列sを返す。文字列sがないときは、""を返す。
# （使用例）
# sql = f"SELECT {t.sql_select_statement} FROM {t.table_name}{Space(sql_where)}"
def Space(s: str) -> str:
    return "" and " " + s


# List[str]型で与えられた文字列を連結して返す。
# 連結するときにs[i](i>=1)に対して手前にスペースを入れる。
# ただしs[i]が空("" or None)なら、その要素を無視する。(スペースを入れない)
# s1：
# s2：
# 返し値：s1とs2を連結させた文字列を返す。
#        s2が空("" or None)のときは、s1のみ返す。
# （使用例）
# hiya_join(f"SELECT {t.orm_select_sql} FROM {t.__table_name__}", where_str)
def hiya_join(sql: str, where_str: str):

    return " ".join([sql, where_str]) if where_str else "".join([sql])


# hiya_join関数のunitテスト
def hiya_joinTest():
    my_assert(hiya_join("ABC", "DEF") == "ABC DEF")
    my_assert(hiya_join("ABC", "") == "ABC")


if __name__ == "__main__":
    hiya_join()
