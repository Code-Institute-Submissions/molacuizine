from django.shortcuts import render, redirect, reverse
from .models import Product, Category
from django.db.models import Q

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

        if 'q' in request.GET:
            query = request.GET['q']
            # Query is blank query= ""
            if not query:
                return redirect(reverse('products'))
            else:
                queries = Q(
                    name__icontains=query) | Q(description__icontains=query)
                products = products.filter(queries)

    context = {
        'products': products,
        'current_category': categories,
    }
    return render(request, 'products/products.html', context)
