"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path,include
from mainshop.views import home,shopSingleproduct,ShopList,SearchProduct,add_to_cart,show_cart,checkout,remove_from_cart,admindashbaord,CategoryViewSet,SubCategoryViewSet,SliderItemViewSet,adminproduct,ProductViewSet,ProductImageViewSet,create_product,ProductListAPIView,ProductDetailAPIView,loginAdminSite,admin_logout,get_all_session,orderItem,WatchlistAPI
# watchlist_add_cookie,show_cookies,remove_from_wishlist,
from rest_framework_nested import routers

# shopAllproduct,
router = DefaultRouter()
router.register(r'admincategory', CategoryViewSet, basename='admincategory')
router.register(r'adminsubcategory', SubCategoryViewSet, basename='SubCategoryViewset')
router.register(r'slider', SliderItemViewSet, basename='slider')
##for product
# router.register(r'products', ProductViewSet, basename='product')
# products_router = routers.NestedDefaultRouter(router, r'products', lookup='product')
# products_router.register(r'product-images-variant', ProductImageViewSet, basename='product-images')
urlpatterns = [
    path('',home,name='home'),
    path('shop/<int:id>/',shopSingleproduct),
    # path('shop/',shopAllproduct),
    path('shop/', ShopList.as_view(), name='shop-list'),
    path('search-products/', SearchProduct.as_view(), name='search-products'),
    # path("watchlist/", watchlist_add_cookie, name="watchlist_add_cookie"),
    # path("showcookielist/", show_cookies, name="show_cookies"),
    # path("wishlist/remove/", remove_from_wishlist, name="remove_from_wishlist"),
    path("cart/", add_to_cart , name="addtocart"),
    path("cart/show/", show_cart , name="showcart"),
    path("remove_from_cart/",remove_from_cart, name="remove_from_cart"),
    path("checkout/", checkout , name="checkout"),
    path("loginadminsite/",loginAdminSite,name="loginAdminSite"),
    path("logout/",admin_logout,name="adminlogout"),
    path("admindashboard/", admindashbaord , name="admindashbaord"),
    path("adminproduct/", adminproduct , name="adminproduct"),
    ##create product
    path("create-product/", create_product , name="create_product"),
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
    # path("admincategory/", CategoryViewSet , name="admincategory"),
    #updated watchlist
    path("api/watchlist/", WatchlistAPI.as_view(), name="watchlist-api"),
    #updated watchlist
    path("get-session/", get_all_session, name=" get_all_session"),
    path("order/",orderItem, name="orderItem"),

]
urlpatterns += router.urls
##add product and product image together in url
# urlpatterns += products_router.urls