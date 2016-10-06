from flask import Flask, render_template, redirect, request, session
import random

app = Flask(__name__)

app.secret_key = 'secretsOfNimh'

def initializeMagicNum():
	try: 
		session["magicNum"]
	except KeyError:
		session["magicNum"] = int(round((random.random())*100))
	try: 
		session["guess"]
	except KeyError:
		session["guess"] = 0
	try:
		session["style"]
	except KeyError:
		session["style"] = "hide"
		session["showHide"] = ["hide", "show"]
	try: 
		session["newGame"]
	except KeyError:
		session["newGame"] = True
		session["resultText"] = ""


def resetMagicNum():
	session["magicNum"] = int(round((random.random())*100))
	session["guess"] = 0 
	session["style"] = "hide"
	session["newGame"] = True
	session["showHide"] = ["hide", "show"]


@app.route('/')
def welcome():
	initializeMagicNum()
	session["result"] = int(session["magicNum"]) - int(session["guess"])
	if session["newGame"] == False:
		if (session["result"] < 0): 
			session["style"] = "red"
			session["resultText"] =  str(session["guess"])+ " was too HIGH!"
		elif (session["result"] > 0):	
			session["style"] = "red"
			session["resultText"] =  str(session["guess"])+ " was too LOW!"
		else: 
			session["style"] = "green"
			session["resultText"] = "You WON!"
			session["showHide"] = ["show", "hide"]
	return render_template('index.html', userguess = session["guess"], magicNum = session["magicNum"], style = session["style"], resultText = session["resultText"], showHide=session["showHide"])

@app.route('/guess', methods=['POST'])
def guess():
	session["guess"] = request.form['userguess']
	session["newGame"] = False
	return redirect('/')

@app.route('/reset')
def reset():
	resetMagicNum()
	return redirect('/')

app.run(debug=True)