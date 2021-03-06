__author__ = 'mohamed'

from Mongo import MongoManager
import math
from collections import Counter

from CosineSimilarity import CosineSimilarity
import pickle , sys


def getMeshes(article):
    """
    This function will access the meshes of the document and retrieve them as a list
    """
    mylist = []

    meshes = article['Meshes']

    for key,value in meshes.items():
        mylist.append(str(value['MeshTerm']))

    return mylist

def buildVector(masterWords, otherWords):
        masterCounter = Counter(masterWords)
        otherCounter = Counter(otherWords)
        all_items = set(masterCounter.keys()).union( set(otherCounter.keys()))
        vector1 = [masterCounter[k] for k in all_items]
        vector2 = [otherCounter[k] for k in all_items]
        return vector1, vector2

def cosine(masterVector, otherVector):
        dot_product = sum(n1 * n2 for n1,n2 in zip(masterVector, otherVector))
        magnitude1 = math.sqrt (sum(n ** 2 for n in masterVector))
        magnitude2 = math.sqrt (sum(n ** 2 for n in otherVector))
        return dot_product / (magnitude1 * magnitude2)



def pickleObject(vector,file):

    try:


        #now start pickling the vector onto disk
        pickle.dump(vector,file)

        return True

    except Exception ,args:
        print ("exception occurred with stack trace %s" % args)
        return False


def getArticle(file,start,end):
    """
    This function will retrieve the article with pmid from the database

    """
    mongo  = MongoManager()
    mongo.connectNow()
    #access the meshes of the first article retrieved
    #cosine = CosineSimilarity()
    bigVector = []
    finalVector = []
    articles = mongo.db.articles.find()
    index = int(start)
    subindex = 0
    allArticles = []



    #load all articles first
    for all in mongo.db.articles.find():
        allArticles.append(all)


    print("All Articles have been loaded successfully into Memory")

    #access articles in the database
    for article in allArticles[int(start):]:
        bigVector = []
        index += 1
        print("%s" % (index))
        for paper in allArticles:

            subindex += 1

            if article['id'] != paper['id']:

                #loop over the master Meshes first , because they are our template
                try:
                    masterAbstract= str(article['Abstract']).split()
                    otherWords = str(paper['Abstract']).split()
                    masterVector , otherVector = buildVector(masterAbstract,otherWords)
                    cosineValue = cosine(masterVector,otherVector)
                    bigVector.append((int(article['id']),int(paper['id']),float(cosineValue)))
                except Exception , args:
                    continue

        bigVector.sort(key=lambda keys:keys[2] , reverse=True)

        finalVector.append(bigVector[0:20])

        subindex = 0

    openedFile = open(file,"wb")
    result = pickleObject(finalVector,file=openedFile)
    openedFile.flush()

    openedFile.close()
    print ("Closing the pickling file")









if __name__ == '__main__':

    article = "10611347"

    if sys.argv <= 2:
        print ("Usage : Python distanceCalculator.py <File Name> <Start> <End>")
    else:

        file = sys.argv[1]
        start = sys.argv[2]
        end = sys.argv[3]
        getArticle(file=file,start=start,end=end)