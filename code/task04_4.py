from typing import *

def decimal_to_Octal(deciNum: int) -> int:
    oct_str = oct(deciNum)
    oct_str_without_prefix = oct_str[2:]
    return int(oct_str_without_prefix, 8)