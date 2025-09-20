
from django.urls import path
from shop1.views import *

urlpatterns = [
    path('',shop),
    path('singleproduct',singleProduct,name="singleproduct"),
    path('home/',home,name='home'),
    path('allproduct/',allProduct,name='shop'),
    # path('checkout/',checkout,name='checkout')

]