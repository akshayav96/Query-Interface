# -*- coding:utf-8 -*-

import json

from flask import Flask, request, render_template
app = Flask(__name__)

app.debug = True

class BaseDataTables:

    def __init__(self, request, columns, collection):

        self.columns = columns

        self.collection = collection

        # values specified by the datatable for filtering, sorting, paging
        self.request_values = request.values


        # results from the db
        self.result_data = None

        # total in the table after filtering
        self.cardinality_filtered = 0

        # total in the table unfiltered
        self.cadinality = 0

        self.run_queries()

    def output_result(self):

        output = {}

        # output['sEcho'] = str(int(self.request_values['sEcho']))
        # output['iTotalRecords'] = str(self.cardinality)
        # output['iTotalDisplayRecords'] = str(self.cardinality_filtered)
        aaData_rows = []

        for row in self.result_data:
            aaData_row = []
            for i in range(len(self.columns)):
                print (row, self.columns, self.columns[i])
                aaData_row.append(str(row[ self.columns[i] ]).replace('"','\\"'))
            aaData_rows.append(aaData_row)

        output['aaData'] = aaData_rows

        return output

    def run_queries(self):

         self.result_data = self.collection
         self.cardinality_filtered = len(self.result_data)
         self.cardinality = len(self.result_data)

columns = [ 'column_1', 'column_2', 'column_3', 'column_4']

@app.route('/')
def index():
    return render_template('index.html', columns=columns)
    return 'Hello World!'

@app.route('/_server_data')
def get_server_data():

    collection = [dict(zip(columns, [1,2,3,4])), dict(zip(columns, [5,5,5,5]))]

    results = BaseDataTables(request, columns, collection).output_result()

    # return the results as a string for the datatable
    print (json.dumps(results).type)
    return json.dumps(results)


@app.route('/',  methods=['GET','POST'] )
def show_tables():
	table1 = pd.DataFrame()
	if request.method == 'POST':
		text = request.form['text']
		results1 = query_language_model(text)
		females = get_pmid_results(results1)
		results2 = query_language_model(text)
		males = get_pmid_results(results2)
		results3 = query_language_model(text)
		agender = get_pmid_results(results3)
		return render_template('view.html',tables=[females.to_html(classes='female'), males.to_html(classes='male'), agender.to_html(classes='agender')], titles = ['na', 'TF-IDF', 'Language Model', 'Vector Space Model'])



if __name__ == '__main__':
    app.run()
