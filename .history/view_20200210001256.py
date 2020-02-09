from flask import render_template
from flask_book_management_1 import app


@app.route('/home')
def home():
    name = "Hello World"
    return name
