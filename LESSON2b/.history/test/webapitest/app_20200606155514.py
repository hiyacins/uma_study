from flask import Flask, jsonify, request

app = Flask(__name__)


incomes = [
    {"1": 1},
    {"2": 2},
]


@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
    y = incomes.append(request.get_json())
    return sonify(y), 200


if __name__ == '__main__':
    app.run()
