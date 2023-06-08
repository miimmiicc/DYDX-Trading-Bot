from constants import RESOLUTION
from utils import get_iso_times
from pprint import pprint
import pandas as pd 
import numpy as np 
import time


#GET RELEVANT TIME PERIODS ISO FROM AND TO
ISO_TIMES = get_iso_times() 


#GET CANDLES RECENT
def get_candles_recent(client, market): 
    #DEFINE OUTPUT
    close_prices = []

    #PROTECT API
    time.sleep(0.2)

    #GET DATA
    candles = client.public.get_candles(
        market= market,
        resolution = RESOLUTION, 
        limit = 100
    )
    
    #STRUCTURE DATA 
    for candle in candles.data["candles"]:
        close_prices.append(candle["close"])

    #CONSTRUCT AND RETURN CLOSE PRICE SERIES
    close_prices.reverse()
    prices_result = np.array(close_prices).astype(np.float)
    return prices_result



#GET CANDLES HISTORY
def get_candles_historical(client, market):
    
    #DEFINE OUTPUT
    close_prices = []

    #EXTRACT HISTORICAL PRICE DATA FOR EACH TIMEFRAME
    for timeframe in ISO_TIMES.keys():

        #CONFIRM TIMES NEEDED
        tf_obj = ISO_TIMES[timeframe]
        from_iso = tf_obj["from_iso"]
        to_iso = tf_obj["to_iso"]

        #PROTECT RATE LIMITS
        time.sleep(0.2)

        #GET DATA
        candles = client.public.get_candles(
            market = market,
            resolution = RESOLUTION, 
            from_iso = from_iso,
            to_iso = to_iso,
            limit = 100
        )

        #DATA FORMAT
        for candle in candles.data["candles"]:
            close_prices.append({"datetime": candle["startedAt"], market: candle["close"]})
    
    #CONSTRUCT AND RETURN TIMEFRAME
    close_prices.reverse()
    return close_prices

#CONSTRUCT MARKET PRICES
def construct_market_prices(client):
    #DECLARE VARIABLES

    tradeable_markets = []
    markets = client.public.get_markets() 

    #FIND TRADEABLE PAIRS
    for market in markets.data["markets"].keys():
        market_info = markets.data["markets"][market]
        if market_info["status"] == "ONLINE" and market_info["type"] == "PERPETUAL":
            tradeable_markets.append(market)

    #SET INITIAL DATAFRAME
    close_prices = get_candles_historical(client, tradeable_markets[0])
    df = pd.DataFrame(close_prices)
    df.set_index("datetime", inplace=True)

    #TEST PRINT FOR FIRST COIN 
    # print(df.tail())


    #APPEND OTHER PRICES TO DATAFRAME
    #(TOTAL OF 5 PRICES INCLUDED HERE)
    for market in tradeable_markets[1:]: 
        close_prices_add = get_candles_historical(client,market)
        df_add = pd.DataFrame(close_prices_add)
        df_add.set_index("datetime", inplace = True)
        df = pd.merge(df , df_add, how="outer", on="datetime", copy=False)
        del df_add

    #CHECK FOR NaNS
    nans = df.columns[df.isna().any()].tolist()
    if len(nans) > 0:
        print("Dropping Columns!")
        print(nans)
        df.drop(columns=nans, inplace=True)

    #RETURN RESULT
    print(df)
    return df 
