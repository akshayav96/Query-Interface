from flask import *
import pandas as pd
app = Flask(__name__)
import pickle
from flask import *
import pandas as pd
app = Flask(__name__)
from get_pmid_results import *
from functools import reduce
from tfidf_files import do_search
from tfidf_files import similarity
from tfidf_files import tokenize
from tfidf_files import intersection
from query_language_model import *

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
	table1 = pd.DataFrame()
	if request.method == 'POST':
		text = request.form['text']
		results1 = do_search(text)
		females = get_pmid_results(results1)
		results2 = query_language_model(text)
		males = get_pmid_results(results2)
		return render_template('view.html',tables=[females.to_html(classes='female'), males.to_html(classes='male')], titles = ['na', 'TF-IDF', 'Language Model'])



if __name__ == "__main__":
    app.run(debug=True)
