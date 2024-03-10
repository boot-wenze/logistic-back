"""Celery task module"""

# pylint: disable=no-member
# pylint: disable=unused-import
# import time
import json
from typing import TypeVar, Optional, Any
from django.core.cache import cache
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_celery_results.models import TaskResult

from api.models import Cart, Command, Favorite


T = TypeVar("T", str, dict, list, int, Any)


channel_layer = get_channel_layer()


@shared_task
def add_remove_favorite(b_id: str, product_id: str, user_id: str):
    """

    Args:
        - b_id : Bness ID
        - product_id : Product ID
        - user_id : User ID
    Return: message status
    """
    data = Favorite.add_remove_favorite(b_id, user_id, product_id)

    async_to_sync(channel_layer.group_send)(
        f"favorite_{user_id}_{product_id}",
        {"type": "add.delete.favorite", "data": data},
    )


@shared_task
def get_favorites(user_id: str):
    """

    Args:
        - user_id : User ID
    Return: items
    """
    data = Favorite.get_favorites(user_id)

    async_to_sync(channel_layer.group_send)(
        f"favorites_{user_id}",
        {"type": "get.favorite", "data": data},
    )


@shared_task
def get_cart(data: dict, user_id: str):
    """

    Args:
        - data : data dict
    Return: items
    """
    data = Cart.add_remove_cart(data)

    async_to_sync(channel_layer.group_send)(
        f"cart_{user_id}",
        {"type": "cart", "data": data},
    )


@shared_task
def get_a_product_cart(product_id: str, user_id: str):
    """

    Args:
        - data : data dict
    Return: items
    """
    data = Cart.get_cart_products(user_id, product_id)

    async_to_sync(channel_layer.group_send)(
        f"cart_by_id_{user_id}",
        {"type": "cart.by.id", "data": data},
    )


@shared_task
def get_all_cart(user_id: str):
    """

    Args:
        - data : data dict
    Return: items
    """
    data = Cart.get_all_from_cart(user_id)

    async_to_sync(channel_layer.group_send)(
        f"all_cart_{user_id}",
        {"type": "all.cart", "data": data},
    )


@shared_task
def add_order(order, suivis, products):
    """

    Args:
        - order : order dict
        - suivis : suivis dict
        - products : products list
    Return: None
    """
    Command.register_order(body=order, suivis=suivis, products=products)
