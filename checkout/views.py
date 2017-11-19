# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from collections import defaultdict
from decimal import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import stripe

from profiles.models import *



stripe.api_key = settings.STRIPE_SECRET_KEY
# easypost.api_key = settings.EASYPOST_TEST_KEY

@login_required
def payment_form(request):
    customer_id =  request.user.userstripe.stripe_id
    context = { "stripe_key": settings.STRIPE_PUBLIC_KEY }
    return render(request, "shoppingcart.html", context)

@login_required
def checkout(request):
    # customer_id = request.user.userstripe.stripe_id
    userId = request.user.id
    _the_Stripe = userStripe.objects.get(user__id = userId)
    customer_id = _the_Stripe.stripe_id

    if request.method == "POST":
         token = request.POST.get("stripeToken")


    try:
        customer = stripe.Customer.retrieve(customer_id)
        # customer.sources.create(source=token)

        userId = request.user.id
        #now we have to get the item instances in the shopping cart
        cart = shoppingCart.objects.get(user__id = userId)


        # the_order = Order.objects.create(user = request.user)
        # instance_ids = itemInstance.objects.filter(shopping_cart__id = cart.id).values_list('id', flat=True)
        # for x in instance_ids:
        #     da_instance = itemInstance.objects.get(id = x)
        #     da_instance.order = the_order
        #     da_instance.save()

        customers_items_id =  [item.instanceOfItem.id for item in itemInstance.objects.filter(shopping_cart__id = cart.id)]
        for x in customers_items_id:
            #query the item is x
            da_item = Item.objects.get(id = x)
            da_item.inventory -= 1
            da_item.sale_count +=1
            da_item.save()



        cart.amountSpent *= 100
        amountInt = int(cart.amountSpent)


        charge  = stripe.Charge.create(
            amount = amountInt,
            currency = "usd",
            customer = customer,
            description = "The product charged to the user"
        )
    except stripe.error.CardError as ce:
        return False, ce
    else:
        return render( request, "thanks.html")



        # The payment was successfully processed, the user's card was charged.
        # You can now redirect the user to another page or whatever you want






@login_required
def shop1(request):
    userId = request.user.id
    the_items = Item.objects.all()
    cart = shoppingCart.objects.get(user__id = userId)
    items_in_cart = itemInstance.objects.filter(shopping_cart__id = cart.id)

    for x in items_in_cart:
        x.quantity = int(x.quantity)
    stripe_total = cart.amountSpent * 100

    # #this is just to print
    # customers_items = itemInstance.objects.filter(shopping_cart__id = cart.id).values()



    context = {
    "items_in_cart": items_in_cart,
    "the_items": the_items,
    "total": cart.amountSpent,
     "stripe_key": settings.STRIPE_PUBLIC_KEY,
     "stripe_total": stripe_total
    }
    return render(request, "shop1.html", context)


@login_required
def update(request, id):
    instance = itemInstance.objects.get(id = id)
    _item = instance.instanceOfItem
    customers_cart = instance.shopping_cart

    #first subtract the price times the quantity from the amount sent
    _price = float(instance.instanceOfItem.price)
    _quantity = float(instance.quantity)
    solution = _price * _quantity
    _solution = float(solution)
    cart_total = float(customers_cart.amountSpent)
    customers_cart.amountSpent = cart_total - solution
    customers_cart.save()



    instance.quantity = request.POST['quantity']
    instance.save()

    #get the shopping cart of the item
    #update the amount spent in the shopping cart


    #now we add the new price times quantity for the amount spont
    _price = float(instance.instanceOfItem.price)
    _quantity = float(instance.quantity)
    solution = _price * _quantity
    _solution = float(solution)
    cart_total = float(customers_cart.amountSpent)

    customers_cart.amountSpent = cart_total + solution
    customers_cart.save()


    return redirect("/shop1")

@login_required
def remove(request, id):
    instance = itemInstance.objects.get(id = id)
    the_item = instance.instanceOfItem
    customers_cart = instance.shopping_cart

    _price = float(instance.instanceOfItem.price)
    _quantity = float(instance.quantity)
    solution = _price * _quantity
    _solution = float(solution)
    cart_total = float(customers_cart.amountSpent)
    customers_cart.amountSpent = cart_total - solution
    customers_cart.save()


    the_item.save()


    instance.delete()


    return redirect("/shop1")


@login_required
def addToCart(request, id):
    userId = request.user.id
    customers_cart = shoppingCart.objects.get(user__id = userId)
    customers_items = [item.instanceOfItem.name for item in itemInstance.objects.filter(shopping_cart__id = customers_cart.id)]

    the_item = Item.objects.get(id = id)
    the_items_once = []
   #with this flag we just gont create a new sale in the first place
    addItemFlag = "not yet added"
    for x in customers_items:
        if x == the_item.name:
            addItemFlag="already added"

    if addItemFlag == "already added":

        return redirect("/shop1")

    if addItemFlag == "not yet added":
        the_items_once.append(the_item)
       #then dont add the who queryset to the array

        itemInstance.quantity = request.POST['quantity']

        #these are the conversion
        _price = float(the_item.price)
        _quantity = float(itemInstance.quantity)
        solution = _price * _quantity
        _solution = float(solution)
        cart_total = float(customers_cart.amountSpent)
        the_item.price = Decimal(solution)



        #first we create the sale
        sale = itemInstance.objects.create(instanceOfItem = the_item, shopping_cart = customers_cart, quantity = request.POST['quantity'])
        #update the total spent
        customers_cart.amountSpent = cart_total + solution
        print customers_cart.amountSpent
        customers_cart.save()
        return redirect("/shop1")
