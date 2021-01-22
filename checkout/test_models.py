from django.test import TestCase
from .models import Order, OrderLineItem
from django.shortcuts import get_object_or_404
from profiles.models import Town
from products.models import Product, Category


class TestModels(TestCase):

    def setUp(self):
        self.Town = Town.objects.create(
            name="vacoas", long_coord=-20.3171, lat_coord=57.5265)
        self.Category = Category.objects.create(name="sides")

    def test_Order_item_string_returns_name(self):
        order = Order.objects.create(
            full_name='zahur meerun',
            email='zahurmeerun@yahoo.com',
            phone_number='57075200',
            street_address='vacoas',
            town=get_object_or_404(
                        Town, name='vacoas'),
            postcode='222222',
            request='none')
        self.assertAlmostEqual(str(order), order.order_number)

    def test_OrderLineItem_string_returns_name(self):
        order = Order.objects.create(
            full_name='zahur meerun',
            email='zahurmeerun@yahoo.com',
            phone_number='57075200',
            street_address='vacoas',
            town=get_object_or_404(
                        Town, name='vacoas'),
            postcode='222222',
            request='none')
        product = Product.objects.create(
                name="Item", price=50, category_id=1, spice_index=True)
        orderlineitem = OrderLineItem.objects.create(
            order_id=order.id, product=product)
        self.assertAlmostEqual(str(orderlineitem), order.order_number)
