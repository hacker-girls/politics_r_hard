import flask
import twitter
from flask import Flask, request, render_template
from twitter import *
import json
import requests
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix

OAUTH_TOKEN="2464717370-ztIheNqKFIr9ll1ZG3OEa1SxRPTGY8k1XL3Ukj0"
OAUTH_SECRET="doEQPqBTLo22FrakNfY2q3jdLJyary6TFcLT8sv8AJes7"
CONSUMER_KEY="0J1e4CLZOLJTG1fVQaQya4fH1"
CONSUMER_SECRET="SUZK3xOyW4DJzY0rqr8pr2PQuVjEjEPgUNd73fMYd5eXSg4sY9"

twitter = Twitter (
	auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
)

def model(user_df):

        total_df = pd.read_csv('./data/total.csv')
        stop_words = set(stopwords.words('english'))

        def pre_process(mess):
                mess = nltk.word_tokenize(mess)
                clean = [word.lower() for word in mess if word.lower() not in stop_words]
                return clean

        def piped_vect(X,y,user_x):
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
                text_clf = Pipeline([('vect', CountVectorizer(analyzer=pre_process,encoding='utf-8',strip_accents=['ascii','unicode'],max_df=0.8,min_df=0.3)),('tfidf',TfidfTransformer()),('clf', MultinomialNB()),])
                text_clf = text_clf.fit(X_train, y_train)
                predicted = text_clf.predict(user_x)
                return predicted

        pred = piped_vect(total_df['Tweets'],total_df['pol'],user_df['Tweets'])
        return pred

def gen_Graph(user_df):
        right_buzz = ['snowflake','MAGA','PC','illegals','pro-life','buildthewall','wall','LiberalLogic','Hoax','istandwithbrett','alllivesmatter','bluelivesmatter','antifa','red','tax cut','win','puppet','fake news']
        left_buzz = ['metoo','lovewins','notmypresident','pro-choice','LGBT','reform','familiesbelongtogether','abolishICE','blacklivesmatter','nobannowall','marchforourlives','gun control','imwithher','feelthebern']

        rightb = 0
        leftb = 0

        for tweets in user_df['Tweets']:
                for word in right_buzz:
                        if word.lower() in tweets.lower():
                                rightb = rightb + 1
                for word in left_buzz:
                        if word in tweets:
                                leftb = leftb + 1


        return rightb,leftb


app = Flask(__name__)

@app.route('/', methods=['POST'])


def form_input():
	if request.method == 'POST':
		screen_name = request.form['screen_name']
		location = request.form['location']

	# user_tweets = twitter.statuses.user_timeline(count=1000, screen_name=screen_name)

	data = {'Sources': [], 'Tweets': []}
	data['Sources'].append(screen_name)

	tlist = []

	for t in twitter.statuses.user_timeline(count=1000, screen_name=screen_name, tweet_mode="extended"):
		tlist.append(t['full_text'].encode("utf-8"))
	data['Tweets'].append(tlist)

	df = pd.DataFrame(data, columns=['Sources', 'Tweets'])

	# app.logger.debug(itpTweets)

	    #DF IS THE IMPORTANT DATAFRAME
	    #DF->MODEL
	pred = model(df)

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
			'pred' : pred,
			'election': election,
			'contest_type' : contest_type,
			'contest_office_federal' : contest_office_federal,
			'contest_office_state' : contest_office_state,
			'contest_office_local' : contest_office_local,
			'contest_candidates_federal' : contest_candidates_federal,
			'contest_candidates_state' : contest_candidates_state,
			'contest_candidates_local' : contest_candidates_local,
			'polling_places_list' : polling_places,
			'early_vote_sites_list' : early_vote_sites_list,
                'repubhit' : repubhit, #help what r the spacing
                'demhit' : demhit
		}

	return flask.render_template("result.html", **templateData)

@app.route('/')

def main():
	return flask.render_template("index.html")

if __name__ == '__main__':
	app.debug=True
	app.run()
