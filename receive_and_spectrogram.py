#
#   PLUTO CONTINUOUS CAPTURE TEST PROGRAM AND SIGMF FORMATING
#
#   Alejandro Manuel López Gómez
#
#   .sigmf capture files of IQ values of length multiple of FFT length for each buffer capture
#   captured samples are plotted in spectrogram.

import adi
import pickle
import numpy as np
import datetime as dt
from sigmf import SigMFFile
import matplotlib.pyplot as plt

def main():
    # sigmf metadata
    author = 'A.M.L.G'
    version =  '1.0.0'
    data_file = 'capture.sigmf-data'
    meta_file = 'capture.sigmf-meta'
    description = 'IQ Data Capture from PlutoSDR at 100 MHz'

    # plutoSDR capture parameters
    sample_rate = 1e6
    center_frequency = 100e6
    number_samples = pow(2,14)

    sdr = set_pluto(center_frequency,number_samples,sample_rate)
    memory = capture(sdr)
    convert_and_save_data(memory,data_file,meta_file,sample_rate,center_frequency,number_samples,author,description,version)
    create_spectrogram(memory,sample_rate,number_samples)

def set_pluto(center_frequency,number_samples,sample_rate):
    sdr = adi.Pluto('ip:192.168.2.1')
    sdr.gain_control_mode_chan0 = 'fast_attack'
    sdr.rx_lo = int(center_frequency)
    sdr.sample_rate = int(sample_rate)
    sdr.rx_rf_bandwidth = int(number_samples)
    sdr.rx_buffer_size = int(number_samples)
    return sdr

def capture(sdr):
    try:
        print("Capturing... Stop code (Ctrl + C) for results")
        memory = []
        while True:
            samples = sdr.rx()
            memory.extend(samples)
    except KeyboardInterrupt:
        pass
    return memory

def convert_and_save_data(memory_128,data_file,meta_file,sample_rate,center_frequency,number_samples,author,description,version):
    print("Parsing and saving data...\nData length:",len(memory_128),"\nNumber of segments:",len(memory_128)/number_samples, "\nFile length in seconds:",(number_samples/sample_rate)*(len(memory_128)/number_samples))
    memory_64 = np.array(memory_128).astype(np.complex64)
    memory_64.tofile(data_file)

    meta = SigMFFile(
        data_file=data_file,
        global_info={
            SigMFFile.DATATYPE_KEY: 'cf32_le',
            SigMFFile.SAMPLE_RATE_KEY: sample_rate,
            SigMFFile.AUTHOR_KEY: author,
            SigMFFile.DESCRIPTION_KEY: description,
            SigMFFile.VERSION_KEY: version
        }
    )

    meta.add_capture(0, metadata={
        SigMFFile.FREQUENCY_KEY: center_frequency,
        SigMFFile.DATETIME_KEY: dt.datetime.utcnow().isoformat() + 'Z'
    })

    meta.tofile(meta_file)

def create_spectrogram(memory,sample_rate,fft_size):
    print("Creating and plotting spectrogram...")
    num_rows = len(memory)//fft_size
    spectrogram = np.zeros((num_rows,fft_size))
    for i in range(num_rows):
        spectrogram[i, :] = 20*np.log10(np.abs(np.fft.fftshift(np.fft.fft(memory[i*fft_size:(i+1)*fft_size]))))

    fig, ax = plt.subplots()
    im = ax.imshow(spectrogram, aspect='auto', extent=[sample_rate/-2/1e6, sample_rate/2/1e6, 0, (fft_size/sample_rate)*(len(memory)/fft_size)])
    fig.colorbar(im, orientation='vertical')
    ax.set_title("Spectrogram")
    ax.set_xlabel("Frequency [MHz]")
    ax.set_ylabel("Time [s]")
    plt.show()

if __name__ == "__main__":
    main()