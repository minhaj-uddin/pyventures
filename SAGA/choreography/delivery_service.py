class DeliveryService:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.event_bus.subscribe("PaymentCompleted", self.schedule_delivery)

    def schedule_delivery(self, data):
        print(
            f"DeliveryService: Scheduling delivery for order {data['order_id']}")
        self.event_bus.publish("DeliveryScheduled", {
                               "order_id": data["order_id"]})
