from typing import List

    def decimal_to_Octal(deciNum: int) -> int:

    # 1. Initialize an empty string to store the octal representation.
    octal_str = ""

    # 2. While the decimal number is greater than zero, perform the following steps:
    while deciNum > 0:
        # a. Calculate the remainder of the division by 8.
        remainder = deciNum % 8
        # b. Append the remainder to the octal representation string.
        octal_str = str(remainder) + octal_str
        # c. Divide the decimal number by 8.
        deciNum //= 8

    # 3. Convert the octal representation string to an integer.
    octal_num = int(octal_str)

    return octal_num