__author__ = 'mohamed'

import whoosh
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED,SchemaClass
from whoosh.analysis import StandardAnalyzer , StemmingAnalyzer



class ArticleDocument(SchemaClass):

    id = ID(stored=True)
    title = TEXT(stored=False,analyzer=StandardAnalyzer(),field_boost=2.0)
    abstract = TEXT(stored=False,analyzer=StandardAnalyzer())
