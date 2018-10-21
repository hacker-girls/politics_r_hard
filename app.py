import flask
import twitter
from flask import Flask, request, render_template
from twitter import *
import json
import requests

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

	user_tweets = twitter.statuses.user_timeline(count=1, screen_name=screen_name)

	# app.logger.debug(itpTweets)

	address = location

	params = {
		'address': address,
	}

	r = requests.get("https://www.googleapis.com/civicinfo/v2/voterinfo?key=AIzaSyCDTh1Io4GW47gv12B5cEqOV6uA93Hx6Ew", params=params)
	data = r.json()
	election = data['election']['name']
	contests = data['contests']
	contest_type = []
	contest_office_federal = []
	contest_office_state = []
	contest_office_local = []
	contest_candidates_federal = []
	contest_candidates_state = []
	contest_candidates_local = []
	for contest in contests:
		if 'type' in contest:
			contest_type.append(contest['type'])
		if 'level' in contest:
			if 'country' in contest['level']:
				contest_office_federal.append(contest['office'])
				for c in contest['candidates']:
					if c['party'] == 'Democratic Party':
						partyColor = 'blue'
					elif c['party'] == 'Republican Party':
						partyColor = 'red'
					else:
						partyColor = 'grey'

					splitName = c['name'].split();
					formattedName = splitName[0] + "%20" + splitName[1]
					imgRequest = requests.get("https://en.wikipedia.org/w/api.php?action=query&titles=" + formattedName + "&format=json&prop=pageimages&formatversion=2")
					imgData = imgRequest.json()
					if 'thumbnail' in imgData['query']['pages'][0]:
						imgUrl = imgData['query']['pages'][0]['thumbnail']['source']
						contest_candidates_federal.append({'name': c['name'], 'office': contest['office'], 'imgUrl': imgUrl, 'partyColor': partyColor})
					else:
						contest_candidates_federal.append({'name': c['name'], 'office': contest['office'], 'imgUrl': 'https://freeiconshop.com/wp-content/uploads/edd/person-solid.png', 'partyColor': partyColor})
			elif 'administrativeArea1' in contest['level']:
				contest_office_state.append(contest['office'])
				for c in contest['candidates']:
					if c['party'] == 'Democratic Party':
						partyColor = 'blue'
					elif c['party'] == 'Republican Party':
						partyColor = 'red'
					else:
						partyColor = 'grey'

					splitName = c['name'].split();
					formattedName = splitName[0] + "%20" + splitName[1]
					imgRequest = requests.get("https://en.wikipedia.org/w/api.php?action=query&titles=" + formattedName + "&format=json&prop=pageimages&formatversion=2")
					imgData = imgRequest.json()
					if 'thumbnail' in imgData['query']['pages'][0]:
						imgUrl = imgData['query']['pages'][0]['thumbnail']['source']
						contest_candidates_state.append({'name': c['name'], 'office': contest['office'], 'imgUrl': imgUrl, 'partyColor': partyColor})
					else:
						contest_candidates_state.append({'name': c['name'], 'office': contest['office'], 'imgUrl': 'https://freeiconshop.com/wp-content/uploads/edd/person-solid.png', 'partyColor': partyColor})
			else:
				contest_office_local.append(contest['office'])
				for c in contest['candidates']:
					if c['party'] == 'Democratic Party':
						partyColor = 'blue'
					elif c['party'] == 'Republican Party':
						partyColor = 'red'
					else:
						partyColor = 'grey'

					splitName = c['name'].split();
					formattedName = splitName[0] + "%20" + splitName[1]
					imgRequest = requests.get("https://en.wikipedia.org/w/api.php?action=query&titles=" + formattedName + "&format=json&prop=pageimages&formatversion=2")
					imgData = imgRequest.json()
					if 'thumbnail' in imgData['query']['pages'][0]:
						imgUrl = imgData['query']['pages'][0]['thumbnail']['source']
						contest_candidates_local.append({'name': c['name'], 'office': contest['office'], 'imgUrl': imgUrl, 'partyColor': partyColor})
					else:
						contest_candidates_local.append({'name': c['name'], 'office': contest['office'], 'imgUrl': 'https://freeiconshop.com/wp-content/uploads/edd/person-solid.png', 'partyColor': partyColor})

	templateData = {
			'screen_name' : '{} last 10 tweets'.format(screen_name),
			'user_tweets' : user_tweets,
			'election': election,
			'contest_type' : contest_type,
			'contest_office_federal' : contest_office_federal,
			'contest_office_state' : contest_office_state,
			'contest_office_local' : contest_office_local,
			'contest_candidates_federal' : contest_candidates_federal,
			'contest_candidates_state' : contest_candidates_state,
			'contest_candidates_local' : contest_candidates_local
		}

	return flask.render_template("result.html", **templateData)

@app.route('/')

def main():
	return flask.render_template("index.html")

if __name__ == '__main__':
	app.debug=True
	app.run()

