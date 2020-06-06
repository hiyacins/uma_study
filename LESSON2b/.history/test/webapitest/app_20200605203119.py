from flask import Flask, jsonify, request

app = Flask(__name__)


incomes = [
    {"1": "python"}
]


@app.route('/incomes')
def get_incomes():
    return jsonify({"1": "python"})


if __name__ == '__main__':
    app.run()
