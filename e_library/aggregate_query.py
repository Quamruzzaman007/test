from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['e_library'] 

def arregate_query():
    return [    
        {
            "$lookup": {
                "from": "languages",
                "localField": 'language_id',
                "foreignField": "_id",
                "as": "languages"}
            },
            {
                "$unwind":"$languages"
            },
            {
            "$lookup": {
                "from": "books",
                "localField": 'languages.book_id',
                "foreignField": "_id",
                "as": "books",
                }
            },
            {
                "$unwind":"$books"
            },
            {
            "$lookup": {
                "from": "book_publishers",
                "localField": 'books._id',
                "foreignField": "book_id",
                "as": "book_publishers",
                }
            },
            {
                "$unwind":"$book_publishers"
            },
            {
            "$lookup": {
                "from": "publishers",
                "localField": 'book_publishers.publisher_id',
                "foreignField": "_id",
                "as": "publishers",
                }
            },
            {
                "$unwind":"$publishers"
            }
          
        ]

def arregate_query_with_search(keyword):
    return [   
        {"$match":{"$text": {"$search":keyword}}}, 
        {
            "$lookup": {
                "from": "languages",
                "localField": 'language_id',
                "foreignField": "_id",
                "as": "languages"}
            },
            {
                "$unwind":"$languages"
            },
            {
            "$lookup": {
                "from": "books",
                "localField": 'languages.book_id',
                "foreignField": "_id",
                "as": "books",
                }
            },
            {
                "$unwind":"$books"
            },
            {
            "$lookup": {
                "from": "book_publishers",
                "localField": 'books._id',
                "foreignField": "book_id",
                "as": "book_publishers",
                }
            },
            {
                "$unwind":"$book_publishers"
            },
            {
            "$lookup": {
                "from": "publishers",
                "localField": 'book_publishers.publisher_id',
                "foreignField": "_id",
                "as": "publishers",
                }
            },
            {
                "$unwind":"$publishers"
            }
          
        ]