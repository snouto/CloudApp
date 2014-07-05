__author__ = 'mohamed'

import sys

from Entrez import EntrezManager

from Mongo import MongoManager





index = 0

articleManager = EntrezManager()
dbManager = MongoManager()


if len(sys.argv) >= 3:

    args = sys.argv

    """
    We will begin reading the file from here
    """
    index = int(args[2])

    print ("trying to connect to MongoDB")

    result = dbManager.connect("localhost",27017,"pmc")

    if result == False:
        print("Unable to connect to Mongo DB")
    else:

        print ("Begin reading the index file ")

        indexFile = open("index",mode="w")

        print ("Begin reading the PMC IDs file")

        file = open(args[1], mode="r")

        lines = file.readlines()
        print ("Done. Reading the PMC IDs file")

        for line in lines[index:]:

            try:

                print("Reading article No. %d" % index)

                index += 1
                indexFile.write(str(index))
                #starting from the initial index Now begin parsing the file to get each Article id
                articleID = line.split(",")[9] #getting the article id which it will be at 9
                print ("article ID %s " % articleID)

                if len(articleID) > 0:
                    #it means that the record is actually associated with an article id so begin
                    #retrieving the entire article from NCBI PubMed online database and insert it into mongo DB
                    xmlData , article = articleManager.getDocument(articleID)

                    if article != None and xmlData != None:
                        #Get the article meshes first
                        meshes = articleManager.getMeshes(xmlData)

                        if meshes != None:

                            article["Meshes"] = {}

                            #insert the meshes in the body of the article document itself
                            meshIndex = 0

                            for item in meshes:
                                article["Meshes"][str(meshIndex)] = dict(MeshTerm = item[0] , Major = item[1])
                                meshIndex += 1
                        else:
                            print ("There are no Meshes for the following article %d" % articleID)


                        #Now save the article in Mongo DB
                        dbManager.insertArticle(article)

                else:
                    continue
            except Exception:
                continue



            #close the index file
    indexFile.close()
            #close the PMC IDs file as well
    file.close()




else:
    print ("Usage :  python cloud.py [FileName] [Index]")
