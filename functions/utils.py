from datetime import datetime, timedelta

#FORMAT NUMBER 
def format_number(curr_num, match_num):
    
    #FUNCTION WILL RETURN THE CORRECTLY FORMATTED STRING

    curr_num_string = f"{curr_num}"
    match_num_string = f"{match_num}"

    if "." in match_num_string:
        match_decimals = len(match_num_string.split(".")[1])
        curr_num_string = f"{curr_num:.{match_decimals}f}"
        curr_num_string = curr_num_string[:]
        return curr_num_string
    else:
        return f"{int(curr_num)}"

#FORMAT TIME
def format_time(timestamp):
    return timestamp.replace(microsecond = 0).isoformat()


# GET ISO TIMES
def get_iso_times():

    #GET TIMESTAMPS
    date_start_0 = datetime.now()
    date_start_1 = date_start_0 - timedelta(hours=100)
    date_start_2 = date_start_1 - timedelta(hours=100)
    date_start_3 = date_start_2 - timedelta(hours=100)
    date_start_4 = date_start_3 - timedelta(hours=100)

    #DATETIME FORMAT
    times_dict = {
        "range_1":{
            "from_iso": format_time(date_start_1),
            "to_iso": format_time(date_start_0),
        },
        "range_2":{
            "from_iso": format_time(date_start_2),
            "to_iso": format_time(date_start_1),
        },
        "range_3":{
            "from_iso": format_time(date_start_3),
            "to_iso": format_time(date_start_2),
        },
        "range_4":{
            "from_iso": format_time(date_start_4),
            "to_iso": format_time(date_start_3),
        },
    }

    #RETURN RESULT
    return times_dict


