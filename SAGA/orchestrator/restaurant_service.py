class RestaurantService:
    def prepare(self, order_id):
        print(f"RestaurantService: Preparing food for order {order_id}")
        return True

    def cancel(self, order_id):
        print(f"RestaurantService: Canceling food prep for order {order_id}")
