import time
import random
import logging
from app import app

logger = logging.getLogger(__name__)

# Global retry config
RETRY_KWARGS = {
    'autoretry_for': (Exception,),
    'retry_kwargs': {'max_retries': 3, 'countdown': 5},
    'acks_late': True
}


@app.task(name='order.charge_payment', **RETRY_KWARGS)
def charge_payment(order_id):
    try:
        print(f"[{order_id}] Charging payment...")
        time.sleep(random.uniform(0.5, 2))
        if random.random() < 0.1:
            raise Exception("Payment gateway failed.")
        print(f"[{order_id}] Payment charged.")
        return f"Payment charged for {order_id}"
    except Exception as e:
        logger.exception(f"[{order_id}] Payment error: {str(e)}")
        raise


@app.task(name='order.reserve_inventory', **RETRY_KWARGS)
def reserve_inventory(order_id):
    try:
        print(f"[{order_id}] Reserving inventory...")
        time.sleep(random.uniform(0.5, 2))
        if random.random() < 0.1:
            raise Exception("Inventory service timeout.")
        print(f"[{order_id}] Inventory reserved.")
        return f"Inventory reserved for {order_id}"
    except Exception as e:
        logger.exception(f"[{order_id}] Inventory error: {str(e)}")
        raise


@app.task(name='order.schedule_delivery', **RETRY_KWARGS)
def schedule_delivery(order_id):
    try:
        print(f"[{order_id}] Scheduling delivery...")
        time.sleep(random.uniform(0.5, 2))
        if random.random() < 0.1:
            raise Exception("Delivery scheduling failed.")
        print(f"[{order_id}] Delivery scheduled.")
        return f"Delivery scheduled for {order_id}"
    except Exception as e:
        logger.exception(f"[{order_id}] Delivery error: {str(e)}")
        raise


@app.task(name='order.send_confirmation_email', **RETRY_KWARGS)
def send_confirmation_email(order_id):
    try:
        print(f"[{order_id}] Sending confirmation email...")
        time.sleep(random.uniform(0.5, 2))
        if random.random() < 0.1:
            raise Exception("SMTP error.")
        print(f"[{order_id}] Email sent.")
        return f"Email sent for {order_id}"
    except Exception as e:
        logger.exception(f"[{order_id}] Email error: {str(e)}")
        raise


@app.task(name='order.log_fulfillment_summary')
def log_fulfillment_summary(results):
    print("=== Order Fulfillment Summary ===")
    for r in results:
        print(f"- {r}")
    return f"Summary logged for {len(results)} tasks."
