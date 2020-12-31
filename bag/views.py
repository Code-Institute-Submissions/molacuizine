from django.shortcuts import (
    render, redirect, reverse)


# Create your views here.
def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, product_id):
    """ A view that add's specific product to bag"""
    if request.POST:
        # product = Products.get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('quantity'))

        # Create or call existing bag
        bag = request.session.get('bag', {})

        if product_id in bag.keys():
            bag[product_id] += quantity
        else:
            bag[product_id] = quantity

    request.session['bag'] = bag
    print(bag)
    return redirect(reverse('product_detail', args=[product_id]))