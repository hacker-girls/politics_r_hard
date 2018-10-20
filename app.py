import flask
import twitter
from flask import Flask, request, render_template
from twitter import *
import json

OAUTH_TOKEN="2464717370-ztIheNqKFIr9ll1ZG3OEa1SxRPTGY8k1XL3Ukj0"
OAUTH_SECRET="doEQPqBTLo22FrakNfY2q3jdLJyary6TFcLT8sv8AJes7"
CONSUMER_KEY="0J1e4CLZOLJTG1fVQaQya4fH1"
CONSUMER_SECRET="SUZK3xOyW4DJzY0rqr8pr2PQuVjEjEPgUNd73fMYd5eXSg4sY9"

twitter = Twitter (
	auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
) 

app = Flask(__name__)

@app.route('/', methods=['POST'])
def form_input():
	if request.method == 'POST':
		screen_name = request.form['screen_name']
		location = request.form['location']

	user_tweets = twitter.statuses.user_timeline(count=10, screen_name=screen_name)

	# app.logger.debug(itpTweets)

	templateData = {
		'screen_name' : '{} last 10 tweets'.format(screen_name),
		'user_tweets' : user_tweets,
	}

	return flask.render_template("result.html", **templateData)

@app.route('/')

def main():
	return flask.render_template("index.html")

if __name__ == '__main__':
	app.debug=True
	app.run()

