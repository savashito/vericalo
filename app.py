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

if __name__ == '__main__':
    entities_text("I am a good person that borns people for fun and feeds their wifes because they are pretty and valuable")
    app.run(host= '0.0.0.0')
