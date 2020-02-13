from flask import Flask
from flask import render_template
from db import MySQL
dns = {
    'user': 'root',
    'host': 'localhost',
    'password': 'hiya1023',
    'database': 'site_master'
}
db = MySQL(**dns)

app = Flask(__name__)


@app.route('/', methods=['POST'])
def login(name=None):
    #if request.method == 'GET':
    # ログイン画面に遷移
    return render_template('index.html', name=name)


@app.route('/home')
def home(name=None):
    name = "Hello World"
    return name


## おまじない
if __name__ == "__main__":
    app.run(debug=True)