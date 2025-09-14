import time
from event_bus import RedisEventBus
from order_service import OrderService
from restaurant_service import RestaurantService
from payment_service import PaymentService
from delivery_service import DeliveryService


def run(order_id):
    bus = RedisEventBus()

    # Start all services
    OrderService(bus)
    RestaurantService(bus)
    PaymentService(bus)
    DeliveryService(bus)

    # Trigger order creation
    bus.publish("OrderCreated", {"order_id": order_id})

    # Keep the main thread alive to allow background listeners to run
    while True:
        time.sleep(1)


if __name__ == "__main__":
    import sys
    order_id = sys.argv[1] if len(sys.argv) > 1 else "ORDER-123"
    run(order_id)
