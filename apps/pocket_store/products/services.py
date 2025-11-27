from django.db.models import Q,CharField
from django.db.models.functions import Cast

def filter_products(products, params):

    category = params.get("category", None)
    if category:
        products = products.filter(category_name__icontains=category)
    
    status = params.get("status", None)
    if status:
        products = products.filter(status=status)

    stock = params.get("stock", None)
    if stock:
        stock = stock.lower()
        if stock == "available":
            products = products.filter(stock__gt=0)
        elif stock == "unavailable":
            products = products.filter(stock__lte=0)


    # --- Filtros de rango ---
    price_min = params.get("price_min", None)
    if price_min:
        try:
            price_min = float(price_min)
            products = products.filter(price__gte=price_min)
        except ValueError:
            pass  # ignorar si no es un número válido

    price_max = params.get("price_max", None)
    if price_max:
        try:
            price_max = float(price_max)
            products = products.filter(price__lte=price_max)
        except ValueError:
            pass  # ignorar si no es un número válido

    return products

def search_products(products, params):
    search = params.get("search")
    if not search:
        return products

    # Convertimos los campos numéricos a string
    products = products.annotate(
        stock_str=Cast("stock", CharField()),
        price_str=Cast("price", CharField()),
        discount_str=Cast("discount", CharField()),
        rating_str=Cast("rating", CharField()),
    )

    # Creamos un OR gigante entre campos string
    query = (
        Q(name__icontains=search) |
        Q(description__icontains=search) |
        Q(category_name__icontains=search) |
        Q(stock_str__icontains=search) |
        Q(price_str__icontains=search) |
        Q(discount_str__icontains=search) |
        Q(rating_str__icontains=search)
    )

    return products.filter(query)