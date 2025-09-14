class PaymentService:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.event_bus.subscribe("RestaurantConfirmed", self.charge_payment)

    def charge_payment(self, data):
        order_id = data['order_id']
        print(f"PaymentService: Charging customer for order {order_id}")

        # Simulate failure for specific order IDs
        if order_id.endswith("FAIL"):
            self.event_bus.publish("PaymentFailed", {"order_id": order_id})
        else:
            self.event_bus.publish("PaymentCompleted", {"order_id": order_id})
