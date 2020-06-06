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
    return '', 204


# jsonで取得したデータのvalueを足し算してクライアントに返す。
@app.route('/')
def calc_income():
    x = json.loads(request.get_json())
    z = x[0][0] + x[1][0]
    print(z)
    return jsonify(z)


if __name__ == '__main__':
    app.run()
