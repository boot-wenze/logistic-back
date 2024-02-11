"""Channels Routing"""

# pylint: disable=no-member
# pylint: disable=arguments-differ
# pylint: disable=unused-import
# pylint: disable=missing-docstring
# pylint: disable=attribute-defined-outside-init
# pylint: disable=no-name-in-module

from django.urls import path

from . import consumers

ws_urlpatterns = [
    path(
        "ws/favorite/<str:user_id>/<str:product_id>/<str:b_id>",
        consumers.Favorite.as_asgi(),
    ),
    path(
        "ws/likedProduct/<str:user_id>",
        consumers.GetFavorites.as_asgi(),
    ),
    path(
        "ws/addRemoveCart/<str:user_id>",
        consumers.AddRemoveCart.as_asgi(),
    ),
    path(
        "ws/cartById/<str:user_id>/<str:product_id>",
        consumers.CartById.as_asgi(),
    ),
    path(
        "ws/getAllCart/<str:user_id>",
        consumers.GetAllCart.as_asgi(),
    ),
]
