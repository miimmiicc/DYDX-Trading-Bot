from constants import RESOLUTION
from utils import get_iso_times
from pprint import pprint
import pandas as pd 
import numpy as np 
import time


#GET RELEVANT TIME PERIODS ISO FROM AND TO
ISO_TIMES = get_iso_times() 
pprint(ISO_TIMES)

#CONSTRUCT MARKET PRICES
def construct_market_prices(client):
    pass