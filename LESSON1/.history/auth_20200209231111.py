from flask import Flask
from flask import url_for
from flask import redirect
from flask import render_template

from DataStore.MySQL import MySQL
dns = {
    'user': 'mysql',
    'host': 'localhost',
    'password': 'NewPassword',
    'database': 'kaggle'
}
db = MySQL(**dns)

app = Flask(__name__)


@app.route('/')
def hello():
    name = "Hello World"
    return name


@app.route('/login')
def login(name=None):
    return render_template('index.html', name=name)


## おまじない
if __name__ == "__main__":
    app.run(debug=True)