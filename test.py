import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
t = np.linspace(0, 1, 500, endpoint=False)
x = np.sin(2*np.pi*t*10)
s = np.fft.ifft(np.fft.fft(x) * np.fft.fft(x))
plt.plot(x)
plt.show()