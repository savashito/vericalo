from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from flask import Flask
from flask import request
from flask_cors import CORS
import sys
import six

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    content = request.args.get('content')
    result = analyze(content)
    return result

def analyze_categories(categories, verbose=True):
    result = {}
    for category in categories:
        result[category.name] = category.confidence
    if verbose:
        for category in categories:
            print(u'=' * 20)
            print(u'{:<16}: {}'.format('category', category.name))
            print(u'{:<16}: {}'.format('confidence', category.confidence))
    return result

def analyze_sentiment(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude
    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}'.format(
            index, sentence_sentiment))
    print('Overall Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))
    return 0

def analyze(content):
    document = types.Document(content=content, type=enums.Document.Type.PLAIN_TEXT)
    client = language.LanguageServiceClient()
    try:
        annotations = client.analyze_sentiment(document=document)
        analyze_sentiment(annotations)
    except:
        print(sys.exc_info()[0])
    try:
        response = client.classify_text(document)
        categories = response.categories
        analyze_categories(categories)
    except:
        print(sys.exc_info()[0])
    return "OK"
def entities_text(text):
    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    for entity in entities:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
        print(u'{:<16}: {}'.format('metadata', entity.metadata))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))
def sentiment_text(text):
    """Detects sentiment in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects sentiment in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    sentiment = client.analyze_sentiment(document).document_sentiment

    print('Score: {}'.format(sentiment.score))
    print('Magnitude: {}'.format(sentiment.magnitude))
def syntax_text(text):
    """Detects syntax in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    tokens = client.analyze_syntax(document).tokens

    # part-of-speech tags from enums.PartOfSpeech.Tag
    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

    for token in tokens:
        print(u'{}: {}'.format(pos_tag[token.part_of_speech.tag],
                               token.text.content))

def entity_sentiment_text(text):
    """Detects entity sentiment in the provided text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)

    # Detect and send native Python encoding to receive correct word offsets.
    encoding = enums.EncodingType.UTF32
    if sys.maxunicode == 65535:
        encoding = enums.EncodingType.UTF16

    result = client.analyze_entity_sentiment(document, encoding)
    max_sal = 0
    max_word = ""
    sentiment = 0
    for entity in result.entities:
        # print('Mentions: ')
        # print(u'Name: "{}"'.format(entity.name))
        for mention in entity.mentions:
            print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
            print(u'  Content : {}'.format(mention.text.content))
            print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
            print(u'  Sentiment : {}'.format(mention.sentiment.score))
            print(u'  Type : {}'.format(mention.type))
        # print(u'Salience: {}'.format(entity.salience))
        # print(u'Sentiment: {}\n'.format(entity.sentiment))
        #sentiment = sentiment + entity.sentiment
        # print salience
        # print entity.salience
        # print entity
        print (entity.text.content)
        print (entity.salience)
        # print 
        if(max_sal<entity.salience):
            max_sal = entity.salience
            max_word = mention
    print "Most important is {}".format(max_word)
    print "sentiment "+str(sentiment)


def classify_text(text):
    """Classifies content categories of the provided text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)

    categories = client.classify_text(document).categories

    for category in categories:
        print(u'=' * 20)
        print(u'{:<16}: {}'.format('name', category.name))
        print(u'{:<16}: {}'.format('confidence', category.confidence))
###########


import tweepy, config
from googletrans import Translator
from textblob import TextBlob
translator = Translator()



# class MyStreamListener(tweepy.StreamListener):
#   def on_status(self, status):
#       print(status.text)
#       print (status)
#       # print ()
#       id = status.id
#       tw = tweepy.API.statuses_lookup(id)
#       print(tw)
#       return
#       tr = translator.translate(status.text)
#       print(tr.text)
#       wiki = TextBlob(tr.text)
#       print(wiki.sentiment)
#       # tweepy.API.statuses_lookup(id_[, include_entities][, trim_user][, map_])

def get_sentiment(text):
    tr = translator.translate(text)
    # print(tr.text)
    wiki = TextBlob(tr.text)
    # print(wiki.sentiment)
    return wiki.sentiment,tr.text
def get_author_influence(author):
    infl = author.followers_count+author.statuses_count+author.friends_count
    # print("Author influence "+str(infl))
    return infl
def get_tweet_influence(t):
    infl = t.retweet_count + t.favorite_count
    # print("Tweet influence "+str(infl))
    return infl
def get_hash_tags(t):
    hs = t.entities['hashtags']
    if(len(hs) > 0):
        hs = hs[0]['text']
    else:
        return None
    # print(hs)
    return hs
def get_image(t):
    # hs = t.media['media_url_https']
    # hs = t.entities['media_url_https']
    media = t.entities['media']
    if(len(media)>0):
        hs = media[0]['media_url_https'] # ["media_url"] #media_url_https
    else:
        hs = None
    return hs
def get_retweets_ids(id):
    results = api.retweets(id)
    ids = []

    for i in range(len(results)):
        ids.append(results[i].id)
    # print(len(results))
    # print(ids)
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
        # print(self.sentiment)

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
            "tema1":{"val":"","imp":""},

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
        # return [ self.influence , 10, 30 , self.retweets, fuentes, self.image, estados]
        # return None

# get_sentiment("malo malo malo ratero")
# get_sentiment("es un buen ratero")
# exit()
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

# [ 10032 , 10%, 30 %, retweet, fuentes, foto, estados]

# tweepy
# 979825600973094912 parent
# 981300116844896259 random user
# 979833734957490176 jordy

# tw.get_retweets()
# print(tw.get_virality_array())


###########
if __name__ == '__main__':
    # text = "I am a good person that borns people for fun and feeds their wifes because they are pretty and valuable"
    # text = "#AMLO simulated sale of apartments in Copilco, reveals Pejeleaks https://goo.gl/if26pR"
    #analyze(text)
    #print("-> anal")
    #entities_text(text)
    #print("-> entiti")
    #sentiment_text(text)
    #print("-> senti")
    #syntax_text(text)
    #print("-> syntax")
    id = 979825600973094912
    tw = Tweet(id,api)
    tw.json()
    # print ("texto e "+tw.etext)
    # tw.printy()
    entity_sentiment_text(tw.etext)
    # print("-> enti_sent")
    #classify_text(text)
    #print("-> class")
    app.run(host= '0.0.0.0')
