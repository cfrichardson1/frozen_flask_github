from app import app
from flask import redirect, render_template, url_for


@app.route('/')
def home():
	return render_template('homepage_exp.html', title_bar ='Homepage')
