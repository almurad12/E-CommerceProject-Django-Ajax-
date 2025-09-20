from django.shortcuts import render
# Create your views here.
from .models import Product,ProductImage,main_category
def shop(request):
    product = Product.objects.all()
    # product = Product.objects.filter(category_name_id=2)
    # product=Product.objects.filter(category_name__main_category_id=1)
    return render(request, 'shop1/index.html',{'product':product})

def singleProduct(request):
    return render(request,'shop1/singleproduct2.html')

def home(request):
    return render(request,'shop1/home.html')

def allProduct(request):
    return render(request,'shop1/allproduct.html')
def checkout(request):
    return render(request,'shop1/checkout.html')
