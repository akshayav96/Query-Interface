import csv             #Base CSV reader library
import pdb             #debugger
import mysql.connector #sql connection lib
import time            #sleep command


def fill_db():
    num_records = 149994
    
    num = range(1,5)
    print ("%d",num)
    
################## PDB TRACING ################################
    pdb.set_trace()
    
###
### INITIALIZE  ABSTRACT ARRAYS
###
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
    

###
### INITIALIZE AUTHOR ARRAYS
###
    index_author = []
    PMID_author = []
    last_name_author = []
    fore_name_author = []
    initials_author = []
    
    
###
### INITIALIZE MESH ARRAYS
###
    index_mesh = []
    pmid_mesh = []
    major_topic_yn_mesh = []
    descriptor_name_mesh = []
    qualifier_name_mesh = []


###############################################################################
###################  ABSTRACT PROCESSING ######################################
    with open('C:\\M244B_SPRING_18\\DB_DATA\\abstract_table.csv', encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        #header = spamreader.next()
        for row in spamreader:
            if (counter == 0):
                header = row
                counter = counter + 1
                print('HEADER: ', header)
            elif counter >= num_records:
                break
                #return
            else:
                #myString = ','.join(row) #join(str(x) for x in row)
                myString = row

                #index_db.append(myString[0])
                PMID_db.append(myString[0])
                ISSN_db.append(myString[1])
                Volume_db.append(myString[2])
                Issue_db.append(myString[3])
                Year_db.append(myString[4])
                Month_db.append(myString[5])
                Title_db.append(myString[6])
                ArticleTitle_db.append(myString[7])
                AbstractText_db.append(myString[8])
                AffiliationInfo_db.append(myString[9])
                PublicationType_db.append(myString[10])
                
                
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
    print("ABSTRACT DONE")
    
###############################################################################
######################## AUTHOR PROCESSING  ###################################
    counter = 0
    
    with open('C:\\M244B_SPRING_18\\DB_DATA\\authors_table.csv', 
              encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        #header = spamreader.next()
        for row in spamreader:
            if (counter == 0):
                header = row
                counter = counter + 1
                print('HEADER: ', header)
#            elif counter >= num_records:
#                break
#                #return
            else:
#               FORMAT: ,PMID,LastName,ForeName,Initials
                myString = row

                index_author.append(myString[0])
                PMID_author.append(myString[1])
                last_name_author.append(myString[2])
                fore_name_author.append(myString[3])
                initials_author.append(myString[4])
                
                counter = counter + 1
    print('AUTHORS LIST PARSED')
    
    add_author = ("INSERT INTO author (pmid, "
               "last_name, fore_name, initials) "
               "VALUES (%s, %s, %s, %s);")

    for ii in range(0,len(PMID_author)):
        if (ii%500 == 0):
            print('Now at modulo', ii)
        #make sure data is in a list
            
        #find badly formed values
#        if (not(Volume_db[ii])):
#            #Find any empty volumes
#            Volume_db[ii] = '0'
#        if (not(Issue_db[ii])):
#            Issue_db[ii] = 0
        data_author = [PMID_author[ii], \
                    last_name_author[ii], \
                    fore_name_author[ii], \
                    initials_author[ii]]
        try:
            cursor.execute(add_author,data_author)
        except Exception as inst:
            print(type(inst))    # the exception instance
#            print('Error at line ',ii)


    emp_no = cursor.lastrowid




###############################################################################
######################## MESH PROCESSING  ###################################
    counter = 0
    
    with open('C:\\M244B_SPRING_18\\DB_DATA\\mesh_table.csv', 
              encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in spamreader:
            if (counter == 0):
                header = row
                counter = counter + 1
                print('HEADER: ', header)
#            elif (counter >= num_records):
#                break
            else:
#,PMID,MajorTopicYN,DescriptorName,QualifierName
                myString = row

                index_mesh.append(myString[0])
                pmid_mesh.append(myString[1])
                major_topic_yn_mesh.append(myString[2])
                descriptor_name_mesh.append(myString[3])
                qualifier_name_mesh.append(myString[4])
                
                counter = counter + 1
            add_mesh = ("INSERT INTO mesh (pmid, "
               "major_topic_yn, descriptor_name, qualifier_name) "
               "VALUES (%s, %s, %s, %s);")

    for ii in range(0,len(pmid_mesh)):
        if (ii%1000 == 0):
            print('Now at mesh modulo', ii)
        #make sure data is in a list
        data_mesh = [pmid_mesh[ii], \
                    major_topic_yn_mesh[ii], \
                    descriptor_name_mesh[ii], \
                    qualifier_name_mesh[ii]]
        try:
            cursor.execute(add_mesh,data_mesh)
        except Exception as inst:
            print(type(inst))    # the exception instance
#            print('Error at line ',ii)
    print('MESH LIST PARSED')



###############################################################################
    cnx.commit()
                
                
###############################################################################
    cnx.close()
    return