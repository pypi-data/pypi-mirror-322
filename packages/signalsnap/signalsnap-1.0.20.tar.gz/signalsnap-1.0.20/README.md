# SignalSnap: Signal Analysis In Python Made Easy 
by M. Sifft, A. Ghorbanietemad and D. Hägele

We present a fast Python toolbox for higher-order spectral analysis of time series. The usual second-order 
power spectrum and its higher-order generalization - so-called bi- and trispectra - are efficiently calculated 
on any platform. The toolbox supports GPU acceleration using the ArrayFire library. The treatment of large datasets 
is not limited by available RAM. We were able to process 11.6 GB of data (given in the hdf5 format) within just one 
minute to obtain a power spectrum with a one-million-point resolution using a five-year-old Nvidia GeForce GTX 1080. 
Similarly, 1000x1000 points of a trispectrum were obtained from processing 3.3 GB of data per minute.

Here are a few outstanding features of SignalSnap:
* Errors of spectral values are automatically calculated ([beginners example](Examples/Calculating%20Spectra%20from%20Numpy%20Array.ipynb), [example](Examples/Higher-Order%20Example:%20Mixing%20of%20Gaussian%20Noise.ipynb))
* Support for just-in-time import from hdf data (dataset does not have to fit in RAM) ([example](Examples/Calculating%20Polyspectra%20from%20Measurement.ipynb))
* Functions for conversion of Numpy array to hdf data is also provided ([example](Examples/Conversion%20of%20CSV%20to%20h5.ipynb))
* Functions for storing and loading calculated spectra together with metadata ([example](Examples/Storing%20and%20Loading%20Spectra.ipynb)) 
* Correlations between two time series can be calculated ([example](Examples/Correlations%20Between%20Two%20Time%20Series.ipynb))
* All calculation can be performed on GPU (NVidia and AMD) (see Arrayfire) ([example](Examples/Comparing%20CPU%20to%20GPU.ipynb))
* Advanced plotting options for two-dimensional higher-order spectra (as seen in most examples)
* Usage of unbiased estimators for higher-order cumulants (see Literature below)
* Efficient implementation of the confined Gaussian window for an optimal RMS time-bandwidth product (see Literature below)
* Special functions for the verification of the stationarity of a signal ([example](Examples/Testing%20the%20Stationarity%20of%20a%20Signal.ipynb))
* Spectra can be calculated from timestamps instead of a continuous trace ([example](Examples/Calculating%20Polyspectra%20from%20Timestamps.ipynb)) 

## Installation
SignalSnap is available on `pip` and can be installed with 
```bash
pip install signalsnap
```

