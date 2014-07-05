__author__ = 'mohamed'

import whoosh ,sys
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StandardAnalyzer
from articleSchema import ArticleDocument
from whoosh.index import create_in
from Mongo import MongoManager
from whoosh import index
from whoosh.qparser import QueryParser

class Searcher(object):

    indexDir = None

    def __init__(self,dir):
        self.indexDir = dir



    def searchIndex(self,keyword):
        results = []

        ix = index.open_dir(self.indexDir)
        queryParser = QueryParser("abstract",ix.schema)
        query = queryParser.parse(keyword)

        with ix.searcher() as s:
            outcome = s.search(query)

            for result in outcome:
                results.append({'id':result.get('id')})


        return results