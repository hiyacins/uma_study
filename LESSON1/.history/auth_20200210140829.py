from flask import Flask
from flask import url_for
from flask import redirect
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


@app.route('/')
def login(name=None):
    """
    GET ：ログイン画面に遷移
    POST：ログイン処理を実施
    """
    #if request.method == 'GET':
        # ログイン画面に遷移
        return render_template('index.html', name=name)


## おまじない
if __name__ == "__main__":
    app.run(debug=True)