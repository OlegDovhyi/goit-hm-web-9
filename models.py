from mongoengine import Document
from mongoengine.fields import StringField, ReferenceField, ListField

class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()
    meta = {"collection": 'authors'}

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()
    meta = {"collection": 'quotes'}  # исправлено с 'qoutes' на 'quotes'
