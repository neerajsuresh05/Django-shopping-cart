from django.db import models
class products(models.Model):
    name=models.CharField(max_length=50)
    price=models.FloatField()
    stock=models.IntegerField()
    img=models.ImageField()
    def __str__(self):
        return self.name
    
class usertable(models.Model):
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    place=models.CharField(max_length=50)
    mobile=models.IntegerField()
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)

class cart(models.Model):
    usern=models.CharField(max_length=50)
    price=models.FloatField()
    itemn=models.CharField(max_length=50)
    item_id=models.IntegerField()
    qty=models.IntegerField()
    userid=models.IntegerField()
    img=models.ImageField()