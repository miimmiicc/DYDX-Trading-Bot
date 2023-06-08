from datetime import datetime, timedelta
from pprint import pprint
from utils import format_number
import time

#GET EXISTING OPEN POSITIONS
def is_open_positions(client, market):

    #PROTECT API
    time.sleep(0.2)

    #GET POSITIONS
    all_positions = client.private.get_positions(
        market=market,
        status="OPEN"
    )

    if len(all_positions.data["positions"]) > 0:
        return True
    else:
        return False 


#CHECK ORDER STATUS
def check_order_status(client, order_id):
    order = client.private.get_order_by_id(order_id)
    if order.data:
        if "order" in order.data.keys():
            return order.data["order"]["status"]
    return "FAILED"


#PLACE MARKET ORDER

def place_market_order(client, market, side, size, price, reduce_only): 
    #Get Position ID
    account_response = client.private.get_account()
    position_id = account_response.data["account"]["positionId"]

    position_id

    #Get expiration time
    server_time = client.public.get_time() 
    expiration = datetime.fromisoformat(server_time.data["iso"].replace('Z','+00:00')) + timedelta(seconds=70)

    #Place an order
    placed_order = client.private.create_order(
        position_id = position_id, # required for creating the order signature
        market=market,
        side=side,
        order_type="MARKET",
        post_only=False,
        size=size,
        price=price,
        limit_fee='0.015',
        expiration_epoch_seconds=expiration.timestamp(),
        time_in_force="FOK",
        reduce_only=reduce_only
    )
    return placed_order.data

#ABORT ALL POSITIONS
def abort_all_positions(client):
    #CANCEL ALL ORDERS
    client.private.cancel_all_orders()

    #API PROTECTION
    time.sleep(0.5) 

    #GET MARKET
    markets = client.public.get_markets().data

    #API PROTECTION
    time.sleep(0.5)


    #GET ALL OPEN POSITIONS
    positions = client.private.get_positions(status = "OPEN")
    all_positions = positions.data["positions"]
    pprint(all_positions)
    #HANDLE OPEN POSITIONS

    close_orders = []
    if len(all_positions) > 0:
        for position in all_positions:

            #DETERMINE MARKET OF EVERY POSITION
            market = position["market"]

            #DETERMINE SIDE OF EVERY POSITION 
            side = "BUY"
            if position["side"] == "LONG":
                side = "SELL"
            print(market, side)

            #GET PRICE
            price = float(position["entryPrice"])
            accept_price = price * 1.7 if side == "BUY" else price * 0.3
            tick_size = markets["markets"][market]["tickSize"]
            accept_price = format_number(accept_price, tick_size)

            #PLACE ORDER TO CLOSE
            order = place_market_order(
                client,
                market,
                side,
                position["sumOpen"],
                accept_price,
                True
            )

            #APPEN THE RESULT
            close_orders.append(order) 

            #PROTECT API

            time.sleep(0.2)    
    #RETURN CLOSED ORDERS 
    return close_orders
        