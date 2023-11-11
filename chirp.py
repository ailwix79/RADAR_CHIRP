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
from scipy.signal import chirp
from scipy.constants import c

def main():
    # maximum unambiguous range (km)
    Rmax = 10e3
    # pulse repetition frequency (Hz). Number of pulses per second.
    prf = c/2*Rmax
    # duty cycle (0-1). Percentage of pulses vs empty space per second.
    duty_cycle = 0.20
    # sample rate (Hz). Sampling frequency, number of samples per second.
    sample_rate = int(1e6)
    # number of samples.
    number_samples = int(2e6)
    create_chirps(duty_cycle,sample_rate,number_samples,prf)

def create_chirps(duty_cycle,sample_rate,number_samples,prf):
    # pulse width (samples). Width of an individual pulse.
    pulse_width = int(duty_cycle*(number_samples/prf))
    # blank width (samples). Spacing between pulses.
    blank_width = int((1-duty_cycle)*(number_samples/prf))
    s = np.zeros(number_samples)
    t = np.linspace(0,pulse_width,pulse_width)
    c = chirp(t,f0=100,t1=pulse_width,f1=10,method='linear')

    for i in range(0,int(prf)):
        s[int(i*(pulse_width+blank_width)):int((i+1)*pulse_width+i*blank_width)] = c

    s = s - np.mean(s)

    plt.plot(np.linspace(0,int(number_samples/sample_rate),number_samples),s)
    plt.xlabel("Time [s]")
    plt.ylabel("Normalized signal")
    plt.title("Radar chirp pulse generation")
    plt.show()

if __name__ == "__main__":
    main()