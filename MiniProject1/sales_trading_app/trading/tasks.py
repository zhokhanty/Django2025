from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Order

@shared_task
def process_order(order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.status == 'pending':
            order.status = 'executed'
            order.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "orders",
                {
                    "type": "send_order_update",
                    "order": {
                        "id": order.id,
                        "product": order.product,
                        "status": order.status,
                        "user": order.user.username,
                        "order_type": order.order_type,
                        "quantity": float(order.quantity),
                        "price": float(order.price),
                    }
                }
            )
            return f"Order {order_id} executed successfully"
        return f"Order {order_id} was already processed"
    except Order.DoesNotExist:
        return f"Order {order_id} does not exist"
