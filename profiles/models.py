# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from allauth.account.signals import user_logged_in, user_signed_up
import stripe



stripe.api_key = settings.STRIPE_SECRET_KEY

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class itemCategory(models.Model):
    name = models.CharField(max_length=234)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=234)
    brand = models.CharField(max_length=234)
    description = models.TextField(default="default text")
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field", height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    inventory = models.FloatField(default=0)
    sale_count = models.FloatField(default=0)
    weight = models.IntegerField(default=0)
    category = models.ForeignKey(itemCategory)


    def __unicode__(self):
        return self.name

class shoppingCart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL )
    name = models.CharField(max_length=120, default="default text")
    amountSpent = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)

class itemInstance(models.Model):
    shopping_cart = models.ForeignKey(shoppingCart)
    instanceOfItem = models.ForeignKey(Item)
    order = models.ForeignKey(Order, null=True, blank=True)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



# Create your models here.
class profile(models.Model):
    name = models.CharField(max_length=120, default="default text")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
    description = models.TextField(default="default text")

    def __unicode__(self):
        return self.name


class userStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    stripe_id = models.CharField(max_length=200)

    def __unicode__(self):
        if self.stripe_id:
            return str(self.stripe_id)
        else:
            return self.user.username




# this crates a userStripe whne a user SIGNS IN
#stripeCallBack checks if a user has a user stripe
# if there is no stripe it will create one
def stripeCallback(sender, request, user, **kwargs):
    user_stripe_account, created = userStripe.objects.get_or_create(user=user)
    if created:
        print 'created for a%s'%(user.username)
    if user_stripe_account.stripe_id is None or user_stripe_account.stripe_id == '':
        #FIND OUT WHAT THIS IS DOING
        new_stripe_id = stripe.Customer.create(email = user.email)
        user_stripe_account.stripe_id = new_stripe_id['id']
        user_stripe_account.save()

#this creates a profile when a user SIGNS UP
def profileCallback(sender, request, user, **kwargs):
    userProfile, is_created = profile.objects.get_or_create(user=user)
    if is_created:
        userProfile.name = user.username
        userProfile.save()

#this creates a shoppingcart when a user signs up
def shoppingCartCallback(sender, request, user, **kwargs):
    #if it doesn't get it it will automatically connect the user
    userShoppingCart, is_created = shoppingCart.objects.get_or_create(user = user)
    if is_created:
        userShoppingCart.name = user.username
        userShoppingCart.save()




#when a user logs in this will connect ot my callback
user_signed_up.connect(stripeCallback)
user_signed_up.connect(profileCallback)
user_signed_up.connect(shoppingCartCallback)








#one purchase can have many many items
#one purchase can have one userStripe
