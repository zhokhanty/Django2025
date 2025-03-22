from celery import shared_task
from .models import Order, Transaction, Balance

@shared_task
def process_trade(order_id):
    try:
        order = Order.objects.get(id=order_id)
        balance, _ = Balance.objects.get_or_create(user=order.user)

        if order.order_type == "BUY":
            total_cost = order.quantity * order.price
            if balance.available_funds >= total_cost:
                balance.available_funds -= total_cost
                holdings = balance.holdings
                holdings[order.product.name] = holdings.get(order.product.name, 0) + order.quantity
                balance.holdings = holdings
                balance.save()
                order.status = "EXECUTED"
            else:
                order.status = "FAILED"

        elif order.order_type == "SELL":
            holdings = balance.holdings
            if holdings.get(order.product.name, 0) >= order.quantity:
                holdings[order.product.name] -= order.quantity
                balance.available_funds += order.quantity * order.price
                balance.holdings = holdings
                balance.save()
                order.status = "EXECUTED"
            else:
                order.status = "FAILED"

        order.save()
        return f"Order {order_id} processed successfully."

    except Order.DoesNotExist:
        return f"Order {order_id} not found."

