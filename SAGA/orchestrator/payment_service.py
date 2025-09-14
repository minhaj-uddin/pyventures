class PaymentService:
    def charge(self, order_id):
        print(f"PaymentService: Charging customer for {order_id}")
        if order_id.endswith("FAIL"):
            return False
        return True

    def refund(self, order_id):
        print(f"PaymentService: Refunding customer for {order_id}")
