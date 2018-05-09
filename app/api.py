import flask
from flask import request, jsonify, render_template,redirect,url_for
from wtforms import Form, StringField, SelectField
from forms import SearchForm
import pickle 
from collections import defaultdict
import math
import pandas as pd
from functools import reduce
from tfidf_files import do_search
from tfidf_files import similarity
from tfidf_files import tokenize
from tfidf_files import intersection
from langmodel import query_language_model



app = flask.Flask(__name__)
app.config["DEBUG"] = True


# with open("Dict.dat","rb") as file:
#     dictionary = pickle.load(file)

with open("freqdoc.dat","rb") as File:
      freqdoc = pickle.load( File)

with open("idf.dat", "rb") as File:
      idf = pickle.load(File)

with open ("len_doc.dat", "rb") as File:
    len_doc = pickle.load(File)

with open("stopwords.dat","rb") as file:
     stop_words= pickle.load(file)

with open('language_model.pickle', 'rb') as handle:
    lm_dict = pickle.load(handle)
    


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/', methods=['GET','POST'] )
def index():
    #result =[]
    #name = SearchForm()
    #form = SearchForm()
    if request.method == 'POST':

        text = request.form['text']

        return jsonify( query_language_model(text))
        #return result 
        #model1 = do_search(text)

    


@app.route('/pmid', methods=['GET'])
def id():
#     # Check if an ID was provided as part of the URL.
#     # If ID is provided, assign it to a variable.
#     # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
       id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."
    results = []
    """ query the respective database table and obtain the results as dataframe.let's say we have a dataframe df with id, author,journal etc.,"""
    if df['id'] == id:
        results.append(df[id])
    return jsonify(results)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()


