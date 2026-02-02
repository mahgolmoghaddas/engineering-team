import gradio as gr
from accounts import Account

# Create a global account instance for demonstration purposes
account = Account(username="demo_user")

# Define Gradio interface functions
def create_account(username):
    global account
    account = Account(username=username)
    return f"Account created for {username}."


def deposit_funds(amount):
    if account.deposit(float(amount)):
        return f"Successfully deposited ${amount}. New balance: ${account.balance:.2f}"
    else:
        return "Deposit failed. Please enter a valid amount."


def withdraw_funds(amount):
    if account.withdraw(float(amount)):
        return f"Successfully withdrew ${amount}. New balance: ${account.balance:.2f}"
    else:
        return "Withdrawal failed. Insufficient funds or invalid amount."


def buy_shares(symbol, quantity):
    if account.buy_shares(symbol, int(quantity)):
        return f"Successfully bought {quantity} shares of {symbol}."
    else:
        return "Purchase failed. Insufficient balance or invalid quantity."


def sell_shares(symbol, quantity):
    if account.sell_shares(symbol, int(quantity)):
        return f"Successfully sold {quantity} shares of {symbol}."
    else:
        return "Sale failed. Insufficient shares or invalid quantity."


def get_portfolio_summary():
    holdings = account.get_holdings()
    summary = "\n".join([f"{symbol}: {quantity}" for symbol, quantity in holdings.items()])
    total_value = account.get_portfolio_value()
    return f"Holdings:\n{summary}\nTotal Portfolio Value: ${total_value:.2f}"


def get_profit_loss():
    profit_loss = account.get_profit_loss()
    return f"Profit/Loss: ${profit_loss:.2f}"


def list_transactions():
    transactions = account.get_transactions()
    summary = "\n".join([f"Date: {t['date']}, Type: {t['type']}, Symbol: {t['symbol']}, "
                             f"Quantity: {t['quantity']}, Price per Share: {t['price']}" for t in transactions])
    return f"Transactions:\n{summary}"

# Define Gradio Interface
iface = gr.Interface(
    fn=[create_account, deposit_funds, withdraw_funds, buy_shares, sell_shares, get_portfolio_summary, get_profit_loss, list_transactions],
    inputs=["text", "number", "number", "text", "number", None, None, None],
    outputs=["text", "text", "text", "text", "text", "text", "text", "text"],
    live=False
)

# Launch the interface
iface.launch()