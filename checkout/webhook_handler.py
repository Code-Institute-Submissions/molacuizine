from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from profiles.models import UserProfile, Town

from .models import Order, OrderLineItem
from products.models import Product

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """

        # Handle succesful payments with submssion errors
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info
        request = intent.metadata.request
        print(request)
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping

        # Clean data in the shipping details/Since null in model
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Request profile related to username in intent
        profile = None
        username = intent.metadata.username
        profile = UserProfile.objects.get(user__username=username)
        if save_info:
            profile.default_phone_number = shipping_details.phone
            profile.default_postcode = shipping_details.address.postal_code
            profile.default_town = shipping_details.address.city
            profile.default_street_address1 = shipping_details.address.line1
            profile.save()

        attempt = 1
        order = False
        while order is False and attempt <= 5:
            try:
                order = Order.objects.get(stripe_pid=pid)
                order = True
                break
            except Order.DoesNotExist:
                order = False
                attempt += 1
                time.sleep(1)
                print(attempt)
        if order is True:
            order = Order.objects.get(stripe_pid=pid)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    street_address=shipping_details.address.line1,
                    town=get_object_or_404(Town, name=shipping_details.address.city),
                    postcode=shipping_details.address.postal_code,
                    request=request,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
