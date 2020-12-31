from products.models import Product
from django.shortcuts import get_object_or_404
import datetime


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
    mins = datetime.datetime.now().hour

    totalMins = hours * 60 + mins

    if 0 <= totalMins < 360:
        delta = 360 - totalMins
        mins = delta % 60
        hours = int((delta-mins)/60)
        message = f'We will be open in {hours} hours and {mins} mins'
    elif totalMins < 1080:
        message = "we are open!"
    elif totalMins <= 1439:
        delta = 1440 - totalMins + 360
        mins = delta % 60
        hours = int((delta-mins)/60)
        message = f'We will be open in {hours} hours and {mins} mins'
    print(message)
    context = {
        'message': message,
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
    }
    
    return context
