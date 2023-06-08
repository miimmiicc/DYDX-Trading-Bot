from dydx3.constants import API_HOST_GOERLI
from decouple import config


# SELECT MODE
MODE = "DEVELOPMENT"

#COIN SPECIFICATIONS OF FACTOR 10
TOKEN_FACTOR_10 = ["XLM-USD","DOGE-USD","TRON-USD", "ICP-USD"]

# CLOSE ALL OPEN POSITIONS AND ORDERS
ABORT_ALL_POSITIONS = True

# FIND COINTEGRATED PAIRS
FIND_COINTEGRATED = True

# MANAGE EXITS
MANAGE_EXITS = True

# PLACE TRADES
PLACE_TRADES = True

# RESOLUTION
RESOLUTION = "1HOUR"


# STATISTICAL WINDOW (MOVING AVERAGE)
WINDOW = 21


#THRESHOLD - Opening
MAX_HALF_LIFE = 24
ZSCORE_THRESH = 1.5
USD_PER_TRADE = 50
USD_MIN_COLLATERAL = 1900


#THRESHOLD - Closing
CLOSE_AT_ZSCORE_CROSS = True


# ETHEREUM ADDRESS
ETHEREUM_ADDRESS = "0xA751480623e08B0bF9F3a2D2b4e0e901F5dB0898"


# PRODUCTION KEYS
STARK_PRIVATE_KEY_TESTNET = config("STARK_PRIVATE_KEY_TESTNET")
DYDX_API_KEY_TESTNET = config("DYDX_API_KEY_TESTNET")
DYDX_API_SECRET_TESTNET = config("DYDX_API_SECRET_TESTNET")
DYDX_API_PASSPHRASE_TESTNET = config("DYDX_API_PASSPHRASE_TESTNET")


#!!!!! CHANGE EXPORT KEY LOGIC WHEN MAINNET KEY IS ADDED !!!!!
# MAIN KEYS - EXPORT
STARK_PRIVATE_KEY = STARK_PRIVATE_KEY_TESTNET
DYDX_API_KEY = DYDX_API_KEY_TESTNET
DYDX_API_SECRET = DYDX_API_SECRET_TESTNET
DYDX_API_PASSPHRASE = DYDX_API_PASSPHRASE_TESTNET


#HOST - EXPORT
HOST = API_HOST_GOERLI


# HTTP PROVIDER
HTTP_PROVIDER_TESTNET = "https://eth-goerli.g.alchemy.com/v2/ms1LmQFq_9FwUL4Gsg0I1OFUDfeQgpsW"


HTTP_PROVIDER = HTTP_PROVIDER_TESTNET
