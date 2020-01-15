from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from servicecatalog.models import ServiceProduct
from .models import Quote, QuoteItem
import stripe
from django.conf import settings
from orders.models import Order, OrderItem


def _quote_id(request):
    quote = request.session.session_key
    if not quote:
        quote = request.session.create()
    return quote

def add_to_cart(request, service_id):
    service = ServiceProduct.objects.get(id=service_id)
    try:
        quote = Quote.objects.get(quote_id=_quote_id(request))
    except Quote.DoesNotExist:
        quote = Quote.objects.create(
            quote_id=_quote_id(request)
        )
        quote.save()
    try:
        quote_item = QuoteItem.objects.get(service=service, quote=quote)
        if quote_item.quantity < quote_item.service.stock:
            quote_item.quantity += 1
        quote_item.save()
    except QuoteItem.DoesNotExist:
        quote_item = QuoteItem.objects.create(
            service = service,
            quote = quote,
            quantity = 1
        )
        quote_item.save()
    return redirect('cart:cart_detail')

def cart_detail(request, order_total=0, counter=0, quote_items=0):
    try:
        quote = Quote.objects.get(quote_id=_quote_id(request))
        quote_items = QuoteItem.objects.filter(quote=quote, active=True)
        for quote_item in quote_items:
            order_total += (quote_item.service.service_cost * quote_item.quantity)
            counter += quote_item.quantity
    except ObjectDoesNotExist:
        pass
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(order_total * 100)
    description = 'Daily Stuff - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        try:
            stripeToken = request.POST['stripeToken']
            stripeEmail = request.POST['stripeEmail']
            stripeBillingName = request.POST['stripeBillingName']
            stripeBillingAddressLine1 = request.POST['stripeBillingAddressLine1']
            stripeBillingAddressCity = request.POST['stripeBillingAddressCity']
            stripeBillingAddressZip = request.POST['stripeBillingAddressZip']
            stripeBillingAddressCountryCode = request.POST['stripeBillingAddressCountryCode']
            stripeShippingName = request.POST['stripeShippingName']
            stripeShippingAddressLine1 = request.POST['stripeShippingAddressLine1']
            stripeShippingAddressCity = request.POST['stripeShippingAddressCity']
            stripeShippingAddressZip = request.POST['stripeShippingAddressZip']
            stripeShippingAddressCountryCode = request.POST['stripeShippingAddressCountryCode']
            customer = stripe.Customer.create(
                email = stripeEmail,
                source = stripeToken
            )
            charge = stripe.Charge.create(
                amount = stripe_total,
                currency = 'gbp',
                description = description,
                customer = customer.id
            )
            # TODO: saving order in admin code here
            try:
                LoggedInCustomer = None
                if request.user.is_authenticated:
                    LoggedInCustomer = request.user.id
                orderDetails = Order.objects.create(
                    token=stripeToken,
                    total=stripe_total,
                    email_id=stripeEmail,
                    billingName=stripeBillingName,
                    billingAddress1=stripeBillingAddressLine1,
                    billingCity=stripeBillingAddressCity,
                    billingPostcode=stripeBillingAddressZip,
                    billingCountry=stripeBillingAddressCountryCode,
                    shippingName=stripeShippingName,
                    shippingAddress1=stripeShippingAddressLine1,
                    shippingCity=stripeShippingAddressCity,
                    shippingPostcode=stripeShippingAddressZip,
                    shippingCountry=stripeShippingAddressCountryCode,
                    customerId=LoggedInCustomer
                )
                orderDetails.save()
                for quote_item in quote_items:
                    order_item = OrderItem.objects.create(
                        product=quote_item.service.product_name,
                        quantity=quote_item.quantity,
                        price=quote_item.service.service_cost,
                        order=orderDetails
                    )
                    order_item.save()
                    '''Reduce the stock when the order is placed or saved'''
                    serviceProduct = ServiceProduct.objects.get(id=quote_item.service.id)
                    serviceProduct.stock = int(quote_item.service.stock - quote_item.quantity)
                    serviceProduct.popularity += 1
                    serviceProduct.save()
                    '''Remove the item from the shopping cart'''
                    quote_item.delete()
                return redirect('orders:thankspage', orderDetails.id)
            except ObjectDoesNotExist:
                pass
        except stripe.error.CardError as e:
            return False, e
    return render(request, 'cart_detail.html', dict(
        quote_items=quote_items,
        total=order_total,
        counter=counter,
        data_key=data_key,
        stripe_total=stripe_total,
        description=description
    ))