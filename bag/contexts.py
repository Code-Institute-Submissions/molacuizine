from products.models import Product
from django.shortcuts import get_object_or_404


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
    print(bag_items)
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
    }

    return context
