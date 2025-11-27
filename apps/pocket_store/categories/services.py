from django.db.models import Q,CharField
from django.db.models.functions import Cast

def search_categories(categories, params):
    search = params.get("search")
    if not search:
        return categories

    return categories.filter(name__icontains=search)