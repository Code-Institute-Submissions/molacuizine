from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category
from django.db.models import Q
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def all_products(request):
    """ A view to return all products  """

    products = Product.objects.all()

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
    end = count % 5
    # Code to provide page references in pagination
    object_start = ((page_number-1) * 5) + 1
    if page_number == page_num[-1]:
        object_finish = object_start + end-1
    else:
        object_finish = object_start + 4

    previous_page = page_number - 1
    next_page = page_number + 1
    last_page = page_num[-1]
    context = {
        'page_number': page_number,
        'page_num': page_num,
        'objects': objects,
        'count': count,
        'start': object_start,
        'finish': object_finish,
        'next': next_page,
        'previous': previous_page,
        'last': last_page,
    }
    return render(request, 'products/products.html', context)


def query_search(request):
    """ A view to return products when searching using search bar
     including pagination"""

    products = Product.objects.all()

    if 'q' in request.GET:
        query = request.GET['q']
        # Query is blank query= ""
        if not query:
            return redirect(reverse('products'))
        else:
            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # Add pagination numbers and links to product page

    if 'page_number' in request.GET:
        page_number = int(request.GET['page_number'])
    else:
        page_number = 1

    count = products.count()
    objects = products

    p = Paginator(objects, 5)
    page_num = list(range(1, p.num_pages+1))
    objects = objects[(page_number-1)*5:((page_number-1)*5)+5]
    end = count % 5

    # Code to provide page references in pagination

    object_start = ((page_number-1) * 5) + 1
    if page_number == page_num[-1]:
        object_finish = object_start + end-1
    else:
        object_finish = object_start + 4

    previous_page = page_number - 1
    next_page = page_number + 1
    last_page = page_num[-1]
    context = {
        'query': query,
        'page_number': page_number,
        'page_num': page_num,
        'objects': objects,
        'count': count,
        'start': object_start,
        'finish': object_finish,
        'next': next_page,
        'previous': previous_page,
        'last': last_page,
    }
    return render(request, 'products/query_search.html', context)


def category_search(request):
    """ A view to return products when searching category
        including pagination"""

    products = Product.objects.all()
    category = None

    if 'category' in request.GET:
        category = request.GET['category']
        products = products.filter(category__name=category)
        friendly_name = (get_object_or_404(
            Category, name=category)).friendly_name

    # Add pagination numbers and links to product page

    if 'page_number' in request.GET:
        page_number = int(request.GET['page_number'])
    else:
        page_number = 1

    count = products.count()
    objects = products

    p = Paginator(objects, 5)
    page_num = list(range(1, p.num_pages+1))
    objects = objects[(page_number-1)*5:((page_number-1)*5)+5]
    end = count % 5

    # Code to provide page references in pagination

    object_start = ((page_number-1) * 5) + 1
    if page_number == page_num[-1]:
        object_finish = object_start + end-1
    else:
        object_finish = object_start + 4

    previous_page = page_number - 1
    next_page = page_number + 1
    last_page = page_num[-1]
    context = {
        'friendly_name': friendly_name,
        'page_number': page_number,
        'page_num': page_num,
        'objects': objects,
        'current_category': category,
        'count': count,
        'start': object_start,
        'finish': object_finish,
        'next': next_page,
        'previous': previous_page,
        'last': last_page,
    }
    return render(request, 'products/category_search.html', context)


def product_detail(request, product_id):
    """ A view to return product a with specific id/pk """
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def store_management(request):
    """ A view to manage store products, openning hours
        and add items
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    if request.method == 'POST':

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Item could not be added. Please ensure the form is valid.')

    else:
        form = ProductForm()

    context = {
        'form': form,
    }
    return render(request, 'products/store_management.html', context)


@login_required
def product_update(request, product_id):
    """ A view to manage update items in product database
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Item could not be added. Please ensure the form is valid.')

    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'products/product_update.html', context)


@login_required
def product_delete(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
