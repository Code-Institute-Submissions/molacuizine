from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator
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

        if 'q' in request.GET:
            query = request.GET['q']
            # Query is blank query= ""
            if not query:
                return redirect(reverse('products'))
            else:
                queries = Q(
                    name__icontains=query) | Q(description__icontains=query)
                products = products.filter(queries)

    count = products.count()

    # Add pagination numbers and links to product page

    if 'page_number' in request.GET:
        page_number = int(request.GET['page_number'])

    else:
        page_number = 1

    objects = products

    p = Paginator(objects, 5)
    page_num = list(range(1, p.num_pages+1))
    objects = objects[(page_number-1)*5:((page_number-1)*5)+5]

    context = {
        'page_num': page_num,
        'objects': objects,
        'current_category': categories,
        'count': count,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to return product a with specific id/pk """
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)


def category_search(request):
    """ A view to return products when searching with pagination"""

    products = Product.objects.all()
    category = None

    if 'category' in request.GET:
        category = request.GET['category']
        products = products.filter(category__name=category)
        friendly_name = (get_object_or_404(
            Category, name=category)).friendly_name
    if 'page_number' in request.GET:
        page_number = int(request.GET['page_number'])
    else:
        page_number = 1
    objects = products

    p = Paginator(objects, 5)
    page_num = list(range(1, p.num_pages+1))
    objects = objects[(page_number-1)*5:((page_number-1)*5)+5]

    count = products.count()

    context = {
        'page_num': page_num,
        'objects': objects,
        'current_category': category,
        'friendly_name': friendly_name,
        'count': count,
    }
    return render(request, 'products/category_search.html', context)
