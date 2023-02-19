def format_time(string_num):
    """
    Adds a leading zero to a string of numbers if the length is less than 2.
    """
    if len(string_num) < 2:
        return "0" + string_num
    else:
        return string_num


def format_no(string_num):
    string_num = str(string_num)
    """
    将不足10位的字符串补足前导0，使其长度达到10位。

    Args:
    string -- 要处理的字符串，可以是数字字符串或其他字符串

    Returns:
    补足前导0后的字符串，如果原字符串已经是10位或更长的字符串，则返回原字符串。
    """
    if len(string_num) >= 10:
        return string_num
    else:
        return "0" * (10 - len(string_num)) + string_num


def format_score(num):
    num = str(num)
    """
        将不足3位的字符串补足前导0，使其长度达到3位。

        Args:
        string -- 要处理的字符串，可以是数字字符串或其他字符串

        Returns:
        补足前导0后的字符串，如果原字符串已经是3位或更长的字符串，则返回原字符串。
        """
    if len(num) >= 3:
        return str(num)
    else:
        return "0" * (3 - len(num)) + str(num)
