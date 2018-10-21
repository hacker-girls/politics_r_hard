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

	# user_tweets = twitter.statuses.user_timeline(count=1000, screen_name=screen_name)
	
	data = {'Sources': [], 'Tweets': []}
	data['Sources'].append(twitter.users.lookup(handle))

	for t in twitter.statuses.user_timeline(count=1000, screen_name=handle, tweet_mode="extended"):
		tlist.append(t['full_text'].encode("utf-8"))
	data['Tweets'].append(tlist)

	df = pd.DataFrame(data, columns=['Sources', 'Tweets'])
	# app.logger.debug(itpTweets)

	address = location

	params = {
		'address': address,
	}

	r = requests.get("https://www.googleapis.com/civicinfo/v2/voterinfo?key=AIzaSyCDTh1Io4GW47gv12B5cEqOV6uA93Hx6Ew", params=params)
	data = r.json()
	election = data['election']['name']
	if 'pollingLocations' in data:
		polling_places = data['pollingLocations']
	else:
		polling_places = []
	polling_places_list = []
	if 'earlyVoteSites' in data:
		early_vote_sites = data['earlyVoteSites']
	else:
		early_vote_sites = []
	early_vote_sites_list = []
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

	for place in polling_places:
		polling_places_list.append({'name': place['address']['locationName'], 'street_address': place['address']['line1'], 'city': place['address']['city'], 'state': place['address']['state'], 'zip': place['address']['zip']})

	for site in early_vote_sites:
		early_vote_sites_list.append({'name': place['address']['locationName'], 'street_address': place['address']['line1'], 'city': place['address']['city'], 'state': place['address']['state'], 'zip': place['address']['zip']})


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
			'contest_candidates_local' : contest_candidates_local,
			'polling_places_list' : polling_places,
			'early_vote_sites_list' : early_vote_sites_list
		}

	return flask.render_template("result.html", **templateData)

@app.route('/')

def main():
	return flask.render_template("index.html")

if __name__ == '__main__':
	app.debug=True
	app.run()
