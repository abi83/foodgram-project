from apps.recipes.models import CartItem


def cart_count(request):
    """
    A context processor making 'cart_count' variable available in templates
    """
    if request.user.is_authenticated:
        return {
            'cart_count': CartItem.objects.filter(user=request.user).count()
        }
    cart_ids = (request.session.get('cart')
                if request.session.get('cart')
                else [])
    return {'cart_count': len(cart_ids)}
