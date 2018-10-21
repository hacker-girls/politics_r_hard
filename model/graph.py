import pandas as pd

right_buzz = ['snowflake','MAGA','PC','illegals','pro-life','buildthewall','wall','LiberalLogic','Hoax','istandwithbrett','alllivesmatter','bluelivesmatter','antifa','red','tax cut','win','puppet','fake news']
left_buzz = ['metoo','lovewins','notmypresident','pro-choice','LGBT','reform','familiesbelongtogether','abolishICE','blacklivesmatter','nobannowall','marchforourlives','gun control','imwithher','feelthebern']

rightb = 0
leftb = 0

user_df = pd.read_csv('../data/samples/sample_trump.csv')

print user_df['Tweets']
for tweets in user_df['Tweets']:
#    print tweets
    print('\n\n')
    for word in right_buzz:
        if word.lower() in tweets.lower():
            rightb = rightb + 1
    for word in left_buzz:
        if word in tweets:
            leftb = leftb + 1

print rightb
print leftb
            
