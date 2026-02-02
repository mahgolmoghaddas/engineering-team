import gradio as gr
from accounts import Account, get_share_price

# Create an initial account (this is a prototype, so only one user is considered)
account = Account(user_id="user1", initial_deposit=1000.0)

def create_account(initial_deposit):
    global account
    account = Account(user_id="user1", initial_deposit=float(initial_deposit))
    return f"Account created with initial deposit: ${initial_deposit}"

def deposit_funds(amount):
    account.deposit(float(amount))
    return f"Deposited: ${amount}. Current balance: ${account.balance}"

def withdraw_funds(amount):
    if account.withdraw(float(amount)):
        return f"Withdrew: ${amount}. Current balance: ${account.balance}"
    return "Withdrawal failed. Insufficient funds."

def buy_shares(symbol, quantity):
    if account.buy_shares(symbol, int(quantity)):
        return f"Bought {quantity} shares of {symbol}. Current balance: ${account.balance}"
    return "Buy failed. Insufficient funds."

def sell_shares(symbol, quantity):
    if account.sell_shares(symbol, int(quantity)):
        return f"Sold {quantity} shares of {symbol}. Current balance: ${account.balance}"
    return "Sell failed. Insufficient shares."

def view_portfolio_value():
    return f"Portfolio Total Value: ${account.get_portfolio_value()}"

def view_profit_loss():
    return f"Profit/Loss: ${account.get_profit_loss()}"

def view_holdings():
    holdings = account.get_holdings()
    return f"Holdings: {holdings}"

def view_transaction_history():
    transactions = account.get_transaction_history()
    return f"Transaction History: {transactions}"

def get_share_price_ui(symbol):
    return f"Current Price of {symbol}: ${get_share_price(symbol)}"

with gr.Blocks() as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account Actions"):
        gr.Markdown("Create or manage your account.")
        initial_deposit_input = gr.Number(label="Initial Deposit")
        create_btn = gr.Button("Create Account")
        result_create = gr.Textbox(label="Output")
        create_btn.click(create_account, inputs=initial_deposit_input, outputs=result_create)
        
        deposit_amount_input = gr.Number(label="Deposit Amount")
        deposit_btn = gr.Button("Deposit Funds")
        result_deposit = gr.Textbox(label="Output")
        deposit_btn.click(deposit_funds, inputs=deposit_amount_input, outputs=result_deposit)
        
        withdraw_amount_input = gr.Number(label="Withdraw Amount")
        withdraw_btn = gr.Button("Withdraw Funds")
        result_withdraw = gr.Textbox(label="Output")
        withdraw_btn.click(withdraw_funds, inputs=withdraw_amount_input, outputs=result_withdraw)
    
    with gr.Tab("Trading Actions"):
        gr.Markdown("Buy or sell shares.")
        symbol_input = gr.Dropdown(["AAPL", "TSLA", "GOOGL"], label="Select Stock Symbol")
        quantity_input = gr.Number(label="Quantity")
        
        buy_btn = gr.Button("Buy Shares")
        result_buy = gr.Textbox(label="Output")
        buy_btn.click(buy_shares, inputs=[symbol_input, quantity_input], outputs=result_buy)
        
        sell_btn = gr.Button("Sell Shares")
        result_sell = gr.Textbox(label="Output")
        sell_btn.click(sell_shares, inputs=[symbol_input, quantity_input], outputs=result_sell)
        
    with gr.Tab("Reports"):
        view_portfolio_btn = gr.Button("View Portfolio Value")
        result_portfolio = gr.Textbox(label="Output")
        view_portfolio_btn.click(view_portfolio_value, outputs=result_portfolio)
        
        view_profit_loss_btn = gr.Button("View Profit/Loss")
        result_profit_loss = gr.Textbox(label="Output")
        view_profit_loss_btn.click(view_profit_loss, outputs=result_profit_loss)
        
        view_holdings_btn = gr.Button("View Holdings")
        result_holdings = gr.Textbox(label="Output")
        view_holdings_btn.click(view_holdings, outputs=result_holdings)
        
        view_transactions_btn = gr.Button("View Transaction History")
        result_transactions = gr.Textbox(label="Output")
        view_transactions_btn.click(view_transaction_history, outputs=result_transactions)
    
    with gr.Tab("Share Prices"):
        gr.Markdown("Get current share prices.")
        symbol_price_input = gr.Textbox(label="Stock Symbol")
        get_price_btn = gr.Button("Get Share Price")
        result_price = gr.Textbox(label="Output")
        get_price_btn.click(get_share_price_ui, inputs=symbol_price_input, outputs=result_price)

demo.launch()