from flask import render_template


@app.route('/home')
def home():
    name = "Hello World"
    return name
