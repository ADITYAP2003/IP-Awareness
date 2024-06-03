from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

app.template_folder = './static/html'
app.static_folder = './static'


@app.route('/')
def signup():
    return render_template('mainPage.html')


@app.route('/success')
def success():
    return render_template('successRegister.html')


if __name__ == '__main__':
    app.run(debug=True)
