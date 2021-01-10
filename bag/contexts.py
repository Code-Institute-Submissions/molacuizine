from products.models import Product
from django.shortcuts import get_object_or_404, HttpResponse, reverse, redirect
from django.conf import settings
from django.views.decorators.http import require_POST
import datetime
from django.contrib import messages
from bag.models import Store


# Create your views here.
@require_POST
def store_status(request):
    """ A view to manage store open close status """
    store_status = get_object_or_404(Store, id=1)
    try:
        status = request.POST.get('status')
        store_status.store_status = status
        store_status.save()

        messages.success(
            request, f'Store Status is now {store_status.store_status}')
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(
            request, 'Sorry store status could not be updated. Try again')
        return HttpResponse(content=e, status=400)


def bag_contents(request):
    '''View which contains bag order to be used across all apps'''
    product = 0
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})
    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        total += item_data * product.price
        product_count += item_data
        sub_total = item_data*product.price
        bag_items.append({
            'quantity': item_data,
            'product': product,
            'sub_total': sub_total,
        })

    '''Code to update if shop is open or closed'''

    store_status = get_object_or_404(Store, id=1)

    if store_status.store_status == "open":
        open_status = True
        open_message = "We are open!"
    else:
        open_status = False
        open_message = 'We are closed'
    
    context = {
        'open_message': open_message,
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'open_status': open_status,
        'transport': settings.TRANSPORT_COST,
        'grand_total': total + settings.TRANSPORT_COST,
    }

    return context
