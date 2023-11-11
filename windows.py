#
#   PLUTO RADAR TEST
#
#   Alejandro Manuel López Gómez
#
#   Noise generation and plotting via PlutoSDR.
#

import adi
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal.windows as windows

def main():
    N = 1024
    hamm = np.fft.fftshift(np.fft.fft(windows.hamming(N)))
    hann = np.fft.fftshift(np.fft.fft(windows.hann(N)))
    black = np.fft.fftshift(np.fft.fft(windows.blackman(N)))
    bharris = np.fft.fftshift(np.fft.fft(windows.blackmanharris(N)))

    plt.plot(10*np.log10(abs(black)**2))
    plt.show()
if __name__ == "__main__":
    main()