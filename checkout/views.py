from django.shortcuts import (
    render, get_object_or_404, redirect, reverse, HttpResponse)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm
from profiles.models import UserProfile
from .models import OrderLineItem, Order
from products.models import Product
from bag.models import Store
from bag.contexts import bag_contents
from profiles.forms import UserProfileForm
from django.conf import settings
from django.views.decorators.http import require_POST
import json
import stripe


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'save_info': request.POST.get('save_info'),
            'request': request.POST.get('request'),
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


# Create your views here.
@login_required
def checkout(request):
    """ view to display checkout page """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    store_status = get_object_or_404(Store, id=1)

    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    if store_status.store_status == "close":
        messages.error(
            request, "We are presently closed and cannot accept payments")
        return redirect(reverse('products'))

    profile = get_object_or_404(UserProfile, user__username=request.user)

    if request.method == 'POST':
        save_info = request.POST.get('save-info')
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.original_bag = json.dumps(bag)
            order.user_profile = profile
            order.save()
            # Save items to Orderlineitem
            for item_id, item_data in bag.items():
                product = Product.objects.get(id=item_id)
                lineitem_total = product.price * item_data
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=item_data,
                    lineitem_total=lineitem_total,
                )
                order_line_item.save()

            ''' Update profile data if checked by user'''
            if save_info:
                profile_data = {
                    'default_phone_number': order.phone_number,
                    'default_street_address1': order.street_address,
                    'town': order.town,
                    'default_postcode': order.postcode,
                }
                user_profile_form = UserProfileForm(
                    profile_data, instance=profile)

                if user_profile_form.is_valid():
                    user_profile_form.save()

            return redirect(reverse(
                'checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    # Get request
    else:
        # Create Stripe intent request

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key

        intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
                metadata={
                    'bag': json.dumps(request.session.get('bag', {})),
                    'username': request.user,
                },
            )

        order_form = OrderForm(initial={
            'full_name':
                profile.user.first_name + " " + profile.user.last_name,
            'email': profile.user.email,
            'phone_number': profile.default_phone_number,
            'postcode': profile.default_postcode,
            'town': profile.town,
            'street_address': profile.default_street_address1,
            })

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)
