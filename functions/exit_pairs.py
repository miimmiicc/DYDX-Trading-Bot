from constants import CLOSE_AT_ZSCORE_CROSS
from utils import format_number
from public import get_candles_recent
from cointegration import calculate_zscore
from private import place_market_order
import json 
import time
from pprint import pprint


#CLOSE POSITIONS

def manage_trade_exits(client):
    """
        MANAGE EXITING OPEN POSITIONSBASED UPON CRITERIA SET IN CONSTANTS
    """
    
    #INITIALIZE SABING OUTPUT
    save_output = []

    #OPEN JSON FILE 
    try: 
        open_positions_file = open("bot_agents.json")
        open_positions_dict = json.load(open_positions_file)
    except:
        return "complete"
    
    #GUARD: EXIT IF NO OPEN POSITIONS IN FILE 
    if len(open_positions_dict) < 1: 
        return "complete"
    
    #GET ALL OPEN POSITIONS PER TRADING PLATFORM
    exchange_pos = client.private.get_positions(status = "OPEN")
    all_exc_pos = exchange_pos.data["positions"]
    markets_live = []
    for p in all_exc_pos: 
        markets_live.append(p["market"])

    #PROTECT API
    time.sleep(0.5)
    pprint(markets_live)

    #CHECK ALL SAVED POSITIONS MATCH ORDER RECORD
    #EXIT TRADE ACCORDING TO ANY EXIT TRADE RULES
    for position in open_positions_dict:
        #INITIALIZE is_close TRIGGER
        is_close = False

        #EXTRACT POSITION MATCHING INFORMATION FROM JSON FILE -- MARKET 1
        position_market_m1 = position["market_1"]
        position_size_m1 = position["order_m1_size"]
        position_side_m1 = position["order_m1_side"]

        #EXTRACT POSITION MATCHING INFORMATION FROM JSON FILE -- MARKET 2
        position_market_m2 = position["market_2"]
        position_size_m2 = position["order_m2_size"]
        position_side_m2 = position["order_m2_side"]


        #PROTECT API
        time.sleep(0.5)

        #GET ORDER INFO M1 PER EXCHANGE
        order_m1 = client.private.get_order_by_id(position["order_id_m1"])
        order_market_m1 = order_m1.data["order"]["market"]
        order_size_m1 = order_m1.data["order"]["size"]
        order_side_m1 = order_m1.data["order"]["side"]

        #PROTECT API 
        time.sleep(0.5)

        #GET ORDER INFO M2 PER EXCHANGE
        order_m2 = client.private.get_order_by_id(position["order_id_m2"])
        order_market_m2 = order_m2.data["order"]["market"]
        order_size_m2 = order_m2.data["order"]["size"]
        order_side_m2 = order_m2.data["order"]["side"]

        #PERFORM MATCHING CHECKS
        check_m1 = position_market_m1 == order_market_m1 and position_size_m1 == order_size_m1 and position_side_m1 == order_side_m1
        check_m2 = position_market_m2 == order_market_m2 and position_size_m2 == order_size_m2 and position_side_m2 == order_side_m2
        check_live = position_market_m1 in markets_live and position_market_m2 in markets_live

        #GUARD: IF NOT ALL MATCH EXIT WITH ERROR
        if not check_m1 or not check_m2 or not check_live: 
            print(f"WARNING: NOT ALL OPEN POSITIONS MATCH EXCHANGE RECORDS FOR {position_market_m1} and {position_market_m2}")
            continue 

        #GET PRICES 
        series_1 = get_candles_recent(client, position_market_m1)
        time.sleep(0.2)
        series_2 = get_candles_recent(client, position_market_m2)
        time.sleep(0.2)

        #GET MARKETS FOR REFERENCE OF TICK SIZE 
        markets = client.public.get_markets().data

        #PROTECT API 
        time.sleep(0.2)

        #TRIGGER CLOSE BASED ON Z-SCORE
        if CLOSE_AT_ZSCORE_CROSS:
            #INITIALIZE Z-SCORE
            hedge_ratio = position["hedge_ratio"]
            z_score_traded = position["z_score"]
            if len(series_1) > 0 and len(series_1) == len(series_2):
                spread = series_1 - (hedge_ratio * series_2)
                z_score_current = calculate_zscore(spread).values.tolist()[-1]

            #DETERMINE TRIGGER
            z_score_level_check = abs(z_score_current) >= abs(z_score_traded)
            z_score_cross_check = (z_score_current < 0 and z_score_traded > 0) or (z_score_current > 0 and z_score_traded < 0)
            
            #CLOSE TRADE
            if z_score_level_check and z_score_cross_check:

                #INITIATE CLOSE TRIGGER
                is_close = True

        
        #CLOSE POSITIONS IF TRIGGERED
        if is_close:
            #DETERMINE SIDE - M1
            side_m1 = "SELL"
            if position_side_m1 == "SELL":
                side_m1 = "BUY"

            #DETERMINE SIDE - M2
            side_m2 = "SELL"
            if position_side_m2 == "SELL":
                side_m2 = "BUY"

            #GET AND FORMAT PRICE
            price_m1 = float(series_1[-1])
            price_m2 = float(series_2[-1])
            accept_price_m1 = price_m1 * 1.05 if side_m1 == "BUY" else price_m1 * 0.95
            accept_price_m2 = price_m2 * 1.05 if side_m2 == "BUY" else price_m2 * 0.95
            tick_size_m1 = markets["markets"][position_market_m1]["tickSize"]
            tick_size_m2 = markets["markets"][position_market_m2]["tickSize"]
            accept_price_m1 = format_number(accept_price_m1, tick_size_m1)
            accept_price_m2 = format_number(accept_price_m2, tick_size_m2)


            #CLOSE POSITIONS
            try:
                #CLOSE POSITION FOR MARKET 1
                print("!!! CLOSING POSITION FOR MARKET 1 !!!")
                print(f"Closing position for {position_market_m1}")
                close_order_m1 = place_market_order(
                    client,
                    market=position_market_m1,
                    side=side_m1,
                    size=position_size_m1,
                    price=accept_price_m1,
                    reduce_only=True,
                )

                print(close_order_m1["order"]["id"])
                print("!!! CLOSING !!!")
                print(" ")
                #PROTECT API 
                time.sleep(1)

                #CLOSE POSITION FOR MARKET 2
                print("!!! CLOSING POSITION FOR MARKET 2 !!!")
                print(f"Closing position for {position_market_m2}")
                close_order_m2 = place_market_order(
                    client,
                    market=position_market_m2,
                    side=side_m2,
                    size=position_size_m2,
                    price=accept_price_m2,
                    reduce_only=True,
                )

                print(close_order_m2["order"]["id"])
                print("!!! CLOSING !!!")
                print(" ")
            except Exception as e:
                print(f"Exit failed for {position_market_m1} with {position_market_m2}")
                save_output.append(position)

        #KEEP RECORD OF ITEMS AND SAVE 
        else: 
            save_output.append(position)

    #SAVE REMAINING ITEMS
    print(f"{len(save_output)} Items remaining. Saving file...")
    with open("bot_agents.json", "w") as f:
        json.dump(save_output, f)

        
