from orchestrator import Orchestrator
from restaurant_service import RestaurantService
from payment_service import PaymentService
from delivery_service import DeliveryService

if __name__ == "__main__":
    import sys
    order_id = sys.argv[1] if len(sys.argv) > 1 else "ORDER-123"

    orchestrator = Orchestrator(
        restaurant_service=RestaurantService(),
        payment_service=PaymentService(),
        delivery_service=DeliveryService()
    )

    orchestrator.run_saga(order_id)
