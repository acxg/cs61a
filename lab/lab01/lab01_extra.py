"""Optional questions for Lab 1"""

# While Loops

def falling(n, k):
    """Compute the falling factorial of n to depth k.

    >>> falling(6, 3)  # 6 * 5 * 4
    120
    >>> falling(4, 3)  # 4 * 3 * 2
    24
    >>> falling(4, 1)  # 4
    4
    >>> falling(4, 0)
    1
    """
    mul = 1
    while k > 0:
        mul *= n
        n -= 1
        k -= 1
    return mul

def double_eights(n):
    """Return true if n has two eights in a row.
    >>> double_eights(8)
    False
    >>> double_eights(88)
    True
    >>> double_eights(2882)
    True
    >>> double_eights(880088)
    True
    >>> double_eights(12345)
    False
    >>> double_eights(80808080)
    False
    """
    count = 0
    while n/10 > 0:
        if n%10 == 8 and count == 0:
            count = 1
        elif n % 10 == 8 and count == 1:
            return True
        else:
            count = 0
        n //= 10
    if count == 1 and n == 8: 
        return True
    else:
        return False  
