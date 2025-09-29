from django.shortcuts import render,get_object_or_404
from mainshop.models import sliderItem,Product,ProductImage
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
##this is for admin
from mainshop.models import category,sub_category
from mainshop.serializers import CategorySerializer,SubCategorySerializer,SliderItemSerializer, ProductSerializer, ProductImageSerializer
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
# Create your views here.
# def base(request):
#      return render(request,'mainshop/base.html',{'slides': slides})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAdminUser

def home(request):
    #for slide filtering
    slides = sliderItem.objects.all()
    #for trending filtering
    product = Product.objects.filter(trending=True)
    #for newarriable filtering 
    newArriable = Product.objects.filter(newArriable=True)
    #for show all product 
    productAll = Product.objects.all()[:12]
    return render(request,'mainshop/home.html',{'slides': slides,'product':product,'newArriable':newArriable,'productAll':productAll})

def shopSingleproduct(request,id):
    product = get_object_or_404(Product, id=id)
    productImage = ProductImage.objects.filter(product_id=id)
    for img in productImage:
        print(img.name)
        print(img.image)
    return render(request,'mainshop/singleproduct1.html',{'product':product,'productImage': productImage})



##rest view for all product
class ShopList(APIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    def get(self, request):
        product = Product.objects.all()
        # ######################
        # --- filter by category / subcategory ---
        category = request.GET.get("category")
        subcategory = request.GET.get("subcategory")

        if category:
            # product = product.filter(category__id=category)  # or category__slug / name depending on your model
            # product = Product.objects.filter(sub_category__category__id=category)
            product = product.filter(sub_category__category__id=category)
        if subcategory:
            print(subcategory)
            # product = product.filter(subcategory__id=subcategory)
            product = product.filter(sub_category__id=subcategory)
        ##############

         # paginate manually
        paginator = PageNumberPagination()
        paginator.page_size = 16   # same as settings or override
        result_page = paginator.paginate_queryset(product, request)
        serializer = ProductSerializer(result_page, many=True)
        # return Response(serializer.data)
        if request.accepted_renderer.format == 'html':
            return Response({'products': serializer.data}, template_name='mainshop/allproduct7.html')

        return paginator.get_paginated_response(serializer.data)
    


class SearchProduct(APIView):
    def get(self, request):
        search_query = request.GET.get("search", "")
        products = Product.objects.filter(name__icontains=search_query)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

'''
def watchlist_add_cookie(request):
    product_id = request.GET.get("product_id")
    if not product_id:
        return JsonResponse({"error": "No product_id provided"}, status=400)

    # Get existing cookie
    product_cookie = request.COOKIES.get("product_ids")
    # print(product_cookie)

    if product_cookie:
        product_list = json.loads(product_cookie)
        print("ppp",product_list)
    else:
        product_list = []

    # ✅ Check if already exists (compare by id)
    if any(str(p["id"]) == str(product_id) for p in product_list):
        return JsonResponse({"status": "already exists", "product_ids": product_list})

    # ✅ Fetch product details
    try:
        product = Product.objects.get(id=product_id)
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.afterdiscountprice,
            "photo": product.coverphoto.url if product.coverphoto else ""  # ✅ FIXED
        }
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    # ✅ Add new product to cookie list
    product_list.append(product_data)

    # ✅ Return and update cookie
    response = JsonResponse({
        "status": "added",
        "product": product_data,
        "product_ids": product_list
    })
    response.set_cookie(
        "product_ids",
        json.dumps(product_list),
        max_age=3600*24*7  # 7 days
    )
    return response


def show_cookies(request):
    product_cookie = request.COOKIES.get("wishlist")
    if product_cookie:
        try:
            product_ids = json.loads(product_cookie)  # cookie থেকে list of ids
        except json.JSONDecodeError:
            product_ids = []
    else:
        product_ids = []

    # এখন DB থেকে সব product details আনবো
    products = Product.objects.filter(id__in=product_ids)

    # ধরো তুমি একটা serializer বানিয়েছো
    product_data = [
        {   
            "id": p.id,
            "name": p.name,
            "price": p.afterdiscountprice,
            "image": p.coverphoto.url if p.coverphoto else None,
            "url": f"/shop/{p.id}/"
        }
        for p in products
    ]

    return JsonResponse({"products": product_data,
                         "cartitem":products.count()})


def remove_from_wishlist(request):
    product_id = request.GET.get("product_id")
    if not product_id:
        return JsonResponse({"error": "No product_id provided"}, status=400)

    wishlist_cookie = request.COOKIES.get("wishlist", "[]")
    try:
        wishlist = json.loads(wishlist_cookie)
        wishlist = [int(x) for x in wishlist]  # 🔹 normalize to ints
    except json.JSONDecodeError:
        wishlist = []

    product_id = int(product_id)
    if product_id in wishlist:
        wishlist.remove(product_id)

    response = JsonResponse({
        "message": "Removed successfully",
        "wishlist": wishlist,
        "count": len(wishlist)
    })

    response.set_cookie(
        "wishlist",
        json.dumps(wishlist),
        path="/",
        max_age=60*60*24*7  # 7 days
    )

    return response
'''
# updated watchlist
# @csrf_exempt 
class WatchlistAPI(APIView):
    cookie_name = "product_ids"

    def get_watchlist(self, request):
        """Helper to load watchlist from cookie"""
        cookie_data = request.COOKIES.get(self.cookie_name, "[]")
        try:
            raw_data = json.loads(cookie_data)
            watchlist = []
            for x in raw_data:
                if isinstance(x, dict) and "product_id" in x:
                    watchlist.append(int(x["product_id"]))
                else:
                    watchlist.append(int(x))
            return watchlist
        except (json.JSONDecodeError, ValueError, TypeError):
            return []

    def set_watchlist_cookie(self, response, watchlist):
        """Helper to update cookie"""
        response.set_cookie(
            key=self.cookie_name,
            value=json.dumps(watchlist),  # ✅ always save only a list of ints
            max_age=60 * 60 * 24 * 7,     # 7 days
            path="/",
            samesite="Lax",
            secure=False  # set True in production (HTTPS)
        )
        return response

    # ✅ Show watchlist with product details
    def get(self, request):
        product_ids = self.get_watchlist(request)
        products = Product.objects.filter(id__in=product_ids)

        product_data = [
            {
                "id": p.id,
                "name": p.name,
                "price": p.afterdiscountprice,
                "image": p.coverphoto.url if p.coverphoto else None,
                "url": f"/shop/{p.id}/"
            }
            for p in products
        ]

        return Response({
            "products": product_data,
            "cartitem": products.count()
        })

    # ✅ Add to watchlist
    def post(self, request):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "No product_id provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_id = int(product_id)
        except ValueError:
            return Response({"error": "Invalid product_id"}, status=status.HTTP_400_BAD_REQUEST)

        watchlist = self.get_watchlist(request)
        if product_id not in watchlist:
            watchlist.append(product_id)

        response = Response({
            "message": "Added successfully",
            "watchlist": watchlist,
            "count": len(watchlist)
        })
        return self.set_watchlist_cookie(response, watchlist)

    # ✅ Remove from watchlist
    def delete(self, request):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "No product_id provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_id = int(product_id)
        except ValueError:
            return Response({"error": "Invalid product_id"}, status=status.HTTP_400_BAD_REQUEST)

        watchlist = self.get_watchlist(request)
        if product_id in watchlist:
            watchlist.remove(product_id)

        response = Response({
            "message": "Removed successfully",
            "watchlist": watchlist,
            "count": len(watchlist)
        })
        return self.set_watchlist_cookie(response, watchlist)
# updated watchlist end

# for cart
def add_to_cart(request):
    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("quantity", 1))
    image_id = request.POST.get("image_id")

    product = Product.objects.get(id=product_id)
    image = ProductImage.objects.get(id=image_id)

    # ✅ cart dict structure রাখব
    cart = request.session.get("cart", {"items": [], "total": {}})

    items = cart["items"]

    # Check if the product+image already exists in cart
    item_found = False
    for item in items:
        if item["product_id"] == int(product_id) and item["image_id"] == int(image_id):
            item["quantity"] += quantity
            item["product_total"] = item["quantity"] * item["price"]
            item_found = True
            break

    if not item_found:
        # calculate total from existing items
        ProductAllTotal = sum(item["product_total"] for item in items)
        product_total = int(product.afterdiscountprice * quantity)

        items.append({
            "product_id": int(product_id),
            "product_name": product.name,
            "image_id": int(image_id),
            "quantity": quantity,
            "price": product.afterdiscountprice,
            "variant": image.name,
            "image_url": image.image.url,
            "product_total": product_total,
            "product_All_total": ProductAllTotal + product_total
        })

    # ✅ Delivery charge
    delivery_charge = 130
    subtotal = sum(item["product_total"] for item in items)
    grand_total = subtotal + delivery_charge

    # ✅ Save totals আলাদা key তে
    cart["total"] = {
        "subtotal": subtotal,
        "delivery_charge": delivery_charge,
        "grand_total": grand_total
    }

    # Save back to session
    request.session["cart"] = cart
    request.session.modified = True

    return JsonResponse({
        "status": "success",
        "cart": cart
    })


