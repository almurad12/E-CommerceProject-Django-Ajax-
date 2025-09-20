from django.contrib import admin

# Register your models here.
from .models import main_category,Category,Product,ProductImage
admin.site.register(main_category)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)