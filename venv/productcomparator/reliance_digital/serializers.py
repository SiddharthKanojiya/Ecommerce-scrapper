from rest_framework import serializers

class ProductSerializers(serializers.Serializer):
    sinput=serializers.CharField(max_length=200)
    productInfo=serializers.CharField(max_length=500)
    price=serializers.CharField(max_length=20)
    link=serializers.URLField()
    img=serializers.URLField()
    rating=serializers.CharField(max_length=10)

class productclass:
    def __init__(self, sinput, productInfo, price,link,img,rating):
        self.sinput = sinput
        self.productInfo = productInfo
        self.price = price
        self.link=link
        self.img=img
        self.rating=rating