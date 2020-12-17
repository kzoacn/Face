from math import log
from math import sqrt

def fac(n):
    if n==0: return 1
    return fac(n-1)*n
def B(n,t):
    return n*log(t/(sqrt(n)/2),2)+n/2*log(3.14,2)-log(fac(n//2),2)
def E(n,t):
    return n*(-1.3)-B(n,t)

print(E(128,6))
