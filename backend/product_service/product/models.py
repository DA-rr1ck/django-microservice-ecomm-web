from mongoengine import Document, StringField, IntField, FloatField

class Product(Document):
    name = StringField(required=True, max_length=255)
    description = StringField()
    price = FloatField(required=True)
    stock = IntField(default=0)

    meta = {"collection": "products"}  # Collection name in MongoDB
