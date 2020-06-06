from flask import Flask, jsonify, request
import json

app = Flask(__name__)

number = {}


# クライアント側からPostされてくる
@app.route('/incomes')
def get_incomes():
    return jsonify(number)


# postされてきた情報を追加する。No Contentの場合のみ返す。
@app.route('/incomes', methods=['POST'])
def add_income():
    number = request.get_json()
    print(number)
    x = number["1"] + number["2"]
    print(x)
    return '', 204


if __name__ == '__main__':
    app.run()
