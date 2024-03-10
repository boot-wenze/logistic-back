"VIEWS"
# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring
# pylint: disable=unused-import
# pylint: disable=no-member
# pylint: disable=unused-argument
# from django.shortcuts import render
from datetime import datetime
import time

from django.http import HttpResponse


from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from api.models import Command, Product, Suivis

from api.tasks import add_order

# Create your views here.


@api_view(["POST", "GET", "DELETE", "PUT"])
@permission_classes(())
def home(request):
    """Home"""
    if request.method == "GET":
        return HttpResponse("HELLO WORLD")


@api_view(["POST", "GET", "DELETE", "PUT"])
@permission_classes(())
def get_all_orders(request, client_id: str = None):

    if request.method == "GET":

        my_products = []

        my_orders = Suivis.get_all_command(client_id)

        for order in my_orders:
            _ = Product.filter_order(order["command_id"])
            my_products.extend(_)

        return Response(
            {"succeed": True, "data": my_orders, "products": my_products},
            status=status.HTTP_200_OK,
        )


@api_view(["POST", "GET", "DELETE", "PUT"])
@permission_classes(())
def order(request):
    """Order view"""
    if request.method == "POST":

        body = request.data

        cmd: dict = {
            "client_id": body[0]["client_id"],
            "client_fullname": body[0]["client_fullname"],
            "client_phone": body[0]["client_phone"],
            "client_subscription_type": body[0]["client_subscription_type"],
            "email": body[0]["email"],
            "cout_total": body[0]["cout_total"],
            "currency": body[0]["currency"],
            "frais_livraison": body[0]["frais_livraison"],
            "livraison_frais_currency": body[0]["currency"],
            "address_livraison": body[0]["address_livraison"],
        }

        suivis: dict = {
            "client_id": body[0]["client_id"],
        }

        products: list = []

        for element in body:

            detail: str = ""

            for i in element["detail"]:
                detail += i + "\n"

            products.append(
                {
                    "b_id": element["b_id"],
                    "branch_id": element["branch_id"],
                    "photo": element["photo"],
                    "photo_id": element["photo_id"],
                    "product_id": element["product_id"],
                    "nom_produit": element["nom_produit"],
                    "client_subscription_type": element["client_subscription_type"],
                    "number_articles": element["number_articles"],
                    "price": element["price"],
                    "currency": element["currency"],
                    "description": element["description"]
                    + "\n\n"
                    + "detail : \n"
                    + detail,
                    "has_discount": element["has_discount"],
                    "discount_percentage": element["discount_percentage"],
                    "cout_total": element["cout_total"],
                }
            )

        add_order.delay(cmd, suivis, products)

        return Response(
            {"succeed": True, "message": "commande enregistré."},
            status=status.HTTP_201_CREATED,
        )
