
# Foundations

## Applications of DSP

- Telecommunications
    - telecommunication = transferring information from one location to another
    - telecommunication system = transmitter + channel + receiver
    - Multiplexing
        - using the same shared channel for information transfer from multiple sources to multiple destinations
            - need to use the same channel (say a big fat telephone wire) for all communication (eg: lots of people talking on the phone)
        - use DSP to convert analog signals to digital signals and vice versa. digital signals are easier to multiplex.
            - eg: using a big highway for multiple cars (signal packets) to travel at the same time v/s trying to use a shared pipeline for tranferring different fluids (analog signals)
                - fluid will mix and get contaminated if same channel is used for multiple signals
                - so you need lots of smaller channels to multiplex analog signals
            - Time Division Multiplexing (TDM): Each car (signal) gets to use the entire highway for a specific time slot.
            - Frequency Division Multiplexing (FDM): Each car (signal) gets to use a specific lane (frequency band).
                - radio stations, TV channels
            - Wavelength Division Multiplexing (WDM): Similar to FDM but with different colors of cars (wavelengths).
            - Code Division Multiplexing (CDM): Each car has a unique identifier (code) that allows it to be distinguished from others even if they are in the same lane.
    - compression
        - 8000 samples/sec is very redundant and can be compressed a lot once converted from analog to digital
    - Echo control
        - apparently, there is "echo" in telephone lines where you can hear your own voice after a delay
        - you can use DSP to cancel out the echo
- audio processing
    - music
        - path leading from the musician's microphone to the audiophile's speaker is remarkably long
        - lot and lots of DSP in between
            - eg: noise cancellation, equalization, compression, etc.
            - artificial reverberation
                - adding echo to a sound to make it sound like it was recorded in a large hall instead of a small recording room with noise cancellation
    - speech
        - Speech generation (eg: Siri, Alexa)
            - natural human-computer interface
            - two approaches
                - digital recording
                    - store human voice samples and play them back (eg: announcements in a train station)
                - vocal tract simulation
                    - model the human vocal tract and generate speech from text
                    - text-to-speech (TTS) systems
        - Speech recognition
            - two steps: feature extraction followed by feature matching
- Echo Location
    - Radar (RAdio Detection And Ranging)
        - bounce radio signals off objects to detect their presence, distance, speed, etc.
    - Sonar (SOund Navigation And Ranging)
        - bounce sound waves off objects to detect their presence, distance, speed, etc. in water
    - Reflection seismology
        - find oil and gas deposits underground by bouncing sound waves off the earth's insides
- Image Processing
    - medical imaging
        - X-rays, MRI, CT scans, etc.
    - space
        - make the most of the limited bandwidth available for transmitting images from space probes
    - Commercial Imaging Products (tv, cameras, etc.)
        - compression, enhancement, etc.

## Background on Statistics and Probability Theory

## Analog-to-Digital Conversion (ADC) and Digital-to-Analog Conversion (DAC)

- Quantization
    - (a) = analog signal that is to be quantized
    - sample and hold: (b) = (a) sampled at regular intervals
        - record instantaneous value of (a) at regular intervals
    - ADC: (c) = (b) quantized to a finite number of levels represented in 12 bits
        - 12 bits = 2^12 = 4096 levels
        - maximum quantization error = +- LSB / 2 = +- 1/2 * 1/4096 = +- 1/8192
        - good way to model error random variable as Uniform(-1/2 LSB, 1/2 LSB)
            - error due to quantization is additive
            - fails when the input signal is constant for long time
                - dithering: add small noise to the input signal to break the constant signal 
                    - subtractive dithering: remove the dithering noise back after quantization
    - sampling theorem
        - "proper sampling" has 0 "reconstruction error" from the sampled signal to the original signal
            - sampling rate = r, signal frequency = 0 (for constant DC current) -> proper sampling
            - sampling rate = r, signal frequency = f, f < r/2 -> proper sampling (sampling theorem says so. It is possible to reconstruct the original signal from the samples)
            - sampling rate = r, signal frequency = f, f > r/2 -> improper sampling (aliasing)
                - signal looks like it has a lower frequency than it actually does
                - "double curse": high frequencies are folded back into the lower frequencies and added to them. So both high and low frequencies are corrupted.
                - phase also gets messed up
        - Nyquist frequency = 1/2 * sampling frequency
            - continuous signal can be reconstructed from its samples if the signal has no frequency components above the Nyquist frequency
        - impulse train
            - continuous signal represented as a sum of impulses at regular intervals
            - array of numbers is equivalent to impulse train => only need to study error between impulse train and the original signal
            - use frequency domain to study the error
                - say actual signal has fequencies from [0, 0.33 * sampling_freq], then the impulse train will have infinite copies of it in ranges [n * sampling_freq, (n + 0.5) * sampling_freq] for all n in [0, 0.5, 1, 1.5, ... till infinity]
                    - easy to reconstruct original signal from the impulse train by removing all frequencies above 0.5 * sampling_freq
