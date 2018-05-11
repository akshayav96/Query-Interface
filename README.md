# BE224B

A small app for querying PubMed entries using a tf-idf, vector space, and language model.

## Installation Instructions
1. Clone the repository:

```
$ git clone https://github.com/jspolson/BE224B.git
```

2. Unzip the file titled "medline_db.zip" to acquire the .sql file

3. Connect to SQL via your connection client (e.g., MySQL Workbench)

4. Import the .sql file to add the database; you should now have medline_db among your list of tables.

5. Create the following user in mysql by running these commands in your terminal or using your client. 

```
$ create user 'bme223b'@'localhost' identified by 'bme223b';
$ grant all privileges on medline_db.* to 'bme223b'@'localhost' identified by 'bme223b';
```

6. Change directory to the app portion of the repository, and install any required packages.

```
$ cd BE224B/app
$ pip install -r requirements.txt
```

7. Run the following command: 

```
python app1.py
```

8. The app should render at http://127.0.0.1:5000/


## How it Works:
A high-level overview of our application is illustrated in the diagram below. Functions are in black rounded boxes, and white boxes indicate I/O of functions.


![ScreenShot](https://raw.github.com/jspolson/BE224B/master/224B_Overview.png)

Continue reading for more detailed descriptions of each model's algorithm.
## Models and Algorithms
### Language Model 
The Language Model algorithm generates a simple probability distribution for each document by counting the frequency of words in the document and dividing this by the total length of the document. First, each document is pre-processed in a consistent format: punctuation and numbers are removed, and the tokenized words are stemmed using the SnowballStemmer library. This model utilizes the TfidfVectorizer module from scikit-learn to generate an L1-normalized distribution function for each document, in the form of a sparse matrix. This model can be called upon to perform a language model-based query. Of note, the text use to generate this was both the abstract text as well as the article title, given that an abstract was not provided for every article within the XML files. This model weighs words in the title slightly, such that their probability will be higher when considering the document distribution. The overall model is saved in a pickle file; pushing the model to a database and querying it was less efficient. 

When a query is submitted through the flask website, the query is subjected to the same preprocessing methods and then constrained to a vector having the same shape as any entry within the data model. To save time, the model only selects the entries where at least one of the query words appears in the probability distribution. Then, query and document models are compared using the Kullback–Leibler divergence measure. This is calculated using the entropy function within the scipy library. This measure was selected on the basis that it generally gives better information retrieval results than query-likelihood or document-likelihood methods. The PMIDS with the lowest entropy scores are returned (in this case, 20 IDs are returned). One feature that could limit this model, and could be improved upon in the future, is the smoothing. On a machine with 8 GB of RAM, it was difficult to perform computations on the probability distribution matrix. However, probability distribution has been calculated for the entire corpus, enabling computation if a more efficient method or machine is found.

## Contributions

**Jennifer Polson (JP)**
- parsed XML files (see lib-processing/XMLParsing_withLanguage.ipynb)
- created language model (see app/language_model and lib-processing/Language Model_Creation.ipynb)
- created function get_pmid_results.py to query database and return results
- implemented the DataTables rendering within the results view

## Some Notes

The lib-processing directory contains pieces of code used to generate other components of this project not directly involved in the app. The contents are as follows: 
- XMLParsing_withLanguage.ipynb (JP): a python notebook, through with the XML files were parsed, generating portable .csv files for the group to use for the rest of the project. 
- fill_db.py (KG): a python script responsible for populating the SQL database from the .csv files generated in the previous file.
- Language Model_Creation.ipynb (JP) : a python notebook responsible for generating and storing the language model 
