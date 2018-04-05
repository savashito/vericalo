from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from flask import Flask
from flask import request
from flask_cors import CORS
import sys

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

if __name__ == '__main__':
    analyze("I am a good person that borns people for fun and feeds their wifes because they are pretty and valuable")
    app.run(host= '0.0.0.0')
