import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(0,20, 10000)
y = np.sin(x)

coefs = np.polyfit(x, y, 11)
func = np.poly1d(coefs)
y_ = func(x)


fig, ax = plt.subplots()
ax.plot(x,y)
ax.plot(x,y_, 'r')
plt.show()
