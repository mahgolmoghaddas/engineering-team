# accounts.py

```python
# Mock function to simulate current stock prices
def get_share_price(symbol):
    prices = {
        'AAPL': 150.0,
        'TSLA': 700.0,
        'GOOGL': 2800.0
    }
    return prices.get(symbol, 0.0)

class Account:
    def __init__(self, user_id: str, initial_deposit: float) -> None:
        self.user_id = user_id
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.portfolio = {}
        self.transactions = []
        self.transactions.append({
            'type': 'deposit',
            'amount': initial_deposit,
            'balance': self.balance
        })

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
            self.transactions.append({
                'type': 'deposit',
                'amount': amount,
                'balance': self.balance
            })

    def withdraw(self, amount: float) -> bool:
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transactions.append({
                'type': 'withdraw',
                'amount': amount,
                'balance': self.balance
            })
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        if quantity <= 0:
            return False
        price = get_share_price(symbol)
        total_cost = price * quantity
        if self.balance >= total_cost:
            self.balance -= total_cost
            self.portfolio[symbol] = self.portfolio.get(symbol, 0) + quantity
            self.transactions.append({
                'type': 'buy',
                'symbol': symbol,
                'quantity': quantity,
                'price': price,
                'balance': self.balance
            })
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if quantity <= 0:
            return False
        if self.portfolio.get(symbol, 0) >= quantity:
            price = get_share_price(symbol)
            total_sale_value = price * quantity
            self.balance += total_sale_value
            self.portfolio[symbol] -= quantity
            if self.portfolio[symbol] == 0:
                del self.portfolio[symbol]
            self.transactions.append({
                'type': 'sell',
                'symbol': symbol,
                'quantity': quantity,
                'price': price,
                'balance': self.balance
            })
            return True
        return False

    def get_portfolio_value(self) -> float:
        total_value = 0.0
        for symbol, quantity in self.portfolio.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_loss(self) -> float:
        current_value = self.balance + self.get_portfolio_value()
        return current_value - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.portfolio

    def get_transaction_history(self) -> list:
        return self.transactions
```