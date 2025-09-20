from .models import main_category
def menu_items(request):
    return {
        'main_categories':main_category.objects.prefetch_related('maincategory').all()
    }