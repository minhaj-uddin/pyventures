class OrderService:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.event_bus.subscribe("PaymentFailed", self.handle_payment_failed)
        self.event_bus.subscribe(
            "DeliveryScheduled", self.handle_delivery_scheduled)

    def create_order(self, order_id):
        print(f"OrderService: Creating order {order_id}")
        self.event_bus.publish("OrderCreated", {"order_id": order_id})

    def handle_payment_failed(self, data):
        print(
            f"OrderService: Cancelling order {data['order_id']} due to payment failure.")

    def handle_delivery_scheduled(self, data):
        print(
            f"OrderService: Order {data['order_id']} completed and delivery scheduled.")
