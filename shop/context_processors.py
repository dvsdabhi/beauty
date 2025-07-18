from .models import CartItem

def cart_item_count(request):
    count = 0
    customer_id = request.session.get('customer_id')

    if customer_id:
        count = CartItem.objects.filter(customer_id=customer_id).count()

    return {'cart_item_count': count}
