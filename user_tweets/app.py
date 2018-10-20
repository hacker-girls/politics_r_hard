import flask
from flask import Flask, request, render_template
import json


app = Flask(__name__)

@app.route('/getTweets')
def form_input():
	if request.method = 'POST':
		name = request.args.get('name')
		location = request.args.get('location')

@app.route('/')

def main():

	
	templateData = {
		'title' : 'CUhackit last 10 tweets',
		'mytweets' : mytweets,
	}

	return flask.render_template("index.html", **templateData)

if __name__ == '__main__':
	app.debug=True
	app.run()

