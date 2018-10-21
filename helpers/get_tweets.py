import twitter
from twitter import *
import pandas as pd

OAUTH_TOKEN="2464717370-ztIheNqKFIr9ll1ZG3OEa1SxRPTGY8k1XL3Ukj0"
OAUTH_SECRET="doEQPqBTLo22FrakNfY2q3jdLJyary6TFcLT8sv8AJes7"
CONSUMER_KEY="0J1e4CLZOLJTG1fVQaQya4fH1"
CONSUMER_SECRET="SUZK3xOyW4DJzY0rqr8pr2PQuVjEjEPgUNd73fMYd5eXSg4sY9"

twitter = Twitter (
	auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
) 

def get_verf_tweets(names):	

	data = {'Sources': [], 'Tweets': []}

	for name in names:
		result_accts = twitter.users.search(q = name)
		user_found = False

		for acct in result_accts:
			if acct["verified"] == True:
				user_found = True
				data['Sources'].append(name)
				tlist = []
				for t in twitter.statuses.user_timeline(count=2000, screen_name=acct["screen_name"]):
					tlist.append(t['text'])
				data['Tweets'].append(tlist)
				break

		if user_found:
			df = pd.DataFrame(data, columns=['Sources', 'Tweets'])

	return df

def get_handle_tweets(handle):

	data = {'Sources': [], 'Tweets': []}
	data['Sources'].append(twitter.users.lookup(handle))

	for t in twitter.statuses.user_timeline(count=2000, screen_name=handle):
				tlist.append(t['text'])
			data['Tweets'].append(tlist)

	return df

def get_tweets_db(name):	

	data = {'Sources': [], 'Tweets': []}

	result_accts = twitter.users.search(q = name)
	user_found = False

	for acct in result_accts:
		if acct["verified"] == True:
			user_found = True
			data['Sources'] = name
			tlist = []
			for t in twitter.statuses.user_timeline(count=2000, screen_name=acct["screen_name"]):
				tlist.append(t['text'])
			data['Tweets'].append(tlist)
			break

	if user_found:
		df = pd.DataFrame(data, columns=['Sources', 'Tweets'])
		return df

	return False

