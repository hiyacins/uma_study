from flask import Flask, jsonify
from flask import render_template
from flask import request
import mysql.connector

app = Flask(__name__)
mysql = SQLAlchemy()

config = {
    'user': 'root',
    'password': 'hiya1023',
    'host': 'localhost',
    'database': 'site_master'
}


def ExecuteQuery(sql):
    con = mysql.connector.connect(**config)
    cursor = con.cursor(buffered=True)

    stmt = "select * from site_master"
    cursor.execute(stmt)
    results = cursor.fetchall()


@app.route('/')
def login():
    return render_template('index.html')


@app.route("/home", methods=["POST"])
def home():
    results = ExecuteQuery('select * from site_master_login_tb;')
    return results  #jsonify(results)  #render_template('top.html')


## おまじない
if __name__ == "__main__":
    app.run(debug=True)