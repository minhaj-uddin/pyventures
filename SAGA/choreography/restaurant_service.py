class RestaurantService:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.event_bus.subscribe("OrderCreated", self.confirm_restaurant)

    def confirm_restaurant(self, data):
        print(
            f"RestaurantService: Confirming food prep for order {data['order_id']}")
        self.event_bus.publish("RestaurantConfirmed", {
                               "order_id": data["order_id"]})
