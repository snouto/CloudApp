__author__ = 'mohamed'

"""

This file contains the MongoManager Class
Which will connect to mongo database and performs CRUD Operations against the Database associated with
storing the PMC Articles

"""

from pymongo import MongoClient


class MongoManager(object):

    #Mongo Client
    client = None
    db = None

    def connect(self,ip,port,dbName):
        self.client = MongoClient(host=ip,port=port)
        self.db = self.client[dbName]
        return True

    def connectNow(self):
        return self.connect("localhost",27017,"pmc")


    def insertArticle(self,article):
        articleID = self.db.articles.insert(article)
        print("Inserted Article %s in MongoDb with ObjectID : %s" % (article['id'],articleID))
        return True

    def getArticle(self,pmid):
        pass

    def getAllArticles(self):
        """
        Returns the complete articles in the database
        """
        return self.db.articles.find()


    def deleteArticle(self,pmid):
        pass

    def updateArticle(self,article):
        pass

    def getArticle(self,pmid):
        pass

    def insertMeshesForArticle(self,pmid,Meshes):
        pass


