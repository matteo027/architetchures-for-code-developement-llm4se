def decimal_to_Octal(deciNum: int) -> int:
    if not isinstance(deciNum, int):
        raise TypeError("Input must be an integer")
    if deciNum < 0:
        deciNum = abs(deciNum)
    if deciNum > 255:
        raise ValueError("Input must be between 0 and 255")

    octalNum = ""
    while deciNum > 0:
        octalNum = str(deciNum % 8) + octalNum
        deciNum = deciNum // 8
    return int(octalNum)