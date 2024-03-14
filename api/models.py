"""
    Database model:
        - Agent
        - Suivis
        - Favorite
        - Cart
        - Product
        - Deliver
        - Commande
        - Remuneration
"""

# pylint: disable=no-member
# pylint: disable=unused-import
# pylint: disable=unused-argument
# pylint: disable=not-callable
# pylint: disable=arguments-renamed
# pylint: disable=anomalous-backslash-in-string
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from datetime import datetime, timedelta, date
import random
import time
import re
from typing import TypeVar, Optional
import secrets
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser

# from django.contrib.postgres.search import SearchVector
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from api.utils.utils import bness_host, hash_password, host

# Create your models here.
T = TypeVar("T", str, int, list, dict)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Args:
     - sender : table
     - instance : data body
     - created : check if instance is done

    """
    if created:
        Token.objects.create(user=instance)


class Agent(AbstractUser):

    class Diplome(models.TextChoices):

        TENAFEP = "TENAFEP", "TENAFEP"
        DIPLOME_ETAT = "DIPLOME_ETAT", "DIPLOME_ETAT"
        GRADUAT = "GRADUAT", "GRADUAT"
        LICENCE = "LICENCE", "LICENCE"
        MASTER = "MASTER", "MASTER"
        PHD = "PHD", "PHD"

    class Currency(models.TextChoices):

        USD = "USD", "USD"
        FC = "FC", "FC"

    class Poste(models.TextChoices):

        MANAGER = "MANAGER", "MANAGER"
        SERVICE_CLIENT = "SERVICE_CLIENT", "SERVICE_CLIENT"
        LIVREUR = "LIVREUR", "LIVREUR"

    class Payment(models.TextChoices):

        JOURNALIER = "JOURNALIER", "JOURNALIER"
        HEBDOMADAIRE = "HEBDOMADAIRE", "HEBDOMADAIRE"
        MENSUEL = "MENSUEL", "MENSUEL"

    class Gender(models.TextChoices):

        M = "M", "M"
        F = "F", "F"
        N = "N", "N"

    agent_id = models.CharField(max_length=50, unique=True, blank=False, null=False)
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        null=False,
        blank=False,
    )
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=False, blank=False)
    username = models.CharField(max_length=255, unique=True, null=False, blank=False)
    email = models.CharField(max_length=70, null=True, blank=True)
    password = models.CharField(max_length=500, blank=True, null=True)
    has_child = models.BooleanField(default=False)
    is_married = models.BooleanField(default=False)
    child_number = models.IntegerField(default=0)
    last_diplome = models.CharField(
        max_length=50, choices=Diplome.choices, null=False, blank=False
    )
    poste = models.CharField(
        max_length=50, choices=Poste.choices, null=False, blank=False
    )
    address = models.JSONField(default=dict)
    salary = models.FloatField(default=0)

    currency = models.CharField(
        max_length=5,
        choices=Currency.choices,
        default=Currency.FC,
        null=False,
        blank=False,
    )
    payment = models.CharField(
        max_length=50,
        choices=Payment.choices,
        default=Payment.MENSUEL,
        null=False,
        blank=False,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "password"]


class RemunerationJournalier(models.Model):

    class Currency(models.TextChoices):
        USD = "USD", "USD"
        FC = "FC", "FC"

    agent_id = models.CharField(max_length=50, unique=True, blank=False, null=False)
    fullname = models.CharField(max_length=255, null=False, blank=False)
    montant = models.FloatField(default=0)
    currency = models.CharField(
        max_length=5,
        choices=Currency.choices,
        default=Currency.FC,
        null=False,
        blank=False,
    )
    is_paid = models.BooleanField(default=True)
    date_paid = models.DateTimeField(auto_now_add=True)
    motif = models.TextField(null=False, blank=False)


class RemunerationHebdomadaire(models.Model):

    class Currency(models.TextChoices):
        USD = "USD", "USD"
        FC = "FC", "FC"

    agent_id = models.CharField(max_length=50, unique=True, blank=False, null=False)
    fullname = models.CharField(max_length=255, null=False, blank=False)
    montant = models.FloatField(default=0)
    currency = models.CharField(
        max_length=5,
        choices=Currency.choices,
        default=Currency.FC,
        null=False,
        blank=False,
    )
    is_paid = models.BooleanField(default=True)
    date_paid = models.DateTimeField(auto_now_add=True)
    motif = models.TextField(null=False, blank=False)


class RemunerationMensuel(models.Model):

    class Currency(models.TextChoices):
        USD = "USD", "USD"
        FC = "FC", "FC"

    agent_id = models.CharField(max_length=50, unique=True, blank=False, null=False)
    fullname = models.CharField(max_length=255, null=False, blank=False)
    montant = models.FloatField(default=0)
    currency = models.CharField(
        max_length=5,
        choices=Currency.choices,
        default=Currency.FC,
        null=False,
        blank=False,
    )
    is_paid = models.BooleanField(default=False)
    for_month = models.DateField(auto_now_add=True)
    date_paid = models.DateTimeField(auto_now_add=True)
    motif = models.TextField(null=False, blank=False)


class Command(models.Model):

    # class Type(models.TextChoices):
    #     SUPERMARCHE = "SUPERMARCHE"
    #     WENZE = "WENZE"
    #     BOUTIQUE = "BOUTIQUE"
    #     RESTAURANT = "RESTAURANT"

    class Currency(models.TextChoices):
        USD = "USD", "USD"
        FC = "FC", "FC"

    command_id = models.CharField(max_length=200, unique=True, blank=False, null=False)
    client_id = models.CharField(max_length=50, blank=True, null=True)
    client_fullname = models.CharField(max_length=255, null=False, blank=False)
    client_phone = models.CharField(max_length=20, null=True, blank=True)
    client_subscription_type = models.CharField(max_length=50, blank=False, null=False)
    email = models.CharField(max_length=50, blank=True, null=True)
    # product_bought_category = models.CharField(
    #     max_length=50, choices=Type.choices, blank=False, null=False
    # )
    command_date = models.DateTimeField(auto_now_add=True)
    cout_total = models.FloatField()
    currency = models.CharField(
        max_length=5,
        choices=Currency.choices,
        null=False,
        blank=False,
    )
    frais_livraison = models.FloatField()

    livraison_frais_currency = models.CharField(
        max_length=5,
        choices=Currency.choices,
        null=False,
        blank=False,
    )
    date_prevu_livraison = models.DateTimeField(null=True, blank=True)
    address_livraison = models.JSONField(default=dict)
    code_secret = models.CharField(max_length=7, null=False, blank=False)
    is_delivered = models.BooleanField(default=False)

    @classmethod
    def get_all_command(cls, user_id: str):

        orders = list(cls.objects.filter(client_id=user_id))

        return orders

    @classmethod
    def get_order_id(cls, order: str = None):
        try:
            return cls.objects.get(command_id=order)
        except cls.DoesNotExist:
            return None

    @classmethod
    def generate_order_id(cls):
        order_id = secrets.token_hex(8)

        is_id_exist = cls.get_order_id(order_id)

        if is_id_exist is None:
            return order_id
        else:
            cls.generate_order_id()

    @classmethod
    def register_order(cls, body, suivis, products):

        my_order_id = cls.generate_order_id()
        body["command_id"] = my_order_id
        suivis["command_id"] = my_order_id

        for product in products:
            product["command_id"] = my_order_id

        body["code_secret"] = random.randint(1111111, 9999999)

        Product.add_order_product(products)

        Suivis.add_suivis(suivis)

        cls.objects.create(**body)

        return {"succeed": True}


class Suivis(models.Model):

    client_id = models.CharField(max_length=50, blank=True, null=True)
    command_id = models.CharField(max_length=200, unique=True, blank=False, null=False)
    status = models.IntegerField(default=0)

    @classmethod
    def get_all_command(cls, user_id: str):

        orders = list(cls.objects.values().filter(client_id=user_id).order_by("-id"))

        return orders

    @classmethod
    def add_suivis(cls, body):
        cls.objects.create(**body)

    @classmethod
    def update_suivis(cls, order_id, status):
        cls.objects.filter(command_id=order_id).update(status=status)


class Favorite(models.Model):

    # class Type(models.TextChoices):
    #     SUPERMARCHE = "SUPERMARCHE"
    #     WENZE = "WENZE"
    #     BOUTIQUE = "BOUTIQUE"
    #     RESTAURANT = "RESTAURANT"

    b_id = models.CharField(max_length=150, blank=True, null=True)
    client_id = models.CharField(max_length=50, blank=True, null=True)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    # product_favorite_category = models.CharField(
    #     max_length=50, choices=Type.choices, blank=False, null=False
    # )

    @classmethod
    def get_favorites(cls, client_id: str):

        results = list(cls.objects.values("product_id").filter(client_id=client_id))

        data = [i["product_id"] for i in results]

        return data

    @classmethod
    def add_remove_favorite(cls, b_id: str, client_id: str, product_id: str):

        try:
            product = cls.objects.get(
                b_id=b_id, client_id=client_id, product_id=product_id
            )

            product.delete()

            return {"message": "Deleted"}
        except cls.DoesNotExist:
            cls.objects.create(b_id=b_id, client_id=client_id, product_id=product_id)
            return {"message": "Added"}


class Cart(models.Model):

    # class Type(models.TextChoices):
    #     SUPERMARCHE = "SUPERMARCHE"
    #     WENZE = "WENZE"
    #     BOUTIQUE = "BOUTIQUE"
    #     RESTAURANT = "RESTAURANT"

    b_id = models.CharField(max_length=150, blank=True, null=True)
    product_id = models.CharField(max_length=200, blank=True, null=True)
    branch_id = models.CharField(max_length=200, blank=True, null=True)
    photo_id = models.CharField(max_length=200, blank=True, null=True)
    client_id = models.CharField(max_length=200, blank=True, null=True)
    number = models.IntegerField(blank=False, null=False, default=1)
    detail = ArrayField(models.CharField(), blank=True, null=True)

    # product_cart_category = models.CharField(
    #     max_length=50, choices=Type.choices, blank=False, null=False
    # )
    @classmethod
    def get_all_from_cart(cls, client_id: str):

        cart = list(
            cls.objects.values("product_id", "photo_id", "number", "detail").filter(
                client_id=client_id
            )
        )

        return cart

    @classmethod
    def get_cart_products(cls, client_id: str, product_id: str):

        carts = list(
            cls.objects.values("product_id", "photo_id", "number", "detail").filter(
                client_id=client_id, product_id=product_id
            )
        )

        return carts

    @classmethod
    def remove_cart(cls, product_id: str, photo_id: str):
        cls.objects.get(product_id=product_id, photo_id=photo_id).delete()

    @classmethod
    def add_remove_cart(cls, data: dict):

        panier = cls.objects.filter(
            b_id=data["b_id"],
            product_id=data["product_id"],
            photo_id=data["photo_id"],
            branch_id=data["branch_id"],
            client_id=data["client_id"],
        )

        if panier.exists():

            panier.update(number=data.get("number", 0))

            cart = cls.objects.get(
                b_id=data["b_id"],
                product_id=data["product_id"],
                photo_id=data["photo_id"],
                branch_id=data["branch_id"],
                client_id=data["client_id"],
            )
            if cart.number < 1:

                cart.delete()

                return {"message": "panier supprimé"}
            else:
                return {"message": "Panier mis à jour"}
        else:
            cls.objects.create(**data)
            return {"message": "Panier créer"}


class Deliver(models.Model):

    command_id = models.CharField(max_length=200, unique=True, blank=False, null=False)
    agent_id = models.CharField(max_length=50, blank=True, null=True)
    agent_fullname = models.CharField(max_length=255, null=False, blank=False)
    date_livraison = models.DateField()
    is_delivered = models.BooleanField(default=False)


class Product(models.Model):

    class Currency(models.TextChoices):
        USD = "USD", "USD"
        FC = "FC", "FC"

    command_id = models.CharField(max_length=200, blank=False, null=False)
    b_id = models.CharField(max_length=150, blank=True, null=True)
    branch_id = models.CharField(max_length=150, blank=True, null=True)
    photo = models.CharField(max_length=150, blank=True, null=True)
    photo_id = models.CharField(max_length=500, blank=True, null=True)
    product_id = models.CharField(max_length=250, blank=True, null=True)
    nom_produit = models.CharField(max_length=200, blank=False, null=False)
    client_subscription_type = models.CharField(max_length=50, blank=False, null=False)
    number_articles = models.IntegerField()
    price = models.FloatField()
    currency = models.CharField(
        max_length=5,
        choices=Currency.choices,
        null=False,
        blank=False,
    )
    description = models.TextField()
    command_date = models.DateTimeField(auto_now_add=True)
    date_prevu_livraison = models.DateTimeField(blank=True, null=True)
    has_discount = models.BooleanField(default=False)
    discount_percentage = models.IntegerField(default=0)
    cout_total = models.FloatField()
    validated_by_user = models.CharField(max_length=150, blank=True, null=True)
    status = models.IntegerField(default=0)
    orderType = models.CharField(max_length=50, blank=True, null=True, default="Normal")

    @classmethod
    def get_product_by_bness_id(cls, bness_id: str, branch_id: str):

        orders = (
            cls.objects.values()
            .filter(b_id=bness_id, branch_id=branch_id)
            .order_by("-id")
        )

        for order in orders:
            if order["status"] < 0:
                order["status"] = "Annuler"
            elif order["status"] == 0:
                order["status"] = "En attente"
            else:
                order["status"] = "Complet"
            order["command_date"] = str(order["command_date"])
            order["date_prevu_livraison"] = str(order["date_prevu_livraison"])
            order["photo"] = str(order["photo"]).split("/api/media/")[1]
            order["photo"] = bness_host() + order["photo"]

        return list(orders)

    @classmethod
    def filter_order(cls, command_id: str):
        orders = list(cls.objects.values().filter(command_id=command_id))
        return orders

    @classmethod
    def add_order_product(cls, data):

        datas = [Product(**element) for element in data]

        cls.objects.bulk_create(datas)

        for product in data:
            Cart.remove_cart(product["product_id"], product["photo_id"])

    @classmethod
    def finalize_order_product(cls, by_user: str, order_id: str):
        cls.objects.filter(command_id=order_id).update(validated_by_user=by_user)

    @classmethod
    def update_status(cls, data, status):
        cls.objects.filter(**data).update(status=status)

        time.sleep(1)

        get_all = cls.objects.filter(command_id=data["command_id"])

        divider = get_all.count()

        total = 0

        for i in get_all:
            total += i.status

        if (total / divider) == 1:
            Suivis.update_suivis(data["command_id"], 1)
        else:
            Suivis.update_suivis(data["command_id"], 0)

        return {"succeed": True}
