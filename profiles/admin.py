# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from allauth.account.signals import user_logged_in, user_signed_up
import stripe

# Register your models here.
from .models import profile, userStripe

class profileAdmin(admin.ModelAdmin):
    class Meta:
        model = profile

admin.site.register(profile, profileAdmin)

class userStripeAdmin(admin.ModelAdmin):
    class Meta:
        model = userStripe
admin.site.register(userStripe, userStripeAdmin)

# kwargs stands for keyword arguement
#now when a user logs in, this function will connect to my callback
