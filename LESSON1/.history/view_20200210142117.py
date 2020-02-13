from flask import render_template


@app.route('/home')
def home():
    name = "NONE"  #"Hello World"
    return name
