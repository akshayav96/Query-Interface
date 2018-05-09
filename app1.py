from flask import *
import pandas as pd
app = Flask(__name__)
import pickle 
from flask import *
import pandas as pd
app = Flask(__name__)
from pmidresults import get_pmid_results
from functools import reduce
from tfidf_files import do_search
from tfidf_files import similarity
from tfidf_files import tokenize
from tfidf_files import intersection
from langmodel import query_language_model

with open("freqdoc.dat","rb") as File:
      freqdoc = pickle.load( File)

with open("idf.dat", "rb") as File:
      idf = pickle.load(File)

with open ("len_doc.dat", "rb") as File:
    len_doc = pickle.load(File)

with open("stopwords.dat","rb") as file:
     stop_words= pickle.load(file)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/',  methods=['GET','POST'] )
def show_tables():
	table1 = pd.dataframe()
	if request.method == 'POST':
		text = request.form['text']
		results = do_search(text)
		for i in results:
			table1.append(get_pmid_results(i))
		return render_template('view.html', table=[table1.to_html(classes='table1')], title = ['TFIDF table'])


if __name__ == "__main__":
    app.run(debug=True)