# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from allauth.account.signals import user_logged_in, user_signed_up
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.
class profile(models.Model):
    name = models.CharField(max_length=120, default="default text")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
    description = models.TextField(default="default text")

    def __unicode__(self):
        return self.name


class userStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)

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
        print 'created for %s'%(user.username)
    if user_stripe_account.stripe_id is None or user_stripe_account.stripe_id == '':
        new_stripe_id = stripe.Customer.create(email = user.email)
        user_stripe_account.stripe_id = new_stripe_id['id']
        user_stripe_account.save()

#this creates a profile when a user SIGNS UP
def profileCallback(sender, request, user, **kwargs):
    userProfile, is_created = profile.objects.get_or_create(user=user)
    if is_created:
        userProfile.name = user.username
        userProfile.save()

#when a user logs in this will connect ot my callback
user_logged_in.connect(stripeCallback)
user_signed_up.connect(profileCallback)





class Item(models.Model):
    name = models.CharField(max_length=234)
    brand = models.CharField(max_length=234)
    description = models.TextField(default="default text")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
