import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
import get_tweets
import re

url_L = 'https://www.allsides.com/media-bias/media-bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=2&title='
url_L2 = 'https://www.allsides.com/media-bias/media-bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=2&title=&page=1'
url_R = 'https://www.allsides.com/media-bias/media-bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=4&title='
url_C = 'https://www.allsides.com/media-bias/media-bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=3&title='


def get_list(url):
    list = []
    response = get(url)
    html_soup = bs(response.text, 'html.parser')
    for title in html_soup.find_all("td", class_="views-field views-field-title source-title"):
        t = title.find_all('a',href=True)
        list.append(t[0].string.encode("utf-8"))
    return list

left_news = get_list(url_L)
left_news = left_news + get_list(url_L2)
right_news = get_list(url_R)
center_news = get_list(url_C)

#now to feed back into twitter oh jeez heres the hard stuff
OAUTH_TOKEN="2464717370-ztIheNqKFIr9ll1ZG3OEa1SxRPTGY8k1XL3Ukj0"
OAUTH_SECRET="doEQPqBTLo22FrakNfY2q3jdLJyary6TFcLT8sv8AJes7"
CONSUMER_KEY="0J1e4CLZOLJTG1fVQaQya4fH1"
CONSUMER_SECRET="SUZK3xOyW4DJzY0rqr8pr2PQuVjEjEPgUNd73fMYd5eXSg4sY9"

for name in left_news:
    print name
    t = Twitter(
    auth = OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
    user_handle = 
