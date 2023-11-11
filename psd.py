#
#   PLUTO RX PSD PLOT PROGRAM
#
#   Alejandro Manuel López Gómez
#

import adi
import numpy as np
import matplotlib.pyplot as plt

# gain = 70                                     # dB (for manual gain control mode, ignored if other mode is set)
sample_rate = 1e6
center_frequency = 100e6
number_samples = 1e6

sdr = adi.Pluto('ip:192.168.2.1')               # initialize PlutoSDR from API call to IP address

sdr.gain_control_mode_chan0 = 'fast_attack'
# sdr.rx_hardwaregain_chan0 = int(gain)         # only uncomment if manual mode present
sdr.rx_lo = int(center_frequency)
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(number_samples)       # rx() filter width
sdr.rx_buffer_size = int(number_samples)        # per call to rx() function buffer size

samples = sdr.rx()                              # receive samples from Pluto

psd = 20*np.log10(np.abs(np.fft.fftshift(np.fft.fft(samples))))
f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))

plt.plot(f/1e6, psd)
plt.title("Power Spectral Density")
plt.xlabel("Frequency [MHz]")
plt.ylabel("PSD [dB]")
plt.show()
