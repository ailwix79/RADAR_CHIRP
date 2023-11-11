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
from scipy.signal import chirp
from scipy.constants import c,pi

def main():
    # maximum and minimum chirp frequencies
    fmax = 20e3
    fmin = 10e3
    # initial phase at t=0 of chirp signal
    initial_phase = pi
    # sampling rate. SHOULD BE GREATER OR EQUAL TO 2*fmax
    sample_rate = int(1e6)
    # maximum unambiguous range (m)
    Rmax = 15e3
    # range resolution (m)
    Rres = 150
    # pulse repetition frequency (Hz). Number of pulses per second. Also doppler resolution
    prf = c/(2*Rmax)
    # pulse repetition period (microseconds).
    prt = 1e6/prf
    # pulse width (seconds).
    tau = (2*Rres)/c
    # magnification (for plotting purposes)
    tau *= 1e6
    tau = nextpow2(tau)
    # duty cycle
    duty_cycle = (tau*100)/(tau+prt)
    # signal to noise ratio
    snr_db = 10
    # amplitude attenuation
    attenuation = 1
    # delay (samples)
    delay = int(0.75e5)
    doppler = 0

    t,x1 = create_chirps(tau,sample_rate,fmax,fmin,initial_phase)
    x_d = add_delay_and_doppler(x1,delay,doppler)
    x2 = add_awgn(x_d,attenuation,snr_db)
    plot_autocorr(sample_rate,x1,x2)
    plot_fft(sample_rate, t, x1, fmin, fmax)
    plot_chirp(t,x1)

def plot_chirp(t,x):
    plt.plot(t,x)
    plt.xlabel("Time [s]")
    plt.ylabel("Signal")
    plt.title("CHIRP signal")
    plt.grid()
    plt.show()
def plot_fft(sample_rate,t,x,fmin,fmax):
    X = np.fft.fftshift(np.fft.fft(x*scipy.signal.windows.hamming(len(x))))
    X *= 1/np.max(X)
    plt.plot(np.linspace(sample_rate/-2,sample_rate/2,len(x)),10*np.log10(abs(X)**2))
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("PSD [dB]")
    plt.title("FFT of CHIRP signal")
    plt.xlim([0,sample_rate/2])
    plt.axvline(x=fmin, color='r',linestyle='-.')
    plt.axvline(x=fmax, color='r',linestyle='-.')
    plt.xlim([fmin-fmin/2,fmax+fmin/2])
    plt.grid()
    plt.show()

def add_delay_and_doppler(x,delay,doppler):
    n = len(x)
    x_d = np.pad(x,(delay,0),'constant')
    x_d = x_d[0:n]
    x_dd = x_d*np.exp((1j*2*pi*doppler)/len(x_d))
    return x_dd

def add_awgn(x,attenuation,snr_db):
    return attenuation*x + (1/np.sqrt(10**(snr_db/10)))*(np.random.randn(len(x)) + 1j * np.random.randn(len(x)))/np.sqrt(2)

def plot_autocorr(sample_rate,x1,x2):
    w = scipy.signal.windows.hamming(max(len(x1),len(x2)))
    x1 *= w
    x2 *= w
    s = scipy.signal.correlate(x1,x2,mode='same',method='auto')
    s *= 1/np.max(s)
    s = s[0:(len(s)//2)+1]

    n = np.linspace(0,len(x1)//2,len(s))
    plt.plot(n,10*np.log10(abs(np.flip(s))**2))
    plt.title("Auto correlation of CHIRP signal")
    plt.xlabel("Samples")
    plt.ylabel("PSD [dB]")
    plt.grid()
    plt.show()
def create_chirps(tau,sample_rate,fmax,fmin,initial_phase):
    t = np.linspace(0,tau,int(tau*sample_rate))
    x = np.sin(initial_phase+2*pi*((-fmin*fmax*tau)/(fmax-fmin))*np.log(1-((fmax-fmin)/(fmax*tau))*t))
    return t,x

def nextpow2(N):
    n = 1
    while n < N: n *= 2
    return n

if __name__ == "__main__":
    main()