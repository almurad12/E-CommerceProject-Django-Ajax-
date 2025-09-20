from django.contrib import admin
from django.utils.html import format_html
from .models import category,sub_category,sliderItem,Product,ProductImage,Order
'''
# Register your models here.
admin.site.register(category)
admin.site.register(sub_category)
admin.site.register(sliderItem)


class ProductImageInline(admin.TabularInline):  # অথবা StackedInline ব্যবহার করতে পারেন
    model = ProductImage
    extra = 1  # নতুন ফাঁকা ফিল্ড কয়টা দেখাবে
    fields = ("name", "image", "preview_image")
    readonly_fields = ("preview_image",)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" />', obj.image.url)
        return "No Image"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "discount", "afterdiscountprice", "preview_cover")
    inlines = [ProductImageInline]   # ✅ Inline যোগ হলো
    search_fields = ("name",)
    list_filter = ("trending", "newArriable", "sub_category")

    def preview_cover(self, obj):
        if obj.coverphoto:
            return format_html('<img src="{}" width="80" height="80" />', obj.coverphoto.url)
        return "No Cover"
    preview_cover.short_description = "Cover Photo"



@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "preview_image")

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" />', obj.image.url)
        return "No Image"
    preview_image.short_description = "Preview"
    '''
# ------------------------------
# ProductImage Inline (for Product)
# ------------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("name", "image", "preview_image")
    readonly_fields = ("preview_image",)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" />', obj.image.url)
        return "No Image"


# ------------------------------
# Product Admin
# ------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "price", "discount", "afterdiscountprice",
        "quantity", "trending", "newArriable", "preview_cover", "sub_category"
    )
    list_filter = ("trending", "newArriable", "sub_category")
    search_fields = ("name",)
    inlines = [ProductImageInline]

    def preview_cover(self, obj):
        if obj.coverphoto:
            return format_html('<img src="{}" width="80" height="80" />', obj.coverphoto.url)
        return "No Cover"
    preview_cover.short_description = "Cover Photo"


# ------------------------------
# ProductImage Admin
# ------------------------------
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "name", "preview_image")
    search_fields = ("product__name", "name")

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" />', obj.image.url)
        return "No Image"
    preview_image.short_description = "Preview"


# ------------------------------
# Category Admin
# ------------------------------
@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


# ------------------------------
# SubCategory Admin
# ------------------------------
@admin.register(sub_category)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category",)
    search_fields = ("name", "category__name")


# ------------------------------
# Slider Admin
# ------------------------------
@admin.register(sliderItem)
class SliderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "preview_image")

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="60" />', obj.image.url)
        return "No Image"
    preview_image.short_description = "Preview"

admin.site.register(Order)
