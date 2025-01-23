from typing import Tuple
from typing import Optional


def int_to_id(number: int) -> str:
    chars: str = '0123456789abcdefghijklmnopqrstuvwxyz'
    base: int = len(chars)
    
    if number < 0:
        raise ValueError("Input must be a non-negative integer")
    
    # Convert to base-36
    result: list[str] = []
    while number > 0:
        number, remainder = divmod(number, base)
        result.append(chars[remainder])
    
    # Pad with '0' if necessary to reach minimum length of 3
    while len(result) < 3:
        result.append('0')
    
    # Raise error if result is longer than 5 characters
    if len(result) > 5:
        raise ValueError("Input number is too large (results in more than 5 characters)")
    
    # Reverse the list and join into a string
    return ''.join(reversed(result))

def id_to_int(id: str) -> int:
    chars: str = '0123456789abcdefghijklmnopqrstuvwxyz'
    base: int = len(chars)
    
    if not 3 <= len(id) <= 5:
        raise ValueError("ID must be between 3 and 5 characters long")
    
    if not all(c in chars for c in id):
        raise ValueError("ID contains invalid characters")
    
    result: int = 0
    for char in id:
        result = result * base + chars.index(char)
    
    return result
