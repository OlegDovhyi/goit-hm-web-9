import json

from mongoengine import connect

from models import Author, Quote


connect(db='home2', host="mongodb+srv://olegdovgyy:Ingress0@furiya.pgnjs1b.mongodb.net/?retryWrites=true&w=majority")

with open("authors.json", "r", encoding="utf-8") as fh:
    json_list = json.loads(fh.read())

for i, json_dict in enumerate(json_list):
    author = Author(
        fullname=json_dict["fullname"], 
        born_date=json_dict["born_date"], 
        born_location=json_dict["born_location"], 
        description=json_dict["description"]
        )
    author.save()
    exec(f"author{i} = author")


with open("quotes.json", "r", encoding="utf-8") as fh:
    json_list = json.loads(fh.read())

for i, json_dict in enumerate(json_list):
    if i < 3:
        quote = Quote(
            tags=json_dict["tags"], 
            author=author, 
            quote=json_dict["quote"]
            )
        quote.save()
        exec(f"quote{i} = quote")
    else:
        quote = Quote(
            tags=json_dict["tags"], 
            author=author, 
            quote=json_dict["quote"]
            )
        quote.save()
        exec(f"quote{i} = quote")