
# coding: utf-8

# In[18]:


import pandas as pd
import mysql.connector
import calendar

def get_pmid_results(pmids):
    """
    Function that populates data frames with publication information. Input is a list of PubMed IDs; also requires the medline_db database to be run on the machine, and the appropriate user to be set up within SQL (see below).
    Outputs two pandas DataFrame objects: a shortened table with a subset of relevant fields, and a full table with the columns 'PMID', 'ISSN', 'Volume', 'Issue', 'Year', 'Month', 'Journal Title',
            'Article Title', 'Abstract', 'Affiliation', 'Publication Type', 'Authors', and 'MeSH Terms'.

    """
    cnx = mysql.connector.connect(user='bme223b', password='bme223b',                               host='localhost',                               database='medline_db')
    c = cnx.cursor(buffered = True)

    pd.set_option('display.max_colwidth', -1)

    table = pd.DataFrame()
    NoneType = type(None)

    cols = ['PMID', 'ISSN', 'Volume', 'Issue', 'Year', 'Month', 'Journal Title',
            'Article Title', 'Abstract', 'Affiliation', 'Publication Type', 'Authors', 'MeSH Terms']

    if type(pmids) is not NoneType:
        for pm in pmids:
            entry = []
            authors = []
            mesh = []
            #get the abstract entries
            c.execute('''SELECT * FROM abstract WHERE pmid=%s''', (pm,))
            abstract_list= c.fetchone()
            entry.extend(abstract_list[1:])
            #get author entries
            c.execute('''SELECT * FROM author WHERE pmid=%s''', (pm,))
            for i in c.fetchall():
                name = ', '.join((i[2],i[3]))
                authors.append(name)
            entry.append('; '.join(authors))
            #get mesh entries
            c.execute('''SELECT * FROM mesh WHERE pmid=%s''', (pm,))
            for m in c.fetchall():
                term = '/'.join((m[3],m[4]))
                mesh.append(term)
            entry.append('  |  '.join(mesh))
            #compile the table
            table = table.append(pd.Series(entry), ignore_index= True)

        #name and reorder the columns
        table.columns = cols
        table.PMID = table.PMID.astype(int)
        table.Year = table.Year.astype(int)
        table.Month = table.Month.astype(int)
        table['Publication Information'] = table['Journal Title'] + ', '+ table['Year'].map(str) + " " + table['Month'].apply(lambda x: calendar.month_abbr[x])+"; "+ table['Volume'].map(str) + "("+ table['Issue'].map(str)+ ")"
        short_table = table.applymap(str)[['PMID','Authors',  'Article Title', 'Publication Information']]
        full_table = table.drop('Publication Information', axis = 1)

    else:
        short_table = pd.DataFrame()
        full_table = pd.DataFrame()
    c.close()
    cnx.close()
    #return results_table, pmid_dict
    return short_table, full_table


# In[19]:


#testcode
#table = get_pmid_results(pmids)
