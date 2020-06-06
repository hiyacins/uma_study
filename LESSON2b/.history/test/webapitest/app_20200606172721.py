from flask import Flask, jsonify, request

app = Flask(__name__)

number = []


# クライアント側からPostされてくる
@app.route('/incomes')
def get_incomes():
    return jsonify(number)


# postされてきた情報を追加する。No Contentの場合のみ返す。
@app.route('/incomes', methods=['POST'])
def add_income():
    y = number.append(request.get_json())
    return '', 204


if __name__ == '__main__':
    app.run()
