from flask import Flask, jsonify, request

app = Flask(__name__)

incomes = []


@app.route('/incomes')
def get_incomes():
    print(jsonify(y))
    return jsonify(incomes)


# @app.route('/incomes', methods=['POST'])
# def add_income():
#     y = incomes.append(request.get_json())
#     print(jsonify(y))
#     return jsonify(y), 200


if __name__ == '__main__':
    app.run()
