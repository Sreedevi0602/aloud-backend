from django.db import models


# Create your models here.

class Books(models.Model):
    bookid = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    photo = models.FileField(upload_to='media')
    categories = models.ManyToManyField('Category', related_name='books', blank=True)

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name
