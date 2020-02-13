from flask import render_template
from flask_login_site import app


@app.route('/home')
def home():
    name = "NONE"  #"Hello World"
    return name
