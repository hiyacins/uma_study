from flask import Flask, jsonify, request
import json

app = Flask(__name__)

number = []


# クライアント側からPostされてくる
@app.route('/incomes')
def get_incomes():
    return jsonify(number)


# postされてきた情報を追加する。No Contentの場合のみ返す。
@app.route('/incomes', methods=['POST'])
def add_income():
    number.append(request.get_json())
    print(number)
    x = number[0][0] + number[1][0]
    print(x)
    return '', 204


# # jsonで取得したデータのvalueを足し算してクライアントに返す。
# @app.route('/')
# def calc_income():
#     print("きたよ")
#     x = json.loads(number)
#     print(x)
#     z = int(x[0]) + int(x[1])
#     print(z)
#     return jsonify(z)


if __name__ == '__main__':
    app.run()
