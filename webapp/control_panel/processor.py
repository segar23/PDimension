from orders.models import Order


def orderscounter(request):
    return {'orderscounter': Order.objects.filter(status=Order.OrderStatus.UNREAD, isFinalized=True)}
