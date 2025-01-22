import math

def Tohop(n, k):
    """
    Tính tổ hợp C(n, k) = n! / (k! * (n-k)!)
    """
    if n < 0 or k < 0 or k > n:
        raise ValueError("N và K phải là số dương và K <= N.")
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def Chinhhop(n, k):
    """
    Tính chỉnh hợp A(n, k) = n! / (n-k)!
    """
    if n < 0 or k < 0 or k > n:
        raise ValueError("N và K phải là số dương và K <= N.")
    return math.factorial(n) // math.factorial(n - k)


def Hoanvi(n):
    """
    Tính hoán vị P(n) = n!
    """
    if n < 0:
        raise ValueError("N phải là số dương.")
    return math.factorial(n)
