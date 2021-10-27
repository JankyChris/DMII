import numpy as np

# a)

def exp_euler(x0, f, tau, n):
    x = np.zeros(n+1)
    x[0] = x0

    for i in range(n):
        x[i+1] = x[i] + tau*f(x[i])

    return x

# b)

def heun(x0, f, tau, n):
    x = np.zeros(n+1)
    x[0] = x0

# c)