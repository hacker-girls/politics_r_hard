import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix

def csv_to_df(pathname,val):
    df = pd.read_csv(pathname).drop(['Unnamed: 0'],axis=1)
    df = df.sample(frac=1).reset_index(drop=True) #shuffle it up
    df['pol'] = np.full((df.shape[0],1),val)
    return df


leftc = csv_to_df('../data/left_cong.csv',1)
leftc = leftc.rename(columns = {'Sources':'News'})
left = pd.concat([csv_to_df('../data/left1.csv',1),leftc],ignore_index=True)
rightc = csv_to_df('../data/right_cong.csv',-1)
rightc = rightc.rename(columns = {'Sources':'News'})
right = pd.concat([csv_to_df('../data/left1.csv',-1),rightc],ignore_index=True)
center = csv_to_df('../data/center1.csv',0)

print left.shape
print right.shape
print center.shape
total_df = pd.concat([left,center,right],ignore_index=True)
total_df = total_df.sample(frac=1).reset_index(drop=True)

stop_words = set(stopwords.words('english'))

def pre_process(mess):
    mess = nltk.word_tokenize(mess)
    clean = [word.lower() for word in mess if word.lower() not in stop_words]
    return clean

def vocab_length(total):
    sum_ = 0
    for row in total:
        sum_ += len(row)
    return sum_

def piped_vect(X,y,user_x):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)    
    text_clf = Pipeline([('vect', CountVectorizer(analyzer=pre_process,encoding='utf-8',strip_accents=['ascii','unicode'],max_df=0.8,min_df=0.3)),('tfidf',TfidfTransformer()),('clf', MultinomialNB()),])
    text_clf = text_clf.fit(X_train, y_train)
    predicted = text_clf.predict(user_x)
    print predicted
#    print (classification_report(y_test, predicted))

user_df = pd.read_csv('../data/samples/sample_sonia.csv')
piped_vect(total_df['Tweets'],total_df['pol'],user_df['Tweets'])