def show_cart(request):
    cart = request.session.get("cart", [])
    return JsonResponse({"cart": cart})

@csrf_exempt  # only for testing, better handle CSRF properly
def remove_from_cart(request):
    if request.method == "POST":
        product_id = int(request.POST.get("product_id"))
        image_id = int(request.POST.get("image_id"))
        # product_id = request.POST.get("product_id")
        # image_id = request.POST.get("image_id")
        # print(type(product_id),type(image_id))

        cart = request.session.get("cart", {"items": [], "total": {}})
        cart["items"] = [
            item for item in cart["items"]
            if not (item["product_id"] == product_id and item["image_id"] == image_id)
        ]

        # Recalculate totals
        subtotal = sum(item["product_total"] for item in cart["items"])
        delivery_charge = 130 if subtotal > 0 else 0
        grand_total = subtotal + delivery_charge

        cart["total"] = {
            "subtotal": subtotal,
            "delivery_charge": delivery_charge,
            "grand_total": grand_total
        }

        request.session["cart"] = cart
        request.session.modified = True

        return JsonResponse({"message": "Item removed", "cart": cart})




# #######This is for admin panel

def admindashbaord(request):
    category_count = category.objects.count()
    subcategory = sub_category.objects.count()
    slider = sliderItem.objects.count()
    product = Product.objects.count()

    print(category_count)
    return render(request,'admin_another/admindashboard.html',{"category":category_count,"slider":slider,"subcategory": subcategory,"product":product})
