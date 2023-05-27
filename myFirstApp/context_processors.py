from .models import Order

def cart_items(request):
    if request.user.is_authenticated:
        cart_items_count = Order.objects.filter(user=request.user, complete=False).count()
    else:
        cart_items_count = 0
    return {'cart_items_count': cart_items_count}
