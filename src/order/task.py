"""
Celery Task For Remove Cart was not user long time
"""
import logging
from .celery import app
from .models import Cart


@app.task
def remove_cart(cart_id):
    ''' remove cart '''
    try:
        cart = Cart.objects.get(id=cart_id)
        if not cart.user:
            cart.delete()

    except Cart.DoesNotExist:
        logging.warning("Cart allready deleted %d" %(cart_id,))
