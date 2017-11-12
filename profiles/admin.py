# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from allauth.account.signals import user_logged_in, user_signed_up
import stripe

# Register your models here.
from .models import profile, userStripe, Item, shoppingCart, itemInstance, itemCategory

# this is essential the user since the
#true user is built into allauth
class profileAdmin(admin.ModelAdmin):
    class Meta:
        model = profile

admin.site.register(profile, profileAdmin)

class userStripeAdmin(admin.ModelAdmin):
    class Meta:
        model = userStripe
admin.site.register(userStripe, userStripeAdmin)



class ItemAdmin(admin.ModelAdmin):
    class Meta:
        model = Item
admin.site.register(Item, ItemAdmin)

class itemCategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = itemCategory
admin.site.register(itemCategory, itemCategoryAdmin)

class itemInstanceAdmin(admin.ModelAdmin):
    class Meta:
        model = itemInstance
admin.site.register(itemInstance, itemInstanceAdmin)


class shoppingCartAdmin(admin.ModelAdmin):
    class Meta:
        model = shoppingCart
admin.site.register(shoppingCart, shoppingCartAdmin)


# class PurchaseAdmin(admin.ModelAdmin):
#     class Meta:
#         model = Purchase
# admin.site.register(Purchase, PurchaseAdmin)

# kwargs stands for keyword arguement
#now when a user logs in, this function will connect to my callback
