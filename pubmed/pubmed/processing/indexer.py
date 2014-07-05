__author__ ="Mohamed"


import whoosh ,sys
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StandardAnalyzer
from articleSchema import ArticleDocument
from whoosh.index import create_in
from Mongo import MongoManager
from whoosh import index
from whoosh.qparser import QueryParser

class CloudIndexer(object):

    """
    This class represents the cloud indexer which will index documents in the distributed NOSQL Database and stores the search index files
    into a directory
    """
    indexDir = None
    writer  = None
    dbManager = None

    def __init__(self,dir):
        self.indexDir = dir

        ix = index.create_in(dir,ArticleDocument)
        self.writer = ix.writer()
        self.dbManager = MongoManager()



    def loadIndexDirectory(self,dir):
        self.indexDir = dir


    def searchIndex(self,keyword):
        results = []

        ix = index.open_dir(self.indexDir)
        queryParser = QueryParser("abstract",ix.schema)
        query = queryParser.parse(keyword)

        with ix.searcher() as s:
            outcome = s.search(query)

            for result in outcome:
                results.append(result)


        return results




    def beginIndexing(self):

        print ("************************Begin Indexing************************")
        counter = 0

        result = self.dbManager.connectNow()

        if result :
            print ("Connected Successfully to NOSQL Database")

        else:
            print ("There was a problem accessing the NOSQL Database")

        articles = self.dbManager.getAllArticles()

        for article in articles:
            self.indexArticle(article)
            counter += 1
            print ("No. Documents Indexed : %d" % int(counter))


        self.writer.commit()
        print("************************Finished Indexing************************")


    def indexArticle(self,article):

        print ("Indexing Document : %s" % article.get('id',''))
        self.writer.add_document(id=article.get('id'),title=article.get('Title'),abstract=article.get('Abstract'))



if __name__ =='__main__':

    if len(sys.argv) <= 1:
        print ("Usage : python indexer.py <Search Index Directory>")
        sys.exit(1)

    cloudindexer = CloudIndexer(sys.argv[1])

    cloudindexer.beginIndexing()





