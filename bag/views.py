from django.shortcuts import render, redirect, reverse


# Create your views here.
def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, product_id):
    """ A view that renders the bag contents page """

    return redirect(reverse('product_detail', args=[product_id]))
