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

def save_csv(handles, count, csv_path):
    data_csv = pd.DataFrame(columns=['News','Tweets'])
    data_csv['News']=handles
    data = []
    for handle in handles:
        user_tl = twitter.statuses.user_timeline(screen_name=handle, count=count,tweet_mode="extended")
        text = []
        for tw in user_tl:
            if not tw['in_reply_to_status_id']:
                text.append(tw['full_text'].encode("utf-8"))
        data.append(text)
    data_csv['Tweets']=data
    data_csv.to_csv(csv_path)
    return data_csv

"""
url_L = 'https://www.allsides.com/media-bias/media-bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=2&title='
url_L2 = 'https://www.allsides.com/media-bias/media-bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=2&title=&page=1'
url_R = 'https://www.allsides.com/media-bias/media-bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=4&title='
url_C = 'https://www.allsides.com/media-bias/media-bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=3&title='


left_news = get_list(url_L)
left_news = left_news + get_list(url_L2)
right_news = get_list(url_R)
center_news = get_list(url_C)

left_handles = get_screen_names(left_news)
right_handles = get_screen_names(right_news)
center_handles = get_screen_names(center_news)

count = 5000
csv_left = save_csv(left_handles, count,'../data/left1.csv')
csv_right = save_csv(right_handles, count,'../data/right1.csv')
csv_center = save_csv(center_handles, count,'../data/center1.csv')

print("all done!")
"""
save_csv(['snoiboi'],1000,'../data/sample_sonia.csv')
