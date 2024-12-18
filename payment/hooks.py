from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings
import time
from .models import Order

@receiver(valid_ipn_received)
def paypal_payment_received(sender,**kwargs):
    # Add a ten second pause for paypal to send IPN data
    time.sleep(10)
    
    #Grab the info that paypal sends
    paypal_obj = sender
    # Grab the invoice
    my_Invoice = str(paypal_obj.invoice)
    
    
    # Match the Paypal Invioce to the order invoice
    # Look Up The Order
    my_Order = Order.objects.get(invoice=my_Invoice)
    
    # Record the Order was paid
    my_Order.paid = True
    # Save the Order
    my_Order.save()

    
    
    #print(paypal_obj)
    #print(f'Amount Paid:{paypal_obj.mc_gross}')
    













# from paypal.standard.models import ST_PP_COMPLETED
# from paypal.standard.ipn.signals import valid_ipn_received

# def show_me_the_money(sender, **kwargs):
#     ipn_obj = sender
#     if ipn_obj.payment_status == ST_PP_COMPLETED:
#         # WARNING !
#         # Check that the receiver email is the same we previously
#         # set on the `business` field. (The user could tamper with
#         # that fields on the payment form before it goes to PayPal)
#         if ipn_obj.receiver_email != "receiver_email@example.com":
#             # Not a valid payment
#             return

#         # ALSO: for the same reason, you need to check the amount
#         # received, `custom` etc. are all what you expect or what
#         # is allowed.

#         # Undertake some action depending upon `ipn_obj`.
#         if ipn_obj.custom == "premium_plan":
#             price = ...
#         else:
#             price = ...

#         if ipn_obj.mc_gross == price and ipn_obj.mc_currency == 'USD':
#             ...
#     else:
#         #...

# valid_ipn_received.connect(show_me_the_money)