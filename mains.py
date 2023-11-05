from mongoengine import connect
import json
from models import Author, Quote

connect(db='home2', host="mongodb+srv://olegdovgyy:Ingress0@furiya.pgnjs1b.mongodb.net/?retryWrites=true&w=majority")


def find_all_quotes_author(author):
    print(f"Searching for quotes by author: {author}")
    result = []
    author = Author.objects(fullname=author).first()

    if author:
        quotes = Quote.objects(author=author.id).all()
        for quote in quotes:
            result.append(quote.quote)

        return result

    

def find_all_quotes_for_tag(tag):
    result = []
    quotes = Quote.objects(tags=tag)

    for quote in quotes:
        result.append(quote.quote)

    return result


def find_all_quotes_for_tags(tags):
    tags = tags.split(',')
    list_tags =[]
    result = []
    for tag in tags:
        list_tags.append(tag)
    print(list_tags)

    quotes = Quote.objects(tags__in=list_tags)
    for quote in quotes:
        result.append(quote.quote)

    return result


def main():
    while True:
        action = input('Enter command: ')

        if action.startswith('exit'):
            break
        elif action.startswith('name:'):
            parse = action.split(':')
            print(find_all_quotes_author(parse[1].strip()))
        elif action.startswith('tag:'):
            parse = action.split(':')
            print(find_all_quotes_for_tag(parse[1].strip()))
        elif action.startswith('tags:'):
            parse = action.split(':')
            print(find_all_quotes_for_tags(parse[1].strip()))
        else:
            print("Wrong command")

with open("quotes.json", "r", encoding="utf-8") as fh:
    quotes_json_list = json.loads(fh.read())

for quote_data in quotes_json_list:
    author_name = quote_data["author"]
    author = Author.objects(fullname=author_name).first()

    quote = Quote(
        tags=quote_data["tags"], 
        author=author,  
        quote=quote_data["quote"]
    )
    quote.save()



if __name__ == "__main__":
    main()