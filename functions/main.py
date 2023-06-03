from functions import connect_dydx

if __name__ == "__main__":
    #Connecting to client
    try:
        client = connect_dydx()
    except Exception as e: 
        print(e)
        print("Error in Conncetion",e)
        exit(1)