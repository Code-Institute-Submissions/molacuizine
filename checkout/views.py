from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def checkout(request):
    """ view to display checkout page """

    context = {
    }
    return render(request, 'checkout/checkout.html', context)
