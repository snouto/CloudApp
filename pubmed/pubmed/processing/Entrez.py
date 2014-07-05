__author__ = 'mohamed'



"""

This file is for accessing Entrez Online Data Repository using BioPython

"""

from Bio import Entrez # install with 'pip install biopython'
from Bio.Entrez import efetch, read
Entrez.email = "csharpizer@gmail.com" # register your email

class EntrezManager(object):


    def safeDateCompleted(self,dictionary,parentKey , key):

        date = dict(dictionary).get(parentKey,None)
        if date != None and key in dict(date).keys():
            return date[key]
        else:
            return ''

    def safeAbstract(self,dictionary,key):

        article = dict(dictionary).get('Article',None)
        if article != None:
            abstract = dict(article).get('Abstract',None)
            if abstract != None:
                text = dict(abstract).get('AbstractText',None)

                if text != None:
                    return text
                else:
                    return ''
        else:
            return ''

    def getDocument(self,pmid):
        #this method will return all associated attributes for an article
        #including Article Title , Publication Date , Authors' Names , Citations......etc.
        # it will return it as a python dictionary suitable for storage in mongodb
        handle = efetch(db='pubmed', id=str(pmid), retmode='xml')
        xml_data = read(handle)[0]

        article = dict(id = pmid,Title = str(xml_data['MedlineCitation']['Article'][u'ArticleTitle'])
                       , Abstract=str(self.safeAbstract(xml_data['MedlineCitation'],u'Abstract')),
                       DateCompleted="{}/{}/{}".format(self.safeDateCompleted(xml_data['MedlineCitation'],'DateCompleted','Day'),
                                                       self.safeDateCompleted(xml_data['MedlineCitation'],'DateCompleted','Month'),
                                                       self.safeDateCompleted(xml_data['MedlineCitation'],'DateCompleted','Year'),),
                       DateRevised="{}/{}/{}".format(self.safeDateCompleted(xml_data['MedlineCitation'],'DateRevised','Day'),
                                                     self.safeDateCompleted(xml_data['MedlineCitation'],'DateRevised','Month'),
                                                     self.safeDateCompleted(xml_data['MedlineCitation'],'DateRevised','Year')))


        return (xml_data,article)

    def getMeshes(self,article):
        mylist = []
            # call PubMed API
       # handle = efetch(db='pubmed', id=str(pmid), retmode='xml')
        xml_data = article

        #print(xml_data['MedlineCitation']['PMID'])

        # skip articles without MeSH terms
        if u'MeshHeadingList' in xml_data['MedlineCitation']:
            for mesh in xml_data['MedlineCitation'][u'MeshHeadingList']:
                # grab the qualifier major/minor flag, if any
                major = 'N'
                qualifiers = mesh[u'QualifierName']
                if len(qualifiers) > 0:
                    major = str(qualifiers[0].attributes.items()[0][1])
                    if major == 'Y':
                        major = 1
                    else:
                        major = 0

                # grab descriptor name
                descr = mesh[u'DescriptorName']
                name = descr.title()
                mylist.append((name,major))

        return mylist
