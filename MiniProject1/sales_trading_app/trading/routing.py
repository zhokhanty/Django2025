from django.urls import path
from .consumers import OrderBookConsumer

websocket_urlpatterns = [
    path('ws/trading/orders/', OrderBookConsumer.as_asgi()),
]
