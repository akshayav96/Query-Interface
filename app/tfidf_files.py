import pickle 
from collections import defaultdict
import math
import pandas as pd
from functools import reduce

characters = " -.,!#$%^&*();:\n\t\\\"?!{}[]<>/"

with open("freqdoc.dat","rb") as File:
      freqdoc = pickle.load( File)

with open("idf.dat", "rb") as File:
      idf = pickle.load(File)

with open ("len_doc.dat", "rb") as File:
    len_doc = pickle.load(File)




with open("stopwords.dat","rb") as file:
     stop_words= pickle.load(file)


def similarity(query_user,i):
    """Returns the cosine similarity between query and document id.
    Note that we don't bother dividing by the length of the query
    vector, since this doesn't make any difference to the ordering of
    search results."""
   
    similarity = 0.0
    
    
    for term in query_user: 
        tf1 = query_user.count(term)            #frequency of term in query
        idf1 = idf [term].values                          #idf of term in query
        tfidf_query = tf1*idf1                  #tfidf vector of query 
        tfidf_doc = freqdoc[term][i]*idf[term].values    #tfidf vector of the document
        similarity += tfidf_query*tfidf_doc
    similarity = similarity / len_doc[i]
    return similarity

def do_search(queryinput):
    """Asks the user what they would like to search for, and returns a
    list of relevant documents, in decreasing order of cosine
    similarity."""
    idlist =[]
    query_user = tokenize(queryinput)
    if query_user == []:
        sys.exit()
    # find document ids containing all query terms.  Works by
    # intersecting the posting lists for all query terms.
    relevant_document_ids = intersection(
            [set(freqdoc[term].keys()) for term in query_user])
    if not relevant_document_ids:
        print( "No documents matched all query terms.")
    else:
        scores = sorted([(i,similarity(query_user,i))
                         for i in relevant_document_ids],
                                key=lambda x: x[1],
                                reverse=True)
        #print ("Score: filename")
        for (i,score) in scores:
            idlist.append(i)
        return idlist[:20]

def intersection(sets):
    """Returns the intersection of all sets in the list sets. Requires
    that the list sets contains at least one element, otherwise it
    raises an error."""
    return reduce(set.intersection, [s for s in sets])

def tokenize(document):

    """Returns a list whose elements are the separate terms in
    document.  Something of a hack, but for the simple documents we're
    using, it's okay.  Note that we case-fold when we tokenize, i.e.,
    we lowercase everything."""
    terms = document.lower().split()
    return [term.strip(characters) for term in terms if term not in stop_words]

