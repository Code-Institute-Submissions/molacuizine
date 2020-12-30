from django.shortcuts import render
from .models import Product, Category


# Create your views here.
def all_products(request):
    """ A view to return all products and product search """
    products = Product.objects.all()
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category']
            products = products.filter(category__name=categories)
            categories = Category.objects.filter(name=categories)
            print(categories)
    context = {
        'products': products,
        'current_category': categories,
    }
    return render(request, 'products/products.html', context)
