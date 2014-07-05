__author__ = 'mohamed'

from django.shortcuts import render_to_response , redirect
from django.shortcuts import RequestContext
from django.http import *
from processing.Mongo import MongoManager
from processing.searcher import Searcher
import settings



def result(request):
    """
    This method will get the results according to the user inputted query string

    """
    keyword = request.GET.get('s','')
    page = request.GET.get('page','')
    articles = []
    model ={}
    #if the keyword is not empty so proceed forward
    if keyword:

        #initialize the mongoDB Manager
        dbManager = MongoManager()
        dbManager.connectNow()
        #initialize the search indexer
        indexer = Searcher(settings.SEARCHINDEX_CORPUS)
        if page =='':
            page = int(1)
        else:
            page = int(page)

        results = indexer.searchIndex(keyword,num=page)

        print("Keyword is %s and results count is %d " % (keyword,len(results)))

        if results:
            print ("results contain data")

            for result in results:
                #access mongoDB and retrieve the document
                id  = result['id']
                print (id)
                outcome = dbManager.db.articles.find({'id':id})

                for ar in outcome:
                    articles.append(ar)

            model = {'model':{'data':articles}}

    return render_to_response('index.html',RequestContext(request,model))





