from flask import Flask, jsonify
from flask import render_template
from flask import request
import mysql.connector

config = {
    'user': 'root',
    'password': 'hiya1023',
    'host': 'localhost',
    'database': 'site_master'
}
app = Flask(__name__)

# def ExecuteQuery(sql):
#     con = mysql.connector.connect(**config)
#     cursor = con.cursor(buffered=True)

#     stmt = "select * from site_master"
#     cursor.execute(stmt)
#     results = cursor.fetchall()


@app.route('/')
def login():
    return render_template('index.html')


@app.route("/home", methods=["POST"])
def home():
    con = mysql.connector.connect(**config)
    cursor = con.cursor(buffered=True)

    stmt = "select * from site_master"
    cursor.execute(stmt)
    results = cursor.fetchall()

    return results  #jsonify(results)  #render_template('top.html')


## おまじない
if __name__ == "__main__":
    app.run(debug=True)