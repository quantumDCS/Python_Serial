def format_time(string_num):
    """
    Adds a leading zero to a string of numbers if the length is less than 2.
    """
    if len(string_num) < 2:
        return "0" + string_num
    else:
        return string_num


