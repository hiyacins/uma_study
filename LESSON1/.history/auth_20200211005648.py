from flask import Flask, jsonify
from flask import render_template
from flask import request
import mysql.connector

config = {
    'user': 'root',
    'password': 'hiya1023',
    'host': 'localhost',
    'port': 3306,
    'database': 'site_master'
}
app = Flask(__name__)


@app.route('/')
def login():
    con = mysql.connector.connect(**config)
    cursor = con.cursor(buffered=True)

    stmt = "select * from site_master_login_tb"
    cursor.execute(stmt)
    results = cursor.fetchall()
    print(results)
    name = "Hello"
    return name


# def login():
#     return render_template('index.html')

#@app.route("/home", methods=["POST"])
#@app.route('/home')
# def home():
#     con = mysql.connector.connect(**config)
#     cursor = con.cursor(buffered=True)

#     stmt = "select * from site_master_login_tb"
#     cursor.execute(stmt)
#     results = cursor.fetchall()
#      return results  #jsonify(results)  #render_template('top.html')

## おまじない
if __name__ == "__main__":
    app.run(debug=True)