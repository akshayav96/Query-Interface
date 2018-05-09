from nltk.stem.snowball import SnowballStemmer
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
import pandas as pd

from scipy.stats import entropy


import pickle
import numpy as np

def query_language_model(query):
    #open the model - language_model file must be in the folder
    with open('language_model.pickle', 'rb') as handle:
        lm_dict = pickle.load(handle)

    pdf_vectors = np.asarray(lm_dict['pdf'].todense())

    #process the query
    q_terms = query.translate(str.maketrans(" ", " ", string.punctuation+'0123456789'))
    q_terms = [SnowballStemmer("english").stem(w) for w in word_tokenize(q_terms)]
    q_terms = [w for w in q_terms if not w in set(stopwords.words('english'))]
    query_vector = np.asarray(pd.Series(pd.Series(q_terms).value_counts(normalize = True), index = lm_dict['terms']).fillna(0.00001))

    #create vector only of term length
    subset = pdf_vectors[:,[lm_dict['terms'].index(i) for i in q_terms]]
    #subset - this keeps all of the records, with the original shape of the language model
    relevant = pdf_vectors[~(subset==0).all(1)]
    #subset - this keeps all of the records with the shape of the query language model
    #relevant = subset[~(subset==0).all(1)]

    contained_pmids = lm_dict['PMID'][np.nonzero(np.sum(subset, axis = 1))[0]]

    scores = {}
    for i, j in zip(np.arange(0, len(relevant),1), contained_pmids):
        scores[j] = entropy(relevant[i], query_vector)

    return sorted(scores, key=scores.get)[:20]
