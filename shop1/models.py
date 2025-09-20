from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
import os
import uuid

#for unique name generate
def unique_category_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{slugify(instance.name)}-{uuid.uuid4().hex}.{ext}"
    return os.path.join('category_images/', filename)

# Create your models here.
class main_category(models.Model):
      main_category_name = models.CharField(max_length=100, unique=True)




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    image = models.ImageField(upload_to=unique_category_image_path, blank=True, null=True)
    main_category = models.ForeignKey(main_category, on_delete=models.CASCADE,related_name='maincategory')
   

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Generates slug from name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
#product model
#unique url for store product image
def unique_product_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{slugify(instance.product.product_name)}-{uuid.uuid4().hex}.{ext}"
    return os.path.join('product_images/', filename)

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_description = models.CharField(max_length=500)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_price = models.IntegerField()  # No decimals
    trending = models.BooleanField(default=False)
    new_arrival = models.BooleanField(default=False)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=unique_product_image_path)

    def delete(self, *args, **kwargs):
        # Delete the file from storage
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)
