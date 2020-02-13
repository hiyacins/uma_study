from flask import Flask
from flask import render_template
from flask import request
from db import MySQL
dns = {
    'user': 'root',
    'host': 'localhost',
    'password': 'hiya1023',
    'database': 'site_master'
}
db = MySQL(**dns)

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def login():
    # if request.method == "POST":
    #     name = request.form["name"]
    # else:
    #     name = "no name."
    return render_template('index.html', title='flask test', name=name)


@app.route('/home')
def home(name=None):
    name = "Hello World"
    return name


## おまじない
if __name__ == "__main__":
    app.run(debug=True)