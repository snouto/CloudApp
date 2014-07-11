__author__ = 'mohamed'

from django.shortcuts import render_to_response , redirect
from django.shortcuts import RequestContext
from django.http import *
from processing.Mongo import MongoManager
from processing.searcher import Searcher
import settings

from processing.distanceCalculator import *
import json
def recommendation(articleID):
    """
     this method will return the highest recommended articles for the current article id and return the result via json
    """
    bigVector = []
    results = {}
    if articleID:
        dbmanager = MongoManager()
        dbmanager.connectNow()
        searchedArticle = dbmanager.db.articles.find({'id':articleID})[0]
        articles = dbmanager.db.articles.find()

        for paper in articles:

            if searchedArticle['id'] != paper['id']:
                    try:
                        masterAbstract= str(searchedArticle['Abstract']).split()
                        otherWords = str(paper['Abstract']).split()
                        masterVector , otherVector = buildVector(masterAbstract,otherWords)
                        cosineValue = cosine(masterVector,otherVector)
                        bigVector.append((int(searchedArticle['id']),int(paper['id']),float(cosineValue)))

                    except Exception , args:
                        pass


        bigVector.sort(key=lambda keys:keys[2] , reverse=True)

        highestScoredArticles = bigVector[0:5]


        for currentPaper in highestScoredArticles:

            recommended = dbmanager.db.articles.find({'id':str(currentPaper[1])})[0]

            if recommended:

                results[recommended['id']] = {'title':str(recommended['Title']),'abstract':str(recommended['Abstract']),'rdate':str(recommended['DateRevised']),'id':str(recommended['id'])}


    return results




def viewArticle(request):

    """
    This method will access the article id from the request and retrieve its results in a page
    """

    articleID = request.GET.get('articleID','')
    model = {}
    dbmanager = MongoManager()

    try:
            if articleID:
                dbmanager.connectNow()
                cursor = dbmanager.db.articles.find({'id':articleID})
                articles = []
                for paper in cursor:
                    articles.append(paper)

                recommendations = recommendation(articleID)

                print (recommendations)

                model = {'model':{'article':articles[0],'recommendations':recommendations}}

                return render_to_response('viewArticle.html',model,context_instance=RequestContext(request))

            else:
                 return render_to_response('index.html',Context_instance=RequestContext(request))

    except Exception , args:

        return render_to_response('index.html',context_instance=RequestContext(request))




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