- Digital to analog conversion
    - simplest method: generate impulse train + low pass filter (remove frequencies > 0.5 * sampling_freq)
        - not practical because t is difficult to generate impulse train in practice
    - practical method: zeroth-order hold
        - hold the value of the sample for the entire duration of the sample resulting in a staircase waveform
        - spectrum of impulse train gets multiplied by function, H(f) = |sin(pi * f / f_s) / (pi * f / f_s)| = |sinc(f / f_s)|
            - equivalent to convolution of impulse train with rectangular pulse with width = sampling interval  // TODO: understand this intuitively
            - sinc function is the Fourier Transform of the rectangular pulse, which gets multiplied with the spectrum of the impulse train
        - reconstruction filter
            - remove frequencies above 0.5 * sampling_freq
            - increase amplitude of the remaining frequencies by 1 / H(f) factor to account for the attenuation by the zeroth-order hold
                - 4 options: (i) ignore it, (ii) design a analog filter with this proerty, (iii) use a fancy multirate technique, (iv) fix in software before applying DAC
    - myth: analog signals contain infinite resolution and hence more information than digital signals
        - not true. They have similar limitations. Analog signals also have: (i) noise (similar to quantization error), and (ii) maximum allowed frequency (similar to Nyquist frequency limitation due to sampling)
- DSP system design
    - (analog input) ---> Antialias Analog filter ---> ADC ---> Digital processing ---> DAC ---> Reconstruciton Analog filter ---> (analog output)
    - antialias filter: remove frequencies above Nyquist frequency that would mess up the sampling process
    - reconstruction filter: remove frequencies above Nyquist frequency and (optionally) zeroth-order hold compensation
- Analog filters for Data Conversion
    - TODO: revise high-schoool physics necessary for understanding analog filters
    - motivations for studying analog filters for software people
        - digital signal processing must be compatible with the analog filters used in the system
        - future of DSP is replacing analog filters with digital filters -> need to understand analog filters to design digital filters
        - DSP filter design often start with an analog filter and then convert to digital
    - crash course on physics of electrical circuits
        - voltage, current, resistance, capacitance, inductance, etc.
        - Ohm's law: V = I * R
        - Kirchoff's laws: (i) sum of currents at a node = 0, (ii) sum of voltages in a loop = 0
        - capacitors and inductors have a frequency-dependent impedance
            - capacitors: Z = 1 / (j * 2 * pi * f * C)
            - inductors: Z = j * 2 * pi * f * L
        - RC filter
            - low pass filter
            - cutoff frequency = 1 / (2 * pi * R * C)
        - RL filter
            - high pass filter
            - cutoff frequency = R / (2 * pi * L)
        - RLC filter
            - band pass filter
            - cutoff frequencies = 1 / (2 * pi * R * C) and R / (2 * pi * L)



# References

- [The Scientist and Engineer's Guide to Digital Signal Processing](https://ia801301.us.archive.org/23/items/GuideToDigitalSignalProcessing/Guide%20To%20Digital%20Signal%20Processing.pdf)
- [Fourier Transforms and the Fast Fourier Transform (FFT) Algorithm](https://www.cs.cmu.edu/afs/andrew/scs/cs/15-463/2001/pub/www/notes/fourier/fourier.pdf)