from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES, MANAGE_EXITS 
from connection import connect_dydx
from private import abort_all_positions
from public import construct_market_prices, get_candles_historical
from cointegration import store_cointegration_result
from entry_pairs import open_positions
from exit_pairs import manage_trade_exits
from messaging import send_message


if __name__ == "__main__":
    #Connecting to client
    success = send_message("Bot Running")
    try:
        print("CONNECTING TO CLIENT")
        client = connect_dydx()
    except Exception as e: 
        print("Error connecting to client",e)
        send_message("Failed to Connect To cleint")
        exit(1)
    
    #Abort all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print("CLOSING ALL POSITIONS")
            close_orders = abort_all_positions(client)
        except Exception as e:
            print("ERROR CLOSING ALL POSITIONS", e)
            send_message("Failed to close all positions")
            exit(1)

    #FINDING COINTEGRATED PAIRS
    if FIND_COINTEGRATED:
        #CONSTRUCT MARKET PRICES
        try:
            print("FETCHING MARKET PRICES...")
            df_market_prices = construct_market_prices(client)
        except Exception as e:
            print("ERROR CONSTRUCTING MARKET PRICE!!!", e)
            send_message("ERROR CONSTRUCTING MARKET PRICE!!!")
            exit(1)
        #STORE COINTEGRATED PAIRS
        try:
            print("STORING COINTEGRATED PAIRS")
            stores_result = store_cointegration_result(df_market_prices)
            if stores_result != "saved":
                print("ERROR SAVING COINTEGRATED PRICES!!!")
                send_message("ERROR SAVING COINTEGRATED PRICES 101!!!")
                exit(1)
        except Exception as e:
            print("ERROR SAVING COINTEGRATED PRICES: ", e)
            send_message("ERROR SAVING COINTEGRATED PRICES 102!!!")
            exit(1)

    #RUN AS ALWAYS ON
    while True:

        #MANAGING EXITS FOR OPEN POSITIONS
        if MANAGE_EXITS:
            try:
                print("MANAGING EXITS!")
                manage_trade_exits(client)
            except Exception as e:
                print("ERROR MANAGING EXITING PAIRS: ", e)
                send_message("ERROR MANAGING EXITING PAIRS!!!")
                exit(1)

        #PLACE TRADES FOR OPENING POSITIONS
        if PLACE_TRADES:
            try:
                print("FINDING TRADING OPPORTUNITIES!")
                open_positions(client)
            except Exception as e:
                print("ERROR TRADING PAIRS: ", e)
                send_message("ERROR TRADING PAIRS!!!")
                exit(1)