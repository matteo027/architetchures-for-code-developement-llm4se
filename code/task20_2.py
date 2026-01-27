from typing import List
import math

def Strongest_Extension(class_name: str, extensions: List[str]) -> str:
    """Finds the strongest extension for a given class name based on character counts.

    The strength of an extension is defined as the count of uppercase letters
    minus the count of lowercase letters.
    """
    max_strength = -math.inf
    strongest_extension_name = ""

    for extension in extensions:
        CAP = 0
        SM = 0
        for char in extension:
            if 'A' <= char <= 'Z':
                CAP += 1
            elif 'a' <= char <= 'z':
                SM += 1

        strength = CAP - SM

        if strength > max_strength:
            max_strength = strength
            strongest_extension_name = extension

    return f"{class_name}.{strongest_extension_name}"
