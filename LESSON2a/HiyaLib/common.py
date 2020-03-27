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


# s1とs2の文字列を連結して返す。
# 連結するときにs2に対して手前にスペースを入れる。
# ただしs2が空("" or None)なら、その要素を無視する。(スペースを入れない)
# s1：文字列s1をいれる。
# s2：文字列s2をいれる。
# 返し値：s1とs2を連結させた文字列を返す。
#        s2が空("" or None)のときは、s1のみ返す。
# （使用例）
# hiya_join(f"SELECT {t.orm_select_sql} FROM {t.__table_name__}", where_str)
def hiya_join(sql: str, where_str: str):

    return " ".join([sql, where_str]) if where_str else sql


# hiya_join関数のunitテスト
def hiya_joinTest():
    my_assert(hiya_join("ABC", "DEF") == "ABC DEF")
    my_assert(hiya_join("ABC", "") == "ABC")


if __name__ == "__main__":
    hiya_join()
