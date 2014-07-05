__author__ = 'mohamed'

from Mongo import MongoManager
from articleDocument import ArticleDocument

import sys, os, lucene, threading, time
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version


class CloudIndexer(object):
    """
    This class is an indexer that will build a search index against the articles in the database
    and stores the index files into an index directory
    """
    indexDir = None
    dbManager = MongoManager()
    store = None
    analyzer = None
    writer = None
    config = None



    def __init__(self,indir):

        """
        Inits the current Indexer with the index directory where we have to store the search index folder

        """
        try:
            self.indexDir = indir
            store = SimpleFSDirectory(File(indir))
            analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(Version.LUCENE_CURRENT), 1048576)
            config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
            config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
            writer = IndexWriter(store, config)

        except Exception,args:

            print("There was an error during initializing the Cloud Indexer , \n %s" % args)


    def beginIndexing(self):
        """
        This method will begin the indexing process against the articles inside the database
        """
         #access the database first
        dbconnect = self.dbManager.connectNow()

        if dbconnect:
            print ("Connected Successfully to NOSQL Database : MongoDB")
        else:
            print ("There was a problem connecting with the database , please try again")

         #Now , loop over the articles inside the database one by one and index each returned article

        articles = self.dbManager.getAllArticles()

        if len(articles) > 0 :

            print ("**********************************************Begin of Indexing**********************************************")

            for article in articles:
                self.indexArticle(article)


            #closing everything
            self.writer.commit()
            self.writer.close()
            print ("**********************************************Done Indexing Files**********************************************")

        else:
            print ("No articles found in the Database , Please check your database or database collection !")




    def indexArticle(self,article):

        """
        This method will add the current article if valid into the search index

        """

        try:

             print ("Indexing Article with id  : %d " % article['id'])

             if not (len(article.get('Title','')) <= 0 or len(article.get('Abstract','')) <= 0):

                #index the current document
                doc = ArticleDocument(article.get('id'),article.get('Title',''),article.get('Abstract',''))
                #add the current document into the writer
                self.writer.addDocument(doc)
             else:

                 print ("Excluding Document : %d , Without Either Title or Abstract" % article['id'])

                 pass

        except Exception , e:

            print ("%s" % e)



        



