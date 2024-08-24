from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener

class LimitOrderAgent(PriceListener):

    def init(self, execution_client: ExecutionClient) -> None:
        super().init()
        self.execution_client = execution_client
        self.orders = []

    def add_order(self, side: str, product_id: str, amount: int, limit: float):
        order = {
            'side': side,
            'product_id': product_id,
            'amount': amount,
            'limit': limit,
            'executed': False
        }
        self.orders.append(order)

    def on_price_tick(self, product_id: str, price: float):
        for order in self.orders:
            if not order['executed'] and order['product_id'] == product_id:
                if order['side'] == 'buy' and price <= order['limit']:
                    self.execution_client.buy(product_id, order['amount'])
                    order['executed'] = True
                    print(f"Executed buy order for {order['amount']} shares of {product_id} at {price}")
                elif order['side'] == 'sell' and price >= order['limit']:
                    self.execution_client.sell(product_id, order['amount'])
                    order['executed'] = True
                    print(f"Executed sell order for {order['amount']} shares of {product_id} at {price}")

# Example usage
execution_client = ExecutionClient()
agent = LimitOrderAgent(execution_client)

# Add orders
agent.add_order('buy', 'IBM', 1000, 100)  
agent.add_order('sell', 'AAPL', 500, 150)  

# Simulate price ticks
agent.on_price_tick('IBM', 98)
agent.on_price_tick('AAPL', 155)