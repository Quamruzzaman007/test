from pymongo import MongoClient
from faker import Faker
import pytz
import random

client = MongoClient("mongodb://localhost:27017/")
db = client["e_library"]


publishers = db["publishers"]
books = db["books"]
book_publishers = db["book_publishers"]
languages = db["languages"]
reviews = db["reviews"]

tz = pytz.timezone('Asia/Kolkata')
fake = Faker()
# Generate publishers
for i in range(10):
    publisher = {
        "name": fake.company(),
    }
    publishers.insert_one(publisher)
    
# Generate books
for i in range(100):
    book = {
        "title": fake.catch_phrase()
    }
    books.insert_one(book)
    
# Generate book_publishers    
publisher_ids = [publisher["_id"] for publisher in publishers.find()]
book_ids = [book["_id"] for book in books.find()]
for p_id in publisher_ids:
    for b_id in book_ids:
        b_p = {'publisher_id':p_id,'book_id':b_id}
        book_publishers.insert_one(b_p)

# Generate languages
languages_list = ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Chinese", "Japanese"]
for bk_id in book_ids:
    for l in languages_list:
        language = {
            "name": l,
            "book_id":bk_id
            }
        languages.insert_one(language)

language_ids = [language["_id"] for language in languages.find()]
for i in range(1500):
    rn = random.randint(20, 30)
    date = fake.date_time_between(start_date='-30y', end_date='now')
    dt_with_tz = tz.localize(date)
    
    review = {
        "language_id": random.choice(language_ids),
        "Does_it_contain":random.choice(['Yes','No']),
        "rating": random.randint(1, 5),
        "text": fake.sentence(nb_words=rn),
        "time": dt_with_tz.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    reviews.insert_one(review)
print("Data generation complete!")



