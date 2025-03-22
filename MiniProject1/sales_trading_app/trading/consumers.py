import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Order
from django.core.serializers.json import DjangoJSONEncoder
from random import uniform
import asyncio

class OrderBookConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("orders", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("orders", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "fetch_orders":
            orders = list(Order.objects.filter(status="PENDING").values())
            await self.send(json.dumps({"orders": orders}, cls=DjangoJSONEncoder))

    async def send_order_update(self, event):
        order_data = event["order"]
        await self.send(text_data=json.dumps(order_data, cls=DjangoJSONEncoder))

class PriceChartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("price_updates", self.channel_name)
        await self.accept()
        self.running = True

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("price_updates", self.channel_name)
        self.running = False

    async def send_price_update(self, event):
        await self.send(text_data=json.dumps(event["price_data"]))

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "start_stream":
            while self.running:
                price_data = {
                    "asset": "BTC/USD",
                    "price": round(uniform(50000, 55000), 2)
                }
                await self.channel_layer.group_send(
                    "price_updates",
                    {"type": "send_price_update", "price_data": price_data}
                )
                await asyncio.sleep(2)