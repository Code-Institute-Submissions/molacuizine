from django.shortcuts import (
    render, redirect, reverse, get_object_or_404)
from django.contrib import messages
from products.models import Product


# Create your views here.
def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, product_id):
    """ A view that add's specific product to bag"""

    product = get_object_or_404(Product, pk=product_id)

    if request.POST:
        quantity = int(request.POST.get('quantity'))

        # Create or call existing bag
        bag = request.session.get('bag', {})

        if product_id in bag.keys():
            bag[product_id] += quantity
            messages.success(request, f'Added {product.name} to your bag')
        else:
            bag[product_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    print(bag)
    return redirect(reverse('product_detail', args=[product_id]))


def adjust_bag(request, product_id):
    """ A view to adjust bag content"""
    if request.POST:
        # product = Products.get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('quantity'))

        # Request existing bag
        bag = request.session.get('bag', {})

        bag[product_id] = quantity

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def delete_from_bag(request, product_id):
    """View to remove item from the shopping bag"""

    bag = request.session.get('bag')
    bag.pop(product_id)
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))
