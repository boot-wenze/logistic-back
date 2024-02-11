"""Consumer"""

# pylint: disable=arguments-differ
# pylint: disable=unused-import
# pylint: disable=unused-argument
# pylint: disable=import-error
# pylint: disable=missing-docstring
# pylint: disable=attribute-defined-outside-init
# pylint: disable=no-name-in-module
import json
from typing import TypeVar, Any, Optional
from collections import defaultdict, deque

from django.http import HttpRequest

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from api.tasks import (
    add_remove_favorite,
    get_a_product_cart,
    get_all_cart,
    get_cart,
    get_favorites,
)


class Favorite(WebsocketConsumer):
    """Item consumer websocket"""

    def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.product_id = self.scope["url_route"]["kwargs"]["product_id"]
        self.b_id = self.scope["url_route"]["kwargs"]["b_id"]
        self.branch_group = f"favorite_{self.user_id}_{self.product_id}"

        # Join branch group
        async_to_sync(self.channel_layer.group_add)(
            self.branch_group, self.channel_name
        )
        self.accept()

        add_remove_favorite.delay(self.b_id, self.product_id, self.user_id)

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.branch_group, self.channel_name
        )

    def add_delete_favorite(self, event):
        message = event["data"]
        # Send message to WebSocket

        self.send(text_data=json.dumps({"data": message}))


class GetFavorites(WebsocketConsumer):
    """Item consumer websocket"""

    def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.branch_group = f"favorites_{self.user_id}"

        # Join branch group
        async_to_sync(self.channel_layer.group_add)(
            self.branch_group, self.channel_name
        )
        self.accept()

        get_favorites.delay(self.user_id)

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.branch_group, self.channel_name
        )

    def get_favorite(self, event):
        message = event["data"]
        # Send message to WebSocket

        self.send(text_data=json.dumps({"data": message}))


class AddRemoveCart(WebsocketConsumer):
    """Item consumer websocket"""

    def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.branch_group = f"cart_{self.user_id}"

        # Join branch group
        async_to_sync(self.channel_layer.group_add)(
            self.branch_group, self.channel_name
        )
        self.accept()

    def receive(self, text_data=None):

        data = json.loads(text_data)

        get_cart.delay(data, self.user_id)

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.branch_group, self.channel_name
        )

    def cart(self, event):
        message = event["data"]
        # Send message to WebSocket

        self.send(text_data=json.dumps({"data": message}))


class CartById(WebsocketConsumer):
    """Item consumer websocket"""

    def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.product_id = self.scope["url_route"]["kwargs"]["product_id"]
        self.branch_group = f"cart_by_id_{self.user_id}"

        # Join branch group
        async_to_sync(self.channel_layer.group_add)(
            self.branch_group, self.channel_name
        )
        self.accept()

        get_a_product_cart.delay(self.product_id, self.user_id)

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.branch_group, self.channel_name
        )

    def cart_by_id(self, event):
        message = event["data"]
        # Send message to WebSocket

        self.send(text_data=json.dumps({"data": message}))


class GetAllCart(WebsocketConsumer):
    """Item consumer websocket"""

    def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.branch_group = f"all_cart_{self.user_id}"

        # Join branch group
        async_to_sync(self.channel_layer.group_add)(
            self.branch_group, self.channel_name
        )
        self.accept()

        get_all_cart.delay(self.user_id)

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.branch_group, self.channel_name
        )

    def all_cart(self, event):
        message = event["data"]
        # Send message to WebSocket

        self.send(text_data=json.dumps({"data": message}))
