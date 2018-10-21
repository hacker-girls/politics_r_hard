#main
from scripts.tweet_scripts import *

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
csv_left = save_csv(left_handles, count,'./data/ltest.csv')
csv_right = save_csv(right_handles, count,'./data/rtest.csv')
csv_center = save_csv(center_handles, count,'./data/ctest.csv')
