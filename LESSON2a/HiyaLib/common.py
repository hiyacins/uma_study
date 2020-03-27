from io import TextIOWrapper
from typing import Union, List, Tuple
import json
import unittest


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


# unittest項目に対して、期待通りの値が出ればOK。値が違えば、assert文が出る。
# b：unittestしたい項目を入れる。
# （使用例）
# my_assert(hiya_join(["ABC", "DEF"]) == "ABC DEF")
def my_assert(b: bool):
    assert b, '期待通りの値が出力されていません。'


# List[str]型で与えられた文字列を連結して返す。
# 連結するときに s[i](i>=1) に対して手前にスペースを入れる。
# ただし s[i] が空("" or None)なら、その要素を無視する。(スペースを入れない)
# str_list：文字列s1をいれる。
# 返し値：List[str]型で与えられた文字列を連結して返す。ただし、空の要素は、無視する。
# （使用例）
# sql=[f"SELECT {t.orm_select_sql} FROM {t.__table_name__}", where_str]
# hiya_join(sql)
def hiya_join(str_list: List[str]) -> str:

    return " ".join([s for s in str_list if s])


# unittest.TestCaseの子クラス
class MyTest(unittest.TestCase):

    # hiya_join関数のunitテスト
    def test_hiya_joinTest(self):
        # ここにテスト項目を書いていく。
        my_assert(hiya_join(["ABC", "DEF"]) == "ABC DEF")
        my_assert(hiya_join(["ABC", ""]) == "ABC")


if __name__ == "__main__":
    unittest.main()
