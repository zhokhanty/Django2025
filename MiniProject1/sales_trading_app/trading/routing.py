from django.urls import path
from .consumers import OrderBookConsumer, PriceChartConsumer

websocket_urlpatterns = [
    path('ws/trading/orders/', OrderBookConsumer.as_asgi()),
    path('ws/trading/prices/', PriceChartConsumer.as_asgi()),
]