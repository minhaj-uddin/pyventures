class DeliveryService:
    def schedule(self, order_id):
        print(f"DeliveryService: Scheduling delivery for order {order_id}")
        return True

    def cancel(self, order_id):
        print(f"DeliveryService: Cancelling delivery for {order_id}")
