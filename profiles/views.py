from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def profile(request):
    """ Display the user's profile. """

    profile = get_object_or_404(UserProfile, user__username=request.user)

    form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'profiles/profile.html', context)
