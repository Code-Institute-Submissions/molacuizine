from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
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
        spice_index = (request.POST.get('spice_index'))
        # Create or call existing bag
        bag = request.session.get('bag', {})
        if 'spice_index' in request.POST:
            # Product already exists in bag
            if product_id in bag.keys():
                if spice_index in bag[product_id]['spice_index'].keys():
                    bag[product_id]['spice_index'][spice_index] += quantity
                    messages.success(request, f'Updated {product.name} with \
                    spice index of {spice_index} to your bag')
                # Spice index does not exists in bag
                else:
                    bag[product_id]['spice_index'][spice_index] = quantity
                    messages.success(request, f'Added {product.name} with \
                    spice index of {spice_index} to your bag')
            # Product does not exists in bag
            else:
                bag[product_id] = {'spice_index': {spice_index: quantity}}
                messages.success(request, f'Added {product.name} with \
                spice index of {spice_index} to your bag')
        # Product has no spice index
        else:
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
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})
    spice_index = None
    if 'spice_index' in request.POST:
        spice_index = request.POST['spice_index']
        bag[product_id]['spice_index'][spice_index] = quantity
        messages.success(request, f'Updated {product.name} quantity \
        with spice index of {spice_index} to {quantity}')
    else:
        bag[product_id] = quantity
        messages.success(request, f'Updated {product.name} \
        quantity to {quantity}')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def delete_from_bag(request, product_id):
    """View to remove item from the shopping bag"""

    product = get_object_or_404(Product, pk=product_id)
    try:
        spice_index = None
        if 'spice_index' in request.POST:
            spice_index = request.POST['spice_index']
        bag = request.session.get('bag')

        if spice_index:
            del bag[product_id]['spice_index'][spice_index]
            if not bag[product_id]['spice_index']:
                bag.pop(product_id)
                messages.success(request, f'Removed {product.name} from bag')
        else:
            bag.pop(product_id)
            messages.success(request, f'Removed {product.name} from bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
