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

5. Create the following user: be223b, identified by 223b, by running these commands in your terminal. 

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


