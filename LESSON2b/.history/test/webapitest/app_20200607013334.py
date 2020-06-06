from flask import Flask, jsonify, request
import json

app = Flask(__name__)

number = []


# クライアント側からPostされてくる
@app.route('/incomes')
def get_incomes():
    return jsonify(jsonDict)


# postされてきた情報を追加する。No Contentの場合のみ返す。
@app.route('/incomes', methods=['POST'])
def add_income():

    number.append(request.get_json())
    jsonDict = json.loads(number)
    print(jsonDict)
    x = int(jsonDict["1"]) + int(jsonDict["2"])
    print(x)
    return '', 204


if __name__ == '__main__':
    app.run()
