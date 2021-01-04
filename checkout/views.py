from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm
from profiles.models import UserProfile


# Create your views here.
@login_required
def checkout(request):
    """ view to display checkout page """

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    profile = get_object_or_404(UserProfile, user__username=request.user)

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
