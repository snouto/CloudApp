__author__ = 'mohamed'

import lucene
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo

class ArticleDocument(Document):
    """
    This class represents PubMed Article in the search index

    """

    def __init__(self,id,title,abstract):

        #ID Field  Definition
        idfield = FieldType()
        idfield.setIndexed(True)
        idfield.setStored(True)
        idfield.setIndexed(False)

        # Other Fields Definition
        field = FieldType()
        field.setIndexed(True)
        field.setStored(True)
        field.setTokenized(True)

        #add the title field , abstract field and meshes fields to the document
        self.add(Field("id",id,idfield))
        self.add(Field("Title",title,field))
        self.add(Field("Abstract",abstract,field))


