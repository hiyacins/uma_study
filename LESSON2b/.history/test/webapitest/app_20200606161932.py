from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/incomes')
def get_incomes():
    return jsonify(number)


@app.route('/incomes', methods=['POST'])
def add_income():
    y = number.append(request.get_json())
    return jsonify(y), 200


if __name__ == '__main__':
    app.run()