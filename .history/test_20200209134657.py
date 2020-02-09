from flask import Flask
from flask import render_template

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