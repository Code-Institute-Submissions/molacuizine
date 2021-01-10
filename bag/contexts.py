from products.models import Product
from django.shortcuts import get_object_or_404, HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
import datetime
from django.contrib import messages


# Create your views here.
@require_POST
def store_status(request):
    """ A view to manage store open close status """
    try:
        status = request.POST.get('status')
        print(status)
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
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

    '''Code to show if shop is open or closed'''

    hours = datetime.datetime.now().hour
    mins = datetime.datetime.now().minute

    totalMins = hours * 60 + mins
    totalMins = 370
    if 0 <= totalMins < 360:
        delta = 360 - totalMins
        mins = delta % 60
        hours = int((delta-mins)/60)
        if hours < 1:
            open_message = (
                f'We are closed. Orders start in {mins} mins')
        else:
            open_message = (
                f'We are closed. Orders start in {hours} hours and {mins} mins')
        open_status = False
    elif totalMins < 1080:
        open_message = "We are open!"
        open_status = True
    elif totalMins <= 1439:
        delta = 1440 - totalMins + 360
        mins = delta % 60
        hours = int((delta-mins)/60)
        open_message = (
            f'We are closed. Orders start in {hours} hours and {mins} mins')
        open_status = False
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
