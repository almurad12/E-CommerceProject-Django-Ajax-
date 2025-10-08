from django.db import models
import os
from django.utils.text import slugify
from django.db.models.signals import post_delete,pre_save
from django.dispatch import receiver

import datetime
import random
import string
from django.db import models
# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name
#subcategory
class sub_category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(category,on_delete=models.CASCADE,related_name='category')
   
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
#slider
class sliderItem(models.Model):
    image = models.ImageField(upload_to='slider/')
    class Meta:
        ordering = ['id']  # Ensures slides are always in insertion order
    def __str__(self):
        return f"Slide {self.pk}"
    ##if image is delete the image delete from storage
'''
@receiver(post_delete, sender=sliderItem)
def delete_slider_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)  # delete file but not the model no this is for no problem in database
'''

@receiver(pre_save, sender=sliderItem)
def delete_old_slider_image(sender, instance, **kwargs):
    if not instance.pk:
        return  # skip if new object

    try:
        old_image = sliderItem.objects.get(pk=instance.pk).image
    except sliderItem.DoesNotExist:
        return

    new_image = instance.image
    if old_image and old_image != new_image:
        old_image.delete(False)




##destination path for cover photo
#media/coverphoto/productname/cover.png
def product_cover_upload_path(instance, filename):
    # Product এর name অনুযায়ী coverphoto/<product_name>/<filename>
    folder_name = instance.name if instance.name else "unknown"
    return os.path.join("coverphoto", folder_name, filename)

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    afterdiscountprice = models.IntegerField(null=True, blank=True)  # stored in DB
    description1 = models.TextField(null=True, blank=True)
    description2 = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    # coverphoto = models.CharField(max_length=255, null=True, blank=True)
    coverphoto = models.ImageField(
        upload_to=product_cover_upload_path, blank=True,default="default/product_default.jpeg"
    )
    trending = models.BooleanField(default=False)
    newArriable = models.BooleanField(default=False)

    # productImage = models.ForeignKey('ProductImage', on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey('sub_category', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.discount > 0:
            self.afterdiscountprice = self.price - (self.price * self.discount // 100)
        else:
            self.afterdiscountprice = self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

#media/productphoto/samsung-galaxy-s23/back.jpg
def product_image_upload_path(instance, filename):
    # ProductImage এর name ব্যবহার করে ফোল্ডার তৈরি হবে
    folder_name = slugify(instance.name) if instance.name else "unknown"
    return os.path.join("productphoto", folder_name, filename)

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="productimages"
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to=product_image_upload_path)

    def __str__(self):
        return f"{self.product.name} - {self.name}" if self.name else f"Image {self.id}"
    

###order generate with date
'''
def generate_unique_custom_id():
    while True:
        # দিন-মাস-বছর (DD_MM_YY)
        today = datetime.datetime.now()
        date_str = today.strftime("%d_%m_%y")  # e.g., 15_09_25

        # 8-digit random number
        random_digits = ''.join(random.choices(string.digits, k=8))

        new_id = f"{date_str}{random_digits}"

        # Check in DB
        if not Product.objects.filter(id=new_id).exists():
            return new_id
            '''
def generate_unique_custom_id():
    while True:
        today = datetime.datetime.now()

        # date part without underscore — example: 051025
        date_str = today.strftime("%d%m%y")

        # 5 random digits — example: 38472
        random_digits = ''.join(random.choices(string.digits, k=5))

        # combine and convert to integer
        new_id = int(f"{date_str}{random_digits}")  # ✅ convert string to int

        # check in DB for uniqueness
        if not Order.objects.filter(id=new_id).exists():
            return new_id
class Order(models.Model):
    id = models.BigIntegerField(
        max_length=20,  # 8 (date) + 8 (random) = 16, buffer 20
        primary_key=True,
        default=generate_unique_custom_id,
        editable=False
    )
    order_products = models.JSONField(default=dict)   # product list / cart JSON
    address = models.JSONField(default=dict)          # shipping/billing address JSON
    created_at = models.DateTimeField(auto_now_add=True)