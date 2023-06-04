from constants import RESOLUTION
from utils import get_iso_times
from pprint import pprint
import pandas as pd 
import numpy as np 
import time


#GET RELEVANT TIME PERIODS ISO FROM AND TO
ISO_TIMES = get_iso_times() 


#GET CANDLES HISTORY
def get_candles_historical(client, market):
    
    #DEFINE OUTPUT
    close_prices = []

    #EXTRACT HISTORICAL PRICE DATA FOR EACH TIMEFRAME
    for timeframe in ISO_TIMES.keys():

        #CONFIRM TIMES NEEDED
        tf_obj = ISO_TIMES(timeframe)
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
    pass