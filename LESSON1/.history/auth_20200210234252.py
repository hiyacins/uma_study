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

con = mysql.connector.connect(**config)
cursor = con.cursor(buffered=True)

stmt = "select * from site_master"
cursor.execute(stmt)
results = cursor.fetchall()


def ExecuteQuery(sql):
    cur = mysql.connect().cursor()
    cur.execute(sql)
    results = [
        dict((cur.description[i][0], value) for i, value in enumerate(row))
        for row in cur.fetchall()
    ]
    return results


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