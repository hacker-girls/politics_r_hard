import twitter
<<<<<<< HEAD
<<<<<<< HEAD
from twitter import *
import pandas as pd

=======
from flask import Flask, request, render_template
from twitter import *
import json
import urllib.request
import pandas as pd

data = {'Sources': [], 'Tweets': []}

>>>>>>> 4f6f0b3a47af5efed2942723b1b14cdd6830f15a
=======
from twitter import *
import pandas as pd

>>>>>>> 1479e5eadaa846d1900dbcd18aa869421144fcb8
OAUTH_TOKEN="2464717370-ztIheNqKFIr9ll1ZG3OEa1SxRPTGY8k1XL3Ukj0"
OAUTH_SECRET="doEQPqBTLo22FrakNfY2q3jdLJyary6TFcLT8sv8AJes7"
CONSUMER_KEY="0J1e4CLZOLJTG1fVQaQya4fH1"
CONSUMER_SECRET="SUZK3xOyW4DJzY0rqr8pr2PQuVjEjEPgUNd73fMYd5eXSg4sY9"

twitter = Twitter (
	auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
) 

<<<<<<< HEAD
<<<<<<< HEAD
=======
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
=======
>>>>>>> 1479e5eadaa846d1900dbcd18aa869421144fcb8
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

<<<<<<< HEAD
<<<<<<< HEAD
=======
page_link = 'https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress'
page_response = requests.get(page_link, timeout=5)
page_content = BeautifulSoup(page_response.content, "html.parser")

tables = page_content.find_all('table', {'class':'wikitable sortable jquery-tablesorter'})
for table in tables:
	rows = table.find_all('tr')
	for i in range(1, len(rows)):
		elements = rows[i].find_all('td')
		name = elements[0].getText().strip('\n')
		party = elements[3].getText().strip('\n\t\t\t\t\t')
		
		result_accts = twitter.users.search(q = name)

		try:
			acct = result_accts[0]
			if acct["verified"] == True:
				if party == 'Democratic Party' or party == 'Independent':
					ldata['Sources'].append(name)
					tlist = []
					for t in twitter.statuses.user_timeline(count=2000, screen_name=acct["screen_name"]):
						tlist.append(t['text'])
					ldata['Tweets'].append(tlist)
				else:
					rdata['Sources'].append(name)
					tlist = []
					for t in twitter.statuses.user_timeline(count=2000, screen_name=acct["screen_name"]):
						tlist.append(t['text'])
					rdata['Tweets'].append(tlist)

		except IndexError:
			pass

ldf = pd.DataFrame(ldata, columns=['Sources', 'Tweets'])
ldf.to_csv('left_cong_tweets.csv')

rdf = pd.DataFrame(rdata, columns=['Sources', 'Tweets'])
rdf.to_csv('right_cong_tweets.csv')
>>>>>>> 4f6f0b3a47af5efed2942723b1b14cdd6830f15a
=======
>>>>>>> 1479e5eadaa846d1900dbcd18aa869421144fcb8
=======
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
>>>>>>> 1c42f84a7d9ad41e55f6834817f226400b4e61c2

>>>>>>> natalie
