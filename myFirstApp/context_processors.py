from .models import Profile

def cart_count(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(User=request.user).first()
    return {'cartCount': profile.cartCount if profile else 0}
