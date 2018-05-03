import csv             #Base CSV reader library
import pdb             #debugger
import mysql.connector #sql connection lib
import time            #sleep command


def fill_db():
    num_records = 150000
    
    num = range(1,5)
    print ("%d",num)
    pdb.set_trace()
###
### INITIALIZE ARRAYS
    counter = 0
    index_db = []
    PMID_db = []
    ISSN_db = []
    Volume_db = []
    Issue_db = []
    Year_db = []
    Month_db = []
    Title_db = []
    ArticleTitle_db = []
    AbstractText_db = []
    AffiliationInfo_db = []
    PublicationType_db = []    
    

    with open('C:\M244B_SPRING_18\DB_DATA\MEDLINE_Parsed.csv', encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        #header = spamreader.next()
        for row in spamreader:
            if (counter == 0):
                header = row
                counter = counter + 1
                print('HEADER: ', header)
            elif counter == num_records:
                break
                #return
            else:
                #myString = ','.join(row) #join(str(x) for x in row)
                myString = row

                index_db.append(myString[0])
                PMID_db.append(myString[1])
                ISSN_db.append(myString[2])
                Volume_db.append(myString[3])
                Issue_db.append(myString[4])
                Year_db.append(myString[5])
                Month_db.append(myString[6])
                Title_db.append(myString[7])
                ArticleTitle_db.append(myString[8])
                AbstractText_db.append(myString[9])
                AffiliationInfo_db.append(myString[10])
                PublicationType_db.append(myString[11])
                
                
#                print(ArticleTitle_db[0])
                if(counter == 122434):
                    print('Read 122434')
                counter = counter + 1;                
                #row.split(',') 

###
###                 DATABASE CONNECTION
    cnx = mysql.connector.connect(user='bme223b', password='bme223b', \
                              host='127.0.0.1', \
                              database='medline_db')
    cursor = cnx.cursor()
    #######################################################
    ###     DATABASE CLEAR
    #cursor.execute("TRUNCATE `medline_db`.`abstract`;")
    #######################################################
    add_abstract = ("INSERT INTO Abstract (pmid, "
               "issn, volume, issue, year, month, "
               "journal_title, article_title, abstract, "
               "affiliation, publication_type) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

    for ii in range(0,len(PMID_db)):
        if (ii%500 == 0):
            print('Now at modulo', ii)
        #make sure data is in a list
            
        #find badly formed values
        if (not(Volume_db[ii])):
            #Find any empty volumes
            Volume_db[ii] = '0'
        if (not(Issue_db[ii])):
            Issue_db[ii] = 0
        data_abstract = [PMID_db[ii], \
                    ISSN_db[ii], Volume_db[ii], Issue_db[ii],\
                    Year_db[ii], Month_db[ii], Title_db[ii], ArticleTitle_db[ii], \
                    AbstractText_db[ii], AffiliationInfo_db[ii], PublicationType_db[ii]]
        try:
            cursor.execute(add_abstract,data_abstract)
        except Exception as inst:
            print(type(inst))    # the exception instance
#            print('Error at line ',ii)


    emp_no = cursor.lastrowid

    cnx.commit()
    print("DB DONE")
    cnx.close()
    return