# def admincategory(request):
#     return render(request,'admin_another/category.html')

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if request.accepted_renderer.format == 'html':
            return Response({'categories': queryset}, template_name='admin_another/category.html')
        return Response(serializer.data)
    

# class SubCategoryViewset(viewsets.ModelViewSet):
#      def list(self, request, *args, **kwargs):
#         # queryset = self.get_queryset()
#         # serializer = self.get_serializer(queryset, many=True)
#         if request.accepted_renderer.format == 'html':
#             return Response(template_name='admin_another/subcategory.html')
        # return Response(serializer.data)
'''
class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = sub_category.objects.select_related('category').all()
    serializer_class = SubCategorySerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    permission_classes = [IsAdminUser]
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if request.accepted_renderer.format == 'html':
            return Response(template_name='admin_another/subcategory.html')
        return Response(serializer.data)
    '''
    # Force JSON response for DataTables
    

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = sub_category.objects.select_related('category').all()
    serializer_class = SubCategorySerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    # permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Force JSON response for AJAX/DataTables
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return Response(serializer.data)

        # Otherwise return template
        return Response(template_name="admin_another/subcategory.html")

class SliderItemViewSet(viewsets.ModelViewSet):
    queryset = sliderItem.objects.all()
    serializer_class = SliderItemSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    permission_classes = [IsAdminUser]
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if request.accepted_renderer.format == 'html':
            return Response(template_name='admin_another/adminSlider.html')
        return Response(serializer.data)
