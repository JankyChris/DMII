import numpy as np
import matplotlib.pyplot as plt

# a)

def exp_euler(x0, f, tau, n):
    x = np.zeros(n+1)
    x[0] = x0

    for i in range(n):
        x[i+1] = x[i] + tau*f(x[i])

    return x

# b)

def heun(x0, f, tau, n):
    x = xs = np.zeros(n+1)
    x[0] = xs[0] = x0

    for i in range(n):
        xs[i+1] = x[i] + tau*f(x[i])
        x[i+1] = x[i] + 0.5*tau*(f(x[i]) + f(x[i+1]))

    return x

# c)

# x'(t) = -x, 0 < t <= T = 1.5,
# x(0) = 1

N = 1000
T = 1.5
err_euler = []
err_heun = []
x0 = 1

def f(x):
    return -x

for n in range(2,N+1):
    tau = T/n
    t = np.linspace(0, T, n+1)

    x_true = np.exp(-t)
    x_euler = exp_euler(x0, f, tau, n)
    x_heun = heun(x0, f, tau, n)

    err_euler.append(np.max(np.absolute(x_true - x_euler)))
    err_heun.append(np.max(np.absolute(x_true - x_heun)))

def plot_results(err_1, err_2):
    n = np.linspace(1, len(err_1), len(err_1))

    plt.plot(n, err_1, label='Euler')
    plt.plot(n, err_2, label='Heun')
    plt.xlabel('n')
    plt.ylabel('max error')
    plt.title("Comparison of Explicit Euler and Heun's Method")
    plt.yscale('log')
    plt.legend()
    plt.show()

plot_results(err_euler, err_heun)
