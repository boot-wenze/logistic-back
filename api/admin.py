"""ADMIN INTERFACE"""

from django.contrib import admin

from .models import (
    Agent,
    Product,
    Cart,
    Command,
    RemunerationHebdomadaire,
    RemunerationJournalier,
    RemunerationMensuel,
    Suivis,
    Deliver,
    Favorite,
)

# Register your models here.

admin.site.register(Agent)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Command)
admin.site.register(RemunerationHebdomadaire)
admin.site.register(RemunerationJournalier)
admin.site.register(RemunerationMensuel)
admin.site.register(Suivis)
admin.site.register(Deliver)
admin.site.register(Favorite)
