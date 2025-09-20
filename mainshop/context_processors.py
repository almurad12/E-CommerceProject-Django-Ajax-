from mainshop.models import category,sub_category
def categories_context(request):
    # return {
    #     "categories": category.objects.all(),
    #     "subcategories": sub_category.objects.select_related('category')
    # }
    categories_with_sub = []

    # Prefetch subcategories for efficiency
    cats = category.objects.all()
    subs = sub_category.objects.select_related('category')

    for cat in cats:
        cat_subs = [sub for sub in subs if sub.category_id == cat.id]
        categories_with_sub.append({
            "category": cat,
            "subcategories": cat_subs
        })
    return {
        "categories_with_sub": categories_with_sub
    }
