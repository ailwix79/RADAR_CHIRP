#
#   PLUTO RX SPECTROGRAM TEST PROGRAM (PROOF OF CONCEPT)
#
#   Alejandro Manuel López Gómez
#
#   Spectgrogram python script which performs fft length batches and plots a time frequency map.
#

import adi
import numpy as np
import matplotlib.pyplot as plt

def main():
    fft_size = 1024
    sample_rate = 1e6
    center_frequency = 100e6
    number_samples = 250000

    sdr = set_pluto(center_frequency,number_samples,sample_rate)
    spectrogram = process_samples(sdr,number_samples,fft_size)
    draw(spectrogram,sample_rate,number_samples)

def set_pluto(center_frequency,number_samples,sample_rate):
    sdr = adi.Pluto('ip:192.168.2.1')
    sdr.gain_control_mode_chan0 = 'fast_attack'
    sdr.rx_lo = int(center_frequency)
    sdr.sample_rate = int(sample_rate)
    sdr.rx_rf_bandwidth = int(number_samples)
    sdr.rx_buffer_size = int(number_samples)
    return sdr

def draw(spectrogram,sample_rate,number_samples):
    fig, ax = plt.subplots()
    im = ax.imshow(spectrogram, aspect='auto', extent=[sample_rate/-2/1e6, sample_rate/2/1e6, 0, number_samples/sample_rate])
    fig.colorbar(im, orientation='vertical')
    ax.set_title("Spectrogram")
    ax.set_xlabel("Frequency [MHz]")
    ax.set_ylabel("Time [s]")
    plt.show()

def process_samples(sdr,number_samples,fft_size):
    samples = sdr.rx()                            # receive samples from Pluto
    num_rows = number_samples//fft_size         # number of rows
    spectrogram = np.zeros((num_rows,fft_size))  # initial 2d matrix with zeros for spectrogram
    for i in range(num_rows):
        spectrogram[i, :] = 20*np.log10(np.abs(np.fft.fftshift(np.fft.fft(samples[i*fft_size:(i+1)*fft_size]))))
    return spectrogram

if __name__ == "__main__":
    main()