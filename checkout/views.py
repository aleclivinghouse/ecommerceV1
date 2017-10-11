# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import stripe
from profiles.models import *


stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.
#Step 2 addd this to the checkout views
#NEXT go to checkout.html
@login_required
def payment_form(request):
    customer_id =  request.user.userstripe.stripe_id
    context = { "stripe_key": settings.STRIPE_PUBLIC_KEY }
    return render(request, "shoppingcart.html", context)

@login_required
def checkout(request):
    customer_id = request.user.userstripe.stripe_id
    new_item = Item(
        name = "Civic",
        brand = "Honda",
        description = "fjklsadfksja",
        price = 12.99
    )
    if request.method == "POST":
        token  = request.POST.get("stripeToken")
    try:
        customer = stripe.Customer.retrieve(customer_id)
        customer.sources.create(source=token)
        charge  = stripe.Charge.create(
            amount    = 2000,
            currency = "usd",
            customer = customer,
            description = "The product charged to the user"
        )
        new_item.charge_id   = charge.id
    except stripe.error.CardError as ce:
        return False, ce
    else:
        new_item.save()
        # WE ALSO HAVE TO REMOVE ALL ITEMS FROM THE SHOPPING CART
        return render( request, "thanks.html")
        # The payment was successfully processed, the user's card was charged.
        # You can now redirect the user to another page or whatever you want
