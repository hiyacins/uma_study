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
    print('きた')
    jsonDict = json.loads(number.append(request.get_json()))
    print(jsonDict)
    x = int(jsonDict["1"]) + int(jsonDict["2"])
    print(x)
    return '', 204


if __name__ == '__main__':
    app.run()
