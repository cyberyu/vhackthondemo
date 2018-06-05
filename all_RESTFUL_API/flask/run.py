__author__ = 'shiyu'

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import pickle
import sys
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer


app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

def Preprocess(text):
    tokens = word_tokenize(text)
    tokens = [t.lower() for t in tokens]
    stops = stopwords.words('english')
    tokens = [t for t in tokens if t  not in stops]
    pst = PorterStemmer()
    tokens = [pst.stem(t) for t in tokens]
    text = ' '.join(tokens)
    return text

def Predict(comment):
    processedComment = Preprocess(comment)
    f = open('v.pickle','rb')
    vectorizer = pickle.load(f)
    f = open('m.pickle','rb')
    model = pickle.load(f)


    X = vectorizer.transform([processedComment,]).toarray()
    ans = int(model.predict(X))
    return ans

def initialize():
    global refComment, vectorizedFit, vectorizedRefComment

    refComment = "2008 ETF accept account advice age aggressive allocation amount asset averse balance bank bear bitcoin black bond brokerage bubble budget bull buy cash cautious collapse \
    comfortable commission concern conservative contribute coin cost credit currency debt decline dip distribute diversify dividend dollar down downturn dow \
    earn economy equity euro expense exposure fall fear fluctuation frugal fund gain grow high hold hundred income increase index inflation invest loan long lose loss \
    low lower market maximum medium middle million minimum moderate money mutual nasdaq net old owe person portfolio position price principal profit \
    rally ratio reinvest recession red retirement return revenue rise risk safe save securities sell share spend stable stock s&p tax term thousand thrifty tolerance trade \
    unbalanced up value volatile vanguard wallet worry worth yen yield young"

    refComment = Preprocess(refComment)

    vectorizer = CountVectorizer(min_df=1,ngram_range=(1,1))

    vectorizedFit = vectorizer.fit([refComment,])

    vectorizedRefComment = vectorizedFit.transform([refComment,])


def Detect_topic(comment):
    global vectorizedFit,  vectorizedRefComment

    initialize()

    processedComment = Preprocess(comment)
    vectorizedTestComment = vectorizedFit.transform([processedComment,])
    result = ((vectorizedRefComment * vectorizedTestComment.T).A)[0][0]

    if result < 2:
        return 'off topic'
    else:
        return 'on topic'


class HelloWorld(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Email address to create user')
        parser.add_argument('password', type=str, help='Password to create user')

        args = parser.parse_args()

        #json_data = request.get_json(force=True)


        un = str(args['name'])
        pw = str(args['password'])
        #args = parser.parse_args()
        #un = str(args['username'])
        #pw = str(args['password'])
        return jsonify(u=un, p=pw)

class classify(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('textinput', type=str)
        args = parser.parse_args()
        txtinput = str(args['textinput'])
    	info = Predict(txtinput)
        print txtinput
        print info
	return jsonify(y=info)


class topicfy(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('textinput', type=str)
        args = parser.parse_args()
        txtinput = str(args['textinput'])
    	info = Detect_topic(txtinput)
        #print txtinput
        #print info
	return jsonify(y=info)


api.add_resource(classify, '/clsfy')
api.add_resource(topicfy, '/tpcfy')
api.add_resource(HelloWorld, '/testing')


if __name__ == '__main__':

    #print Predict("I like to play it safe")
    # #
    #print Predict("I like to take risk")
    #
    #print Predict("I want high risk ")
    # #
    #print "I want low risk "+ str(Predict("I want low risk "))
    app.run(host='0.0.0.0', debug=True, port=5001)
