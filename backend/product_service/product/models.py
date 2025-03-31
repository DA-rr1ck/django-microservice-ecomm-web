from mongoengine import Document, StringField, IntField, FloatField

class Product(Document):
    name = StringField(required=True, max_length=255)
    description = StringField()
    price = FloatField(required=True)
    stock = IntField(default=0)
    view_count = IntField(default=0)
    cart_count = IntField(default=0)
    order_count = IntField(default=0)
    avg_rating = FloatField(default=0.0)

    meta = {"collection": "products"}  # Collection name in MongoDB
