from rest_framework import serializers
from .models import Product,category,sub_category,sliderItem,ProductImage, Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



###this serilizer for admin
#category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = '__all__'

##subcategory
# class SubCategorySerializer(serializers.ModelSerializer):
#     category_name = serializers.CharField(source='category.name', read_only=True)

#     class Meta:
#         model = sub_category
#         fields = ['id', 'name', 'category', 'category_name']
class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = sub_category
        fields = ['id', 'name', 'category', 'category_name']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else ""

##slider serializers
class SliderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = sliderItem
        fields = ['id', 'image']


###product Image and product serializer crud together
##this serializer only for product
class SubCategorySerializerImg(serializers.ModelSerializer):
    class Meta:
        model = sub_category
        fields = ['id', 'name']  # Include whatever fields you need

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'name', 'image']
        


class ProductSerializer(serializers.ModelSerializer):
    # nested read
    productimages = ProductImageSerializer(many=True, read_only=True)
    sub_category = SubCategorySerializerImg(read_only=True)

    # nested write
    new_images = ProductImageSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'discount', 'afterdiscountprice',
            'description1', 'description2', 'quantity',
            'coverphoto', 'trending', 'newArriable',
            'sub_category', 'productimages', 'new_images'
        ]

    def create(self, validated_data):
        new_images = validated_data.pop('new_images', [])
        product = Product.objects.create(**validated_data)
        for img in new_images:
            ProductImage.objects.create(product=product, **img)
        return product

    def update(self, instance, validated_data):
        new_images = validated_data.pop('new_images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for img in new_images:
            ProductImage.objects.create(product=instance, **img)
        return instance
    # /for absoulte url
    def get_coverphoto(self, obj):
        request = self.context.get("request")
        if obj.coverphoto and hasattr(obj.coverphoto, "url"):
            return request.build_absolute_uri(obj.coverphoto.url)
        return None
    

class  OrderSerializer(serializers.ModelSerializer):
    formatted_date = serializers.SerializerMethodField()
    class Meta:
        model =  Order
        fields = "__all__"
    
    def get_formatted_date(self, obj):
        return obj.created_at.strftime("%b %d, %Y %I:%M %p")  # e.g. "Oct 05, 2025 09:12 PM"