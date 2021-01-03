from django.shortcuts import render, get_object_or_404

# Create your views here.
def profile(request):
    """ Display the user's profile. """

    profile = get_object_or_404(UserProfile, user__username=request.user)

    context = {
        'profile': profile,
    }
    return render(request, 'profiles/profile.html', context)
