from flask import *
import pandas as pd
app = Flask(__name__)
import pickle
from get_pmid_results import *
from functools import reduce
from tfidf_model.tfidf_files import *
from language_model.query_language_model import *


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/',  methods=['GET','POST'] )
def show_tables():
	table1 = pd.DataFrame()
	if request.method == 'POST':
		text = request.form['text']
		results1 = do_search(text)
		tfidf_df = get_pmid_results(results1)[1]
		results2 = query_language_model(text)
		lm_df = get_pmid_results(results2)[1]
		results3 = query_language_model(text)
		vsm_df = get_pmid_results(results3)[1]
		return render_template('view.html',tables=[tfidf_df.to_html(classes='tfidf'), lm_df.to_html(classes='lm'), vsm_df.to_html(classes='vsm')], titles = ['na', 'TF-IDF', 'Language Model', 'Vector Space Model'])



if __name__ == "__main__":
    app.run(debug=True)
