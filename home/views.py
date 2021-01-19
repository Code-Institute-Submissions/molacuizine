from django.shortcuts import render
from profiles.models import Town


def index(request):
    """ A view to return the index page """

    towns = Town.objects.all()
    context = {
        'towns': towns
    }
    return render(request, 'home/index.html', context)
