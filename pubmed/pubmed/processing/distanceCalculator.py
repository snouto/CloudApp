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



def pickleObject(vector,fileName):

    try:
        fileObject = open(fileName,"wb")

        #now start pickling the vector onto disk
        pickle.dump(vector,fileObject)

        #close the file
        fileObject.close()

        return True

    except Exception ,args:
        print ("exception occurred with stack trace %s" % args)
        return False


def getArticle(file):
    """
    This function will retrieve the article with pmid from the database

    """
    mongo  = MongoManager()
    mongo.connectNow()
    #access the meshes of the first article retrieved
    #cosine = CosineSimilarity()
    bigVector = []
    articles = mongo.db.articles.find()
    index = 0
    subindex = 0
    #access articles in the database
    for article in articles:
        index += 1

        for paper in mongo.db.articles.find():

            subindex += 1

            if article['id'] != paper['id']:
                print("Processing %s - %s" % (index,subindex))
                #loop over the master Meshes first , because they are our template
                masterAbstract= str(article['Abstract']).split()
                otherWords = str(paper['Abstract']).split()
                masterVector , otherVector = buildVector(masterAbstract,otherWords)
                cosineValue = cosine(masterVector,otherVector)
                bigVector.append((int(article['id']),int(paper['id']),float(cosineValue)))

        bigVector.sort(key=lambda keys:keys[2] , reverse=True)

        result = pickleObject(bigVector[0:20],fileName=file)

        if result:
            print ("Pickling Done and everything controlled , Happy recommendation using Cosine Similarity ")
        else:
            print ("There was a problem in pickling the object")

        subindex = 0





if __name__ == '__main__':

    article = "10611347"

    if sys.argv <= 1:
        print ("Usage : Python distanceCalculator.py <File Name>")
    else:

        file = sys.argv[1]
        getArticle(file=file)