import sys
import six

import tweepy, config
from googletrans import Translator
from textblob import TextBlob
translator = Translator()

class MyStreamListener(tweepy.StreamListener):

  def on_status(self, status):
    date = get_date_as_string(status.created_at)
    print (date, status.text.encode('utf-8').strip())
    return

def get_date_as_string(date, format = "%a, %d %b %Y %H:%M:%S"):
    return date.strftime(format)

def get_sentiment(text):
    tr = translator.translate(text)
    wiki = TextBlob(tr.text)
    return wiki.sentiment,tr.text

def get_author_influence(author):
    infl = author.followers_count + author.statuses_count + author.friends_count
    return infl

def get_tweet_influence(t):
    infl = t.retweet_count + t.favorite_count
    return infl

def get_hash_tags(t):
    hs = t.entities['hashtags']
    if(len(hs) > 0):
        hs = hs[0]['text']
    else:
        return None
    return hs

def get_image(t):
    media = t.entities['media']
    if(len(media)>0):
        hs = media[0]['media_url_https']
    else:
        hs = None
    return hs

def get_retweets_ids(id):
    results = api.retweets(id)
    ids = []
    for i in range(len(results)):
        ids.append(results[i].id)
    return ids

class Tweet():

    def __init__(self,id,api):
        tweet = api.statuses_lookup([id])
        t = tweet[0]
        self.image = get_image(t)
        self.api = api
        self.text = t.text
        self.influence = get_tweet_influence(t)
        self.hashtags = get_hash_tags(t)
        self.retweets = t.retweet_count
        self.author_influence = get_author_influence(t.author)
        self.sentiment,self.etext = get_sentiment(t.text)
        self.retweets_ids =  get_retweets_ids(id)

    def printy(self):
        print("text: "+self.etext)
        print("influence: " + str(self.influence))
        print("hashtags: " +  str(self.hashtags))
        print("author_influence: " + str(self.author_influence))
        print("sentiment: " + str(self.sentiment))
        print("retweets_ids: " + str(self.retweets_ids))
        print("retweets: " + str(self.retweets))

    def json(self):
        o = {"text":self.text,
            "etext":self.etext,
            "author_influence":self.author_influence,
            "shares":self.retweets,
            "interacciones":self.retweets,
            "interPos":None,
            "interNeg":None,

            "percentFuenteFalsa":None,
            "percentFuenteTemaFalsa":None,
            "percentTemaFalsa":None,
            "image":self.image
            }
        print (o)

    def get_retweets(self):
        tweets = []
        for i in range(len(self.retweets_ids)):
            id = self.retweets_ids[i]
            print (id)
            tweet = Tweet(id,self.api)
            tweet.printy()

    def get_virality_array(self):
        return [ self.influence , 10, 30 , self.retweets, [], self.image, None]


auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

words = ["#amlo"]
streamListener = MyStreamListener()
stream = tweepy.Stream(auth=api.auth,listener = streamListener)
stream.filter(track=words,async = False)

if __name__ == '__main__':
    id = 979825600973094912
    tw = Tweet(id,api)
    print (tw.json())