### Installation of Arrayfire
A comprehensive installation guide for Linux + NVidia GPU can be found [here](https://github.com/MarkusSifft/SignalSnap/wiki/Installation-Guide). 
For GPU calculations the high performance library Arrayfire is used. The Python wrapper ([see here](https://github.com/arrayfire/arrayfire-python)) 
is automatically installed when installing SignalSnap, however, [ArrayFire C/C++ libraries](https://arrayfire.com/download) need to be installed separately. 
Instructioins can be found can be found [here](https://github.com/arrayfire/arrayfire-python) and [here](https://arrayfire.org/docs/installing.htm#gsc.tab=0).


## Documentation
A documentation of SignalSnap's functions can be found [here](https://markussifft.github.io/SignalSnap/). 

### Examples
Examples for every function of the package are currently added to the folder Examples. Here are a few lines 
to get you started. We will generate some white noise as signal/dataset and store it as Numpy array called `y`.

```python
from signalsnap import SpectrumCalculator, SpectrumConfig, PlotConfig
import numpy as np

rng = np.random.default_rng()

# ------ Generation of white noise -----
f_unit = 'kHz'
fs = 10e3  # sampling rate in kHz
N = 1e5  # number of points
t = np.arange(N) / fs  # unit is automatically chosen to be 1/f_unit = ms
y = rng.normal(scale=1, size=t.shape)
```

Now we creat a spectrum object and feed it with the data. This object will store the dataset, 
later the spectra and errors, all freely chosen variables and contains 
the methods for calculating the spectra, plotting and storing.

```python
config = SpectrumConfig(data=y, delta_t=1/fs, f_unit='kHz', 
                        spectrum_size=128, order_in=[2], 
                        f_max=5e3, backend='cpu')
spec = SpectrumCalculator(config)
f, s, serr = spec.calc_spec()
```

```
T_window: 2.540e-02 ms
Maximum frequency: 5.000e+03 kHz
```
![data in first window](Examples/plots/example_window.png)

The output will show you the actual length of a window (in case your T_window is not a multiple of 1/fs), the maximum 
frequency (Nyquist frequency) and the number of point of the calculated spectrum. The data points in the first window 
are plotted, so you can verify the window length (which is also given in points by chunk shape). The function will 
return `f` the frequencies at which the spectrum has been calculated, `s` the spectral values, and `serr` the error 
of the spectra value (1 sigma).

Visualization of the results is just as easy as the calculation.

```python
plot_config = PlotConfig(plot_orders=[2], plot_f_max=5e3/2)
fig = spec.plot(plot_config)
```
![power spectrum of the data](Examples/plots/example_s2.png)

Besides the power spectrum (blue line) the error bands (1 to 5 sigma) are shown as grey lines in the plot.
Now, we can even verify that we are dealing with true Gaussian noise by calculating the higher-order spectra of the time
series.

## Why higher-order spectra?
Higher-order spectra contain additional information that is not contained within a power spectrum. The toolbox is 
capable of calculating the third- and four-order spectrum (also called bi- and trispectrum, respectively). These have 
the following properties:
* Spectra beyond second order are not sensitive to Gaussian noise.
* Bispectrum: shows contributions whenever the phase of two frequencies and their sum are phase correlated (e.g. by 
mixing two signals)
* Trispectrum: can be interpreted as intensity correlation between two frequencies

Let's calculate all spectra up to fourth order of the dataset above and verify that the signal does not deviate 
significantly from Gaussian noise using the first property (has no significant higher-order contributions). We 
only have to change the `order_in` argument:

```python
config = SpectrumConfig(data=y, delta_t=1/fs, f_unit='kHz', 
                        spectrum_size=128, order_in='all', 
                        f_max=5e3, backend='cpu')
spec = SpectrumCalculator(config)
f, s, serr = spec.calc_spec()
```

Plotting can also be done as before by changing the `order_in` argument:
```python
plot_config = PlotConfig(plot_orders=[2,3,4], plot_f_max=5e3/2, green_alpha=0)
fig = spec.plot(plot_config)
```
![polyspectra of the data](Examples/plots/example_poly_no_errors.png)

Now, the third-and fourth-order spectra (S3 and S4) are visible. Just like the power spectrum they are noisy.
To decide which of the fluctuations are significant we need a way of displaying errors in the two-dimensional
plots. Here, errors are visualized be overlaying a green color on the spectral contributions which deviate from 
zero less than a certain number of standard deviations. 

```python
plot_config = PlotConfig(plot_orders=[2,3,4], plot_f_max=5e3/2, sigma=3)
fig = spec.plot(plot_config)
```
![polyspectra of the data](Examples/plots/example_poly.png)

Clearly, all higher-order contributions are nothing but noise and we have, therefore, verifed that our 
original dataset was Gaussian noise (and even white noise due to the flat power spectrum).

## Support
The development of the SignalSnap package is supported by the working group Spectroscopy of Condensed Matter of the 
Faculty of Physics and Astronomy at the Ruhr University Bochum.

## Dependencies
For the package multiple libraries are used for the numerics and displaying the results:
* NumPy
* SciPy
* MatPlotLib
* tqdm
* Numba
* h5py
* ArrayFire

## Literature
Unbiased estimators are used for the calculation of higher-order cumulants. Their derivation can be found in
[this paper](https://arxiv.org/abs/2011.07992). An explanation for how the spectra are calculated can be found in
Appendix B of [this paper](https://doi.org/10.1103/PhysRevResearch.3.033123).