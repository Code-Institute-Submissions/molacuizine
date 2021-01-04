from django.shortcuts import render


# Create your views here.
def checkout(request):
    """ view to display checkout page """

    context = {
    }
    return render(request, 'checkout/checkout.html', context)
