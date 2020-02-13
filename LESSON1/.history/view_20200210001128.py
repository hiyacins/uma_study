from flask import render_template
from flask_book_management_1 import app


@app.route('/')
def hello():
    name = "Hello World"
    return name
