from flask import Flask, jsonify, request
import json

app = Flask(__name__)

number = {}


# サーバーからクライアント側にjsonでpostされた内容を返す
@app.route('/incomes')
def get_incomes():
    return jsonify(number)


# クライアントからサーバーにpostされてきた情報を取得して値を計算する。
# No Contentの場合のみ返す。
@app.route('/incomes', methods=['POST'])
def add_income():
    number = request.get_json()
    print(number)
    number["3"] = number["1"] + number["2"]
    print(number)
    return jsonify(number["3"])　  # '', 204


if __name__ == '__main__':
    app.run()
