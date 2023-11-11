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
import scipy.signal.windows
from scipy.constants import c,pi

def main():
    # INITIAL PARAMETERS
    Rres = 150
    Rmax = 15e3

    # chirp signal parameters
    fmax = 1e9
    fmin = 1e3
    initial_phase = pi
    # sample rate (Hz)
    sample_rate = 1e12
    # pulse width (seconds)
    tau = (2*Rres)/c
    # pulse repetition frequency (Hz)
    prf = c/(2*Rmax)
    # pulse repetition period (seconds).
    prt = 1/prf

    snr_db = 10
    # amplitude attenuation
    attenuation = 1
    # delay (samples)
    delay = int(1e5)
    doppler = 30

    print("Pulse Repetition Time [us]: " + str(prt*1e6))
    print("Pulse Repetition Time [samples]: " + str(prt*sample_rate))

    t,x_ref = create_chirps(tau,sample_rate,fmax,fmin,initial_phase)
    x_eco = add_awgn(add_delay_and_doppler(x_ref,delay,doppler),attenuation,snr_db)

    s = batch(sample_rate,x_ref,x_eco)

def batch(sample_rate,x_ref,x_eco):
    Y = np.zeros((((len(x_ref))//2)+1,((len(x_ref))//2)+1))

    for doppler in range(0,((len(x_ref))//2)+1):
        x_test = x_ref*np.exp((2j*pi*doppler)/len(x_ref))
        s = xcorr(x_test,x_eco)
        Y[i] = s

def xcorr(x1,x2):
    # s = scipy.signal.correlate(x1,x2,mode='same',method='auto')
    s = np.fft.ifftshift(np.fft.ifft((np.fft.fft(x1)*np.fft.fft(np.flip(x2)))))
    s *= 1/np.max(s)
    s = s[0:(len(s)//2)+1]
    return s

def create_chirps(tau,sample_rate,fmax,fmin,initial_phase):
    N = nextpow2(tau*sample_rate)
    t = np.linspace(0,tau,N)
    x = np.sin(initial_phase + 2*pi*((-fmin*fmax*tau)/(fmax-fmin))*np.log(1-((fmax-fmin)/(fmax*tau))*t))
    x *= scipy.signal.windows.hann(len(x))

    print("Pulse Width [us]: "+ str(N*1e6/sample_rate))
    print("Pulse Width [samples]: "+ str(N))
    return t,x

def nextpow2(N):
    n = 1
    while n < N: n *= 2
    return n

def add_delay_and_doppler(x,delay,doppler):
    n = len(x)
    x_d = np.pad(x,(delay,0),'constant')
    x_d = x_d[0:n]
    x_dd = x_d*np.exp((1j*2*pi*doppler)/len(x_d))
    return x_dd

def add_awgn(x,attenuation,snr_db):
    return attenuation*x + (1/np.sqrt(10**(snr_db/10)))*(np.random.randn(len(x)) + 1j * np.random.randn(len(x)))/np.sqrt(2)

def plot_chirp(t,x):
    plt.plot(t*1e6,x)
    plt.xlabel('Time [us]')
    plt.ylabel('Signal')
    plt.title('CHIRP Signal')
    plt.show()

if __name__ == "__main__":
    main()