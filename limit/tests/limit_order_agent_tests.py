import unittest
from unittest.mock import MagicMock
from trading_framework.execution_client import ExecutionClient
from limit.limit_order_agent import LimitOrderAgent

class TestLimitOrderAgent(unittest.TestCase):

    def setUp(self):
        self.mock_execution_client = MagicMock(spec=ExecutionClient)
        self.agent = LimitOrderAgent(self.mock_execution_client)

    def test_buy_order_executes_when_price_drops_below_limit(self):
        # Test buying 1000 shares of IBM when the price drops below $100
        self.agent.add_order('buy', 'IBM', 1000, 100)
        self.agent.on_price_tick('IBM', 98)

        # Assert the buy order was executed
        self.mock_execution_client.buy.assert_called_once_with('IBM', 1000)

    def test_sell_order_executes_when_price_rises_above_limit(self):
        # Test selling 500 shares of AAPL when the price rises above $150
        self.agent.add_order('sell', 'AAPL', 500, 150)
        self.agent.on_price_tick('AAPL', 155)

        # Assert the sell order was executed
        self.mock_execution_client.sell.assert_called_once_with('AAPL', 500)

    def test_order_does_not_execute_if_price_does_not_meet_limit(self):
        # Add a buy order that should not be executed because the price is too high
        self.agent.add_order('buy', 'IBM', 1000, 100)
        self.agent.on_price_tick('IBM', 102)

        # Assert the buy order was not executed
        self.mock_execution_client.buy.assert_not_called()

    def test_multiple_orders_execution(self):
        # Add multiple orders
        self.agent.add_order('buy', 'IBM', 1000, 100)
        self.agent.add_order('sell', 'AAPL', 500, 150)

        # Simulate price ticks
        self.agent.on_price_tick('IBM', 98)
        self.agent.on_price_tick('AAPL', 155)

        # Assert both orders were executed
        self.mock_execution_client.buy.assert_called_once_with('IBM', 1000)
        self.mock_execution_client.sell.assert_called_once_with('AAPL', 500)

if _name_ == '_main_':
    unittest.main()