from django.shortcuts import (
    render, redirect, reverse, get_object_or_404)
from django.contrib import messages
from products.models import Product
from django.views.decorators.http import require_POST


# Create your views here.
@require_POST
def store_status(request):
    """ A view to store open close status """

    return render(request, 'bag/bag.html')


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

    return redirect(reverse('product_detail', args=[product_id]))


def adjust_bag(request, product_id):
    """ A view to adjust bag content"""

    product = get_object_or_404(Product, pk=product_id)

    if request.POST:

        quantity = int(request.POST.get('quantity'))

        # Request existing bag
        bag = request.session.get('bag', {})
        # Update quantity
        bag[product_id] = quantity

    request.session['bag'] = bag
    messages.success(request, f'Updated {product.name} quantity')

    return redirect(reverse('view_bag'))


def delete_from_bag(request, product_id):
    """View to remove item from the shopping bag"""

    product = get_object_or_404(Product, pk=product_id)

    bag = request.session.get('bag')
    bag.pop(product_id)
    request.session['bag'] = bag

    messages.success(request, f'{product.name} removed from bag')

    return redirect(reverse('view_bag'))
