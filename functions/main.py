from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED 
from connection import connect_dydx
from private import abort_all_positions
from public import construct_market_prices, get_candles_historical
from cointegration import store_cointegration_result
if __name__ == "__main__":
    #Connecting to client
    try:
        print("CONNECTING TO CLIENT")
        client = connect_dydx()
    except Exception as e: 
        print("Error connecting to client",e)
        exit(1)
    
    #Abort all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print("CLOSING ALL POSITIONS")
            close_orders = abort_all_positions(client)
        except Exception as e:
            print("ERROR CLOSING ALL POSITIONS", e)
            exit(1)

    #FINDING COINTEGRATED PAIRS
    if FIND_COINTEGRATED:
        #CONSTRUCT MARKET PRICES
        try:
            print("FETCHING MARKET PRICES...")
            df_market_prices = construct_market_prices(client)
        except Exception as e:
            print("ERROR CONSTRUCTING MARKET PRICE!!!", e)
            exit(1)
        #STORE COINTEGRATED PAIRS
        try:
            print("STORING COINTEGRATED PAIRS")
            stores_result = store_cointegration_result(df_market_prices)
            if stores_result != "saved":
                print("ERROR SAVING COINTEGRATED PRICES!!!")
                exit(1)
        except Exception as e:
            print("ERROR SAVING COINTEGRATED PRICES: ", e)
            exit(1)