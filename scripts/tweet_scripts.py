import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
from twitter import *


def get_list(url):
    list = []
    response = get(url)
    html_soup = bs(response.text, 'html.parser')
    for title in html_soup.find_all("td", class_="views-field views-field-title source-title"):
        t = title.find_all('a',href=True)
        list.append(t[0].string.encode("utf-8"))
    return list

#now to feed back into twitter oh jeez heres the hard stuff
OAUTH_TOKEN="2464717370-ztIheNqKFIr9ll1ZG3OEa1SxRPTGY8k1XL3Ukj0"
OAUTH_SECRET="doEQPqBTLo22FrakNfY2q3jdLJyary6TFcLT8sv8AJes7"
CONSUMER_KEY="0J1e4CLZOLJTG1fVQaQya4fH1"
CONSUMER_SECRET="SUZK3xOyW4DJzY0rqr8pr2PQuVjEjEPgUNd73fMYd5eXSg4sY9"
twitter = Twitter(
    auth = OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
def get_screen_names(list_news):
    handles = []
    for name in list_news:
        result_accts = twitter.users.search(q=name)
        for acct in result_accts:
            if acct["verified"] == True:
                handles.append(acct['screen_name'].encode("utf-8"))
                break
    return handles

def get_data(handle,count): 
    user_tl = twitter.statuses.user_timeline(screen_name=handle, count=count)
    text = []
    for tw in user_tl:
        if not tw['in_reply_to_status_id']:
            text.append(tw['text'])
    return text

def save_csv(handles, count, csv_path):
    data_csv = pd.DataFrame(columns=['News','Tweets'])
    data_csv['News']=handles
    data = []
    for handle in handles:
        user_tl = twitter.statuses.user_timeline(screen_name=handle, count=count)
        text = []
        for tw in user_tl:
            if not tw['in_reply_to_status_id']:
                text.append(tw['text'].encode("utf-8"))
        data.append(text)
    data_csv['Tweets']=data
    data_csv.to_csv(csv_path)
    return data_csv