def adminproduct(request):
    subcategories = sub_category.objects.all()

    return render(request,'admin_another/product.html',{'subcategories':subcategories})

#procuct and product Image upload together
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().prefetch_related("productimages")
    serializer_class = ProductSerializer


class ProductImageViewSet(viewsets.ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product not found")
        return product.productimages.all()

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_pk')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product not found")
        serializer.save(product=product)



@csrf_exempt
def create_product(request):
    if request.method == "POST":
        product = Product.objects.create(
            name=request.POST.get("name"),
            sub_category_id=request.POST.get("sub_category") or None,
            price=int(request.POST.get("price")),
            discount=int(request.POST.get("discount")),
            afterdiscountprice=request.POST.get("afterdiscountprice"),
            description1=request.POST.get("description1"),
            description2=request.POST.get("description2"),
            trending=bool(request.POST.get("trending")),
            newArriable=bool(request.POST.get("newArriable")),
            coverphoto=request.FILES.get("coverphoto")
        )

        # 2. Create Product Images
        # images = request.FILES.getAll("image_file[]")  # multiple images
        images = request.FILES.getlist("image_file[]")
        names = request.POST.getlist("image_name[]")    # corresponding names
        print(images,names)

        for i, img in enumerate(images):
            name = names[i] if i < len(names) else f"Image {i+1}"

            ProductImage.objects.create(product=product, name=name, image=img)

        return JsonResponse({"status": "success", "product_id": product.name,})
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=400)


class ProductListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.select_related("sub_category").prefetch_related("productimages").all()
        serializer = ProductSerializer(products, many=True)
        return Response({"results": serializer.data})
    


class ProductDetailAPIView(APIView):

    # Get a single product by ID
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(
            Product.objects.select_related("sub_category").prefetch_related("productimages"),
            pk=pk
        )
        serializer = ProductSerializer(product, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update product
    def put(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Partial update
    def patch(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete product
    def delete(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"message": "Product deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    




# login admin site

def loginAdminSite(request):
    if request.user.is_authenticated:
        return redirect('admindashbaord')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admindashbaord')
        else:
            messages.error(request, "Invalid username or password!")
    return render(request, "admin_another/adminlogin.html")

def admin_logout(request):
    logout(request)   # this clears the session
    return redirect("loginAdminSite")  # replace with your login page name



# def 

# 


def checkout(request):
    value =request.session["cart"]
    return render(request,'mainshop/checkout.html',{"value":value})

def orderItem(request):
    if request.method == "POST":
        productOrdered = request.session.get("cart", {})
        try:
            # JSON থেকে dictionary তে data load করা
            data = json.loads(request.body)

            # চাইলে নিজের মতো করে সাজাতে পারেন
            order_details = {
                "name": data.get("name"),
                "phone": data.get("phone"),
                "address": data.get("address"),
                "district": data.get("district"),
                "thana": data.get("thana"),
                "payment_method": data.get("payment_method"),
            }

            print("📦 Order Data:",productOrdered,order_details)
            # 🟢 Order complete হলে cart empty করা
            if "cart" in request.session:
                del request.session["cart"]   # পুরোপুরি মুছে ফেলবে
                request.session.modified = True

            # এখন চাইলে database এ save করতে পারেন বা return করতে পারেন
            return JsonResponse({
                "status": "success",
                "order": order_details,
                "product": productOrdered,

            })
            

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        # value =request.session["cart"]

    # return JsonResponse(value,))


def get_all_session(request):
    
    return JsonResponse(dict(request.session))