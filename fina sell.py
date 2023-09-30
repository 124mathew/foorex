
import MetaTrader5 as mt5
import time

# Connect to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Symbol and order parameters
symbol = "GBPUSDmicro"
volume = 0.5
desired_start_price = 1.22035  # Set your desired start price here

# Wait for the desired start price or market price to be lower than the desired start price
while True:
    # Get the current market price (use bid or ask, depending on your strategy)
    current_price = mt5.symbol_info_tick(symbol).bid
    
    if current_price <= desired_start_price:
        print("Market price reached or is below the desired start price. Starting the loop.")
        break
    
    # Wait for 1 second before checking again
    time.sleep(1)

# Symbol and order parameters after the desired start price is reached
initial_pending_price = mt5.symbol_info_tick(symbol).ask + 3 * mt5.symbol_info(symbol).point
tp = initial_pending_price + 135 * mt5.symbol_info(symbol).point
sl = initial_pending_price - 130 * mt5.symbol_info(symbol).point

# Counter for wins and losses
cumulative_count = 0

# Place the initial pending buy stop order
request = {
    "action": mt5.TRADE_ACTION_PENDING,
    "symbol": symbol,
    "volume": volume,
    "type": mt5.ORDER_TYPE_BUY_STOP,
    "price": initial_pending_price,
    "sl": sl,
    "tp": tp,
}

result = mt5.order_send(request)

if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("Pending buy stop order send failed, error code =", result.retcode)
else:
    print("Initial pending buy stop order placed successfully")

# Keep track of the current pending order
current_pending_price = initial_pending_price
current_order_type = mt5.ORDER_TYPE_BUY_STOP

# Main loop
while True:
    # Wait for 1 second to avoid excessive loop execution
    time.sleep(1)
    
    # Get the latest ticks
    ticks = mt5.symbol_info_tick(symbol)
    
    # Check if TP or SL is hit
    if current_order_type == mt5.ORDER_TYPE_BUY_STOP and ticks.ask >= current_pending_price + 147 * mt5.symbol_info(symbol).point:
        cumulative_count += 1
        
        # Exit the loop if cumulative count reaches +1
        if cumulative_count >= 1:
            print("Cumulative count reached +1. Stopping the loop.")
            break
        
        # Place a new pending buy stop order
        new_pending_price = ticks.ask + 10 * mt5.symbol_info(symbol).point
        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY_STOP,
            "price": new_pending_price,
            "sl": new_pending_price - 130 * mt5.symbol_info(symbol).point,
            "tp": new_pending_price + 135 * mt5.symbol_info(symbol).point,
        }
        
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("New pending buy stop order send failed, error code =", result.retcode)
        else:
            print("New pending buy stop order placed successfully")
        
        # Update the current pending order
        current_pending_price = new_pending_price
        
    elif current_order_type == mt5.ORDER_TYPE_BUY_STOP and ticks.bid <= current_pending_price - 147 * mt5.symbol_info(symbol).point:
        cumulative_count -= 1
        
        # Exit the loop if cumulative count reaches +1
        if cumulative_count >= 1:
            print("Cumulative count reached +1. Stopping the loop.")
            break
        
        # Place a new pending sell stop order
        new_pending_price = ticks.bid - 10 * mt5.symbol_info(symbol).point
        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL_STOP,
            "price": new_pending_price,
            "sl": new_pending_price + 130 * mt5.symbol_info(symbol).point,
            "tp": new_pending_price - 135 * mt5.symbol_info(symbol).point,
        }
        
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("New pending sell stop order send failed, error code =", result.retcode)
        else:
            print("New pending sell stop order placed successfully")
        
        # Update the current pending order
        current_pending_price = new_pending_price
        current_order_type = mt5.ORDER_TYPE_SELL_STOP
    
    # Check if TP or SL is hit for the SELL_STOP order
    elif current_order_type == mt5.ORDER_TYPE_SELL_STOP and ticks.bid <= current_pending_price - 147 * mt5.symbol_info(symbol).point:
        cumulative_count += 1
        
        # Exit the loop if cumulative count reaches +1
        if cumulative_count >= 1:
            print("Cumulative count reached +1. Stopping the loop.")
            break
        
        # Place a new pending sell stop order
        new_pending_price = ticks.bid - 10 * mt5.symbol_info(symbol).point
        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL_STOP,
            "price": new_pending_price,
            "sl": new_pending_price + 130 * mt5.symbol_info(symbol).point,
            "tp": new_pending_price - 135 * mt5.symbol_info(symbol).point,
        }
        
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("New pending sell stop order send failed, error code =", result.retcode)
        else:
            print("New pending sell stop order placed successfully")
        
        # Update the current pending order
        current_pending_price = new_pending_price
        
    elif current_order_type == mt5.ORDER_TYPE_SELL_STOP and ticks.ask >= current_pending_price + 147 * mt5.symbol_info(symbol).point:
        cumulative_count -= 1
        
        # Exit the loop if cumulative count reaches +1
        if cumulative_count >= 1:
            print("Cumulative count reached +1. Stopping the loop.")
            break
        
        # Place a new pending buy stop order
        new_pending_price = ticks.ask + 10 * mt5.symbol_info(symbol).point
        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY_STOP,
            "price": new_pending_price,
            "sl": new_pending_price - 130 * mt5.symbol_info(symbol).point,
            "tp": new_pending_price + 135 * mt5.symbol_info(symbol).point,
        }
        
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("New pending buy stop order send failed, error code =", result.retcode)
        else:
            print("New pending buy stop order placed successfully")
        
        # Update the current pending order
        current_pending_price = new_pending_price

# Disconnect from the MetaTrader 5 terminal
mt5.shutdown()

