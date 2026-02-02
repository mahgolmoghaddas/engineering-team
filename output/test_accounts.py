import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('user1', 1000.0)

    def test_initial_deposit(self):
        self.assertEqual(self.account.balance, 1000.0)

    def test_deposit(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(self.account.transactions[-1]['type'], 'deposit')
        self.assertEqual(self.account.transactions[-1]['amount'], 500.0)

    def test_withdraw_valid(self):
        success = self.account.withdraw(300.0)
        self.assertTrue(success)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(self.account.transactions[-1]['type'], 'withdraw')
        self.assertEqual(self.account.transactions[-1]['amount'], 300.0)

    def test_withdraw_invalid(self):
        success = self.account.withdraw(1500.0)
        self.assertFalse(success)
        self.assertEqual(self.account.balance, 1000.0)

    def test_buy_shares_valid(self):
        success = self.account.buy_shares('AAPL', 5)
        self.assertTrue(success)
        self.assertEqual(self.account.portfolio['AAPL'], 5)
        self.assertEqual(self.account.transactions[-1]['type'], 'buy')
        self.assertEqual(self.account.transactions[-1]['quantity'], 5)

    def test_buy_shares_invalid(self):
        success = self.account.buy_shares('AAPL', 1000)
        self.assertFalse(success)
        self.assertNotIn('AAPL', self.account.portfolio)

    def test_sell_shares_valid(self):
        self.account.buy_shares('AAPL', 5)
        success = self.account.sell_shares('AAPL', 3)
        self.assertTrue(success)
        self.assertEqual(self.account.portfolio['AAPL'], 2)
        self.assertEqual(self.account.transactions[-1]['type'], 'sell')
        self.assertEqual(self.account.transactions[-1]['quantity'], 3)

    def test_sell_shares_invalid(self):
        success = self.account.sell_shares('AAPL', 3)
        self.assertFalse(success)
        self.assertNotIn('AAPL', self.account.portfolio)

    def test_get_portfolio_value(self):
        self.account.buy_shares('AAPL', 5)
        portfolio_value = self.account.get_portfolio_value()
        self.assertEqual(portfolio_value, 5 * get_share_price('AAPL'))

    def test_get_profit_loss(self):
        self.account.buy_shares('AAPL', 5)
        profit_loss = self.account.get_profit_loss()
        self.assertEqual(profit_loss, self.account.balance + 5 * get_share_price('AAPL') - self.account.initial_deposit)

    def test_get_holdings(self):
        self.account.buy_shares('AAPL', 5)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {'AAPL': 5})

    def test_get_transaction_history(self):
        self.account.deposit(200.0)
        self.account.withdraw(200.0)
        self.account.buy_shares('AAPL', 2)
        self.account.sell_shares('AAPL', 2)
        transactions = self.account.get_transaction_history()
        self.assertEqual(len(transactions), 5)

if __name__ == '__main__':
    unittest.main()