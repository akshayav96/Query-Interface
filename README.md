# BE224B

A small app for querying PubMed entries using a tf-idf, vector space, and language model.

### To install and run the app:
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

6. Change directory to the app portion of the repository, and install any required packages:

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
A high-level overview of our application is illustrated in the diagram below:


![ScreenShot](https://raw.github.com/jspolson/BE224B/master/224B_Overview.png)

Continue reading for more detailed descriptions of each model's algorithm.

### Language Model 
The Language Model algorithm generates a simple probability distribution for each document by counting the frequency of words in the document and dividing this by the total length of the document. First, each document is pre-processed in a consistent format: punctuation and numbers are removed, and the tokenized words are stemmed using the SnowballStemmer library. This model utilizes the TfidfVectorizer module from scikit-learn to generate an L1-normalized distribution function for each document, in the form of a sparse matrix. This model can be called upon to perform a language model-based query. Of note, the text use to generate this was both the abstract text as well as the article title, given that an abstract was not provided for every article within the XML files. This model weighs words in the title slightly, such that their probability will be higher when considering the document distribution. The overall model is saved in a pickle file; pushing the model to a database and querying it was less efficient. 

When a query is submitted through the flask website, the query is subjected to the same preprocessing methods and then constrained to a vector having the same shape as any entry within the data model. To save time, the model only selects the entries where at least one of the query words appears in the probability distribution. Then, query and document models are compared using the Kullback–Leibler divergence measure. This is calculated using the entropy function within the scipy library. This measure was selected on the basis that it generally gives better information retrieval results than query-likelihood or document-likelihood methods. The PMIDS with the lowest entropy scores are returned (in this case, 20 IDs are returned).
