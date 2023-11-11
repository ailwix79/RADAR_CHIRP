#
#   PLUTO TX PULSE GENERATION TEST
#
#   Alejandro Manuel López Gómez
#
#   Noise generation and plotting via PlutoSDR.
#

import adi
import numpy as np
import matplotlib.pyplot as plt

def main():
    gain = 0
    steps = 1000
    amplitude = 1
    sample_rate = 1e6
    number_samples = 1e6
    center_frequency = 433.92e6

    sdr = set_pluto(center_frequency,sample_rate,gain)
    generate_and_transmit_signal(sdr,center_frequency,number_samples,sample_rate,amplitude,steps)

def set_pluto(center_frequency,sample_rate,gain):
    sdr = adi.Pluto("ip:192.168.2.1")
    sdr.sample_rate = int(sample_rate)
    sdr.tx_rf_bandwidth = int(sample_rate)
    sdr.tx_lo = int(center_frequency)
    sdr.tx_hardwaregain_chan0 = gain        # Increase tx power, from -90 to 0 dB
    return sdr

def generate_and_transmit_signal(sdr,center_frequency,number_samples,sample_rate,amplitude,steps):
    t = np.arange(number_samples)/sample_rate
    frequencies = np.linspace(sample_rate/-2,sample_rate/2,steps)

    print("Transmitting signal...")
    sdr.tx_destroy_buffer()
    for i in range(steps):
        samples = amplitude*np.exp(-2.0j*np.pi*frequencies[i]*t)*(2**14)
        sdr.tx(samples)

if __name__ == "__main__":
    main()