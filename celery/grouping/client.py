from celery import chord
from tasks import (
    charge_payment,
    reserve_inventory,
    schedule_delivery,
    send_confirmation_email,
    log_fulfillment_summary
)

if __name__ == '__main__':
    order_id = "ORDER-12345"

    fulfillment_tasks = [
        charge_payment.s(order_id),
        reserve_inventory.s(order_id),
        schedule_delivery.s(order_id),
        send_confirmation_email.s(order_id),
    ]

    result = chord(
        fulfillment_tasks,
        log_fulfillment_summary.s()
    )()

    print(f"Order fulfillment started for {order_id}. Chord ID: {result.id}")
