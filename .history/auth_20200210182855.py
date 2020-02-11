from flask import Flask
from flask import render_template
from flask import request
# from db import MySQL
# dns = {
#     'user': 'root',
#     'host': 'localhost',
#     'password': 'hiya1023',
#     'database': 'site_master'
# }
# db = MySQL(**dns)

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('index.html')


@app.route("/home", methods=["POST"])
def home():
    return render_template('top.html')


## おまじない
if __name__ == "__main__":
    app.run(debug=True)