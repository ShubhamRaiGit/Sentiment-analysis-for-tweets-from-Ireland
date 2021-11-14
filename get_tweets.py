import tweepy
import pandas as pd
import json
import nltk
from nltk.corpus import words
from nltk.corpus import stopwords

nltk.download('stopwords')
consumer_key = 't1JTH5TvboQRstLSwsk0J6s6x'
consumer_secret = 'xlzrpRpmUvTOy2aMOBtbeIOTgDzGl7w3ECfdFtbtScJosYASts'

access_token = '1401122885234683907-JLbGjZb46tNOx5uREIYjZTR0X5c9j9'
access_token_secret = 'gAU9oC8RDHiSnJE2Gq52XAc0wg714370z8HdgslKSXrD2'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
search_string = 'Dune OR Venom'


def get_data(search_string):
    api = tweepy.API(auth, wait_on_rate_limit=True)
    tweet_lst = []
    geoc = '53.350140,-6.266155,200mi'
    for tweet in tweepy.Cursor(api.search_tweets, q=search_string, geocode=geoc, lang="en", result_type='recent',
                               include_entities=True, tweet_mode='extended').items(10):
        tweetDate = tweet.created_at.date()
        twe = json.dumps(tweet._json)
        parsed = json.loads(twe)
        tweet_lst.append(parsed["full_text"])
    cleaned_df = clean_tweet_text(tweet_lst)
    return cleaned_df


def clean_tweet_text(tweet_list_item):
    Word = list(set(words.words()))
    df = pd.DataFrame(tweet_list_item, columns=['text'])
    df["text"] = df["text"].str.replace(r'\n', ' ', regex=True)
    df["text"] = df["text"].str.replace('&amp', ' ')
    df["text"] = df["text"].str.replace(',', ' ')
    df["text"] = df["text"].str.replace('.', ' ')
    df["text"] = df["text"].str.replace('#', ' ')
    df["text"] = df["text"].str.replace(r'@[\w]+', ' ', regex=True)
    df["text"] = df["text"].str.replace(r'http\S+', ' ', regex=True)
    df = df[df['text'].str.contains('|'.join(Word))]
    stop_words = stopwords.words('english')
    df['text'] = df['text'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
    return df


