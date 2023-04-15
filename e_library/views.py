from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime, timedelta
from pymongo import MongoClient
import json
from .aggregate_query import arregate_query
from .aggregate_query import arregate_query_with_search


# Connecting to the database
client = MongoClient('localhost', 27017)
db = client['e_library'] 

#get reviews by publisher and language
def publisher_language_query(publisher, language ):
    aggregate_query = arregate_query()
    if publisher and language:
        aggregate_query.append({"$match":{"publishers.name": publisher}})
        aggregate_query.append({"$match":{"languages.name": language}})
        aggregate_query.append({ "$project": { "text": 1} })
    return aggregate_query


# publisher and date query
def publisher_days_query(publisher, days, start_date):
    aggregate_query = arregate_query()
    if publisher:
         aggregate_query.append({"$match": {"publishers.name": publisher}})
    if days:
        aggregate_query.append({"$match": {'time': {"$lt": start_date.strftime("%Y-%m-%d %H:%M:%S")}}})
        aggregate_query.append({'$group': {'_id': None, 'total_rating': {'$sum': '$rating'}, 'count': {'$sum': 1 }}})
        aggregate_query.append({'$project': {'_id': 0, 'average_rating': {'$divide': ['$total_rating', '$count']}}})
    return aggregate_query


#get publisher by rating and keywords
def get_publisher_by_keywords_rating_query(keyword, rating, start_date):
    aggregate_query = arregate_query()
    if keyword and rating and start_date:
        aggregate_query.append({ "$match":{"text": { "$regex": keyword}}})
        aggregate_query.append({ "$match":{"rating": { "$gte": int(rating)}}})
        aggregate_query.append({ "$match":{"time": {"$lt": start_date.strftime("%Y-%m-%d %H:%M:%S")}}})
        aggregate_query.append({ "$project": { "publishers.name": 1} })
    return aggregate_query

#get reviews by publisher and language
def get_reviews_by_publisher_language(request):
    publisher = request.GET.get('publisher')    
    language = request.GET.get('language')
    if publisher and language:
        reviews_data = db.reviews.aggregate(publisher_language_query(publisher, language))
        return HttpResponse(list(reviews_data))
    else:
        return JsonResponse({"Error": "Publisher Name or Book Language is missing.", "status_code": 400})


#get avg rating by publisher and rating days
def get_average_rating(request):
    publisher = request.GET.get('publisher')
    days = request.GET.get('days')
    if publisher and days:
        start_date = datetime.now() - timedelta(days=int(days))
        data = db.reviews.aggregate(publisher_days_query(publisher, days, start_date))
        return HttpResponse(list(data)) 
    else:
        return JsonResponse({"Error": "Publisher Name or days are missing.", "status_code": 400})

#get publisher by rating and keywords
def get_publisher_by_keywords_rating(request):
    keyword = request.GET.get('keyword')
    rating = request.GET.get('rating')
    days = request.GET.get('days')
    start_date = datetime.now() - timedelta(days=int(days))

    if rating and keyword and start_date:
        data = db.reviews.aggregate(get_publisher_by_keywords_rating_query(keyword, rating, start_date))
        return HttpResponse(list(data))
    else:
        return JsonResponse({"Error": "Publisher Name or keyword is missing.", "status_code": 400})