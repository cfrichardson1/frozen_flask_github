# need to transfer all apps into this one app
from app import app
from flask import redirect, render_template, url_for


@app.route('/index.html')
def home():
	return render_template('homepage.html', title_bar ='Homepage')

@app.route('/PyCitySchools_EDA.html')
def PyCity():
	return render_template('PySchool_Report_colab0.html', title_bar ='Test')
