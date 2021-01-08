from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm
from profiles.models import UserProfile
from .models import OrderLineItem
from products.models import Product
from bag.contexts import bag_contents
import json


# Create your views here.
@login_required
def checkout(request):
    """ view to display checkout page """

    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    profile = get_object_or_404(UserProfile, user__username=request.user)

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.original_bag = json.dumps(bag)
            order.save()
            # Save items to Orderlineitem
            for item_id, item_data in bag.items():
                product = Product.objects.get(id=item_id)
                lineitem_total = product.price * item_data
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=item_data,
                    lineitem_total = lineitem_total,
                )
                order_line_item.save()
                return redirect(reverse('product'))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    # Get request
    else:
        
        order_form = OrderForm(initial={
            'full_name': profile.user.first_name + " " + profile.user.last_name,
            'email': profile.user.email,
            'phone_number': profile.default_phone_number,
            'postcode': profile.default_postcode,
            'town': profile.town,
            'street_address': profile.default_street_address1,
            })

    context = {
        'order_form': order_form,
    }
    return render(request, 'checkout/checkout.html', context)
