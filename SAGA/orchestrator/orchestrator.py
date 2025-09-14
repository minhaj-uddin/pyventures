class Orchestrator:
    def __init__(self, restaurant_service, payment_service, delivery_service):
        self.restaurant = restaurant_service
        self.payment = payment_service
        self.delivery = delivery_service

    def run_saga(self, order_id: str):
        print(f"Starting Saga for Order: {order_id}")

        print("Step 1: Asking restaurant to prepare food...")
        if not self.restaurant.prepare(order_id):
            print("Restaurant preparation failed. Saga aborted.")
            return

        print("Step 2: Charging payment...")
        if not self.payment.charge(order_id):
            print("Payment failed. Rolling back restaurant...")
            self.restaurant.cancel(order_id)
            return

        print("Step 3: Scheduling delivery...")
        if not self.delivery.schedule(order_id):
            print("Delivery failed. Rolling back payment and restaurant...")
            self.payment.refund(order_id)
            self.restaurant.cancel(order_id)
            return

        print(f"Order {order_id} completed successfully!")
