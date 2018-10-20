import pandas as pd
import os

path = 'data/political-social-media-posts/political_social_media.csv'
data = pd.read_csv(path)

data = data.drop(['_golden','_unit_state','orig__golden','audience_gold','bias_gold','message_gold'],axis=1)

for c in data.columns:
    print c

#how the hell am i supposed to know who the id corresponds to

