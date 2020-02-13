from flask import Flask, jsonify
from flask import render_template
from flask import request
from flask_sqlalchemy import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'hiya1023'
app.config['MYSQL_DATABASE_DB'] = 'site_master'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql.init_app(app)


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
    results = ExecuteQuery('select 123 as x from dual')
    return jsonify(results)  #render_template('top.html')


## おまじない
if __name__ == "__main__":
    app.run(debug=True)