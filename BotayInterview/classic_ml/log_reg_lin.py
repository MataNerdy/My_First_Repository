import matplotlib.pyplot as plt
import numpy as np

w = np.array([-1, 2])
b = 0.5

x1 = np.linspace(-2, 2, 100)
x2 = -(w[0] * x1 + b) / w[1]

plt.plot(x1, x2, 'k--', label='Решающая граница (линейная)')
plt.xlabel('x1')
plt.ylabel('x2')
plt.legend()
plt.grid(True)
plt.show()