from orders.models import Cart


def cart_processor(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return {'cart_count': cart.get_item_count()}
    return {'cart_count': 0}
