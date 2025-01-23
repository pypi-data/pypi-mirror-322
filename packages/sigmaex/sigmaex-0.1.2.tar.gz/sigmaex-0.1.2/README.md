# SigmaEx
<img src="https://github.com/lmytime/sigmaex/blob/main/icon.jpg?raw=true" alt="SigmaEx Logo" style="width:100px"></img>

SigmaEx is a Python package for analyzing and visualizing the Gaussian distribution of data arrays. It allows for sigma clipping, histogram analysis, and Gaussian fitting, with a variety of modes for customized data selection.

SigmaEx is optimized for the following cases:
- Estimate the global background of an astronomical image
- Estimate the pixel-to-pixel noise of an astronomical image
- Modeling the distribution of a series of Gaussian-like data

<img src="https://github.com/lmytime/sigmaex/blob/main/sigmaex.jpg?raw=true" alt="Example Output of SigmaEx"></img>

## Features

- **Sigma Clipping**: Removes outliers from the data based on a given sigma threshold.
- **Gaussian Fit**: Fits a Gaussian distribution to the sigma-clipped data and extracts parameters like mean (μ), standard deviation (σ), and amplitude (A).
- **Histogram Generation**: Creates histograms of the data, with options for customized binning and selection modes.
- **Customizable Modes**: Choose from various modes for how the data should be processed, such as positive, negative, or based on mean/median/standard deviation thresholds.
- **Support for FITS and TIFF files**: Load data from FITS and TIFF files for analysis.
- **Plotting**: Generates publication-quality plots of the data histogram and fitted Gaussian.

## Installation

You can install the required dependencies via pip:

```bash
pip install sigmaex
```

# Usage

## Overview

`sigmaex` is a Python package designed for analyzing and fitting Gaussian distributions to data arrays, with features like sigma clipping and customizable histogram analysis. This document outlines how to use the package via the command-line interface (CLI) and how to generate plots and statistics for your data.

## Python Package

```python
from sigmaex import SigmaEx

# read data from fits file
sigmx = SigmaEx.from_fits("test.fits", ext=0)
# Or load any numpy array data
sigmx = SigmaEx(array)

# Plot the result
sigmx.plot()
# Print the result
print(sigmx)

```

## Command-Line Interface (CLI)

### Syntax

To run the package from the command line, use the following syntax:

```sh
sigmaex <data_file> [options]
```

Where `<data_file>` is the path to the input data file (either `.fits` or `.tiff` format).

### Available Options

- `-s, --sigma`: The number of standard deviations for sigma clipping. Default is `3`.
  
  Example:
  -s 5

- `-m, --mode`: The mode for sigma_ex. Options include:
  - `all`: Use all data.
  - `positive`: Use only positive values.
  - `negative`: Use only negative values.
  - `le_mean`: Values less than the sigma-clipped mean.
  - `ge_mean`: Values greater than the sigma-clipped mean.
  - `le_median`: Values less than the sigma-clipped median.
  - `ge_median`: Values greater than the sigma-clipped median.
  - `le_std`: Values less than the sigma-clipped standard deviation.
  - `ge_std`: Values greater than the sigma-clipped standard deviation.
  - `custom`: Custom range defined by `xmin` and `xmax`.

  Example:
  -m ge_mean
  

- `-n, --nbins`: Number of bins for the histogram. Default is `200`.

  Example:
  -n 300

- `--xmin`: Minimum value for the custom mode.

  Example:
  --xmin 0

- `--xmax`: Maximum value for the custom mode.

  Example:
  --xmax 100

- `--sample`: Sample size for large datasets. Default is `1e7`.

  Example:
  --sample 5000000

- `-o, --output`: Output filename for the plot. Default is `sigmaex`.

  Example:
  -o output

### Example Commands

1. **Fitting a Gaussian to a FITS file:**

```sh
sigmaex data.fits
```

This will:
- Read the data from `data.fits`.
- Apply `3σ` clipping.
- Use all data for analysis.
- Generate a histogram with 200 bins.

2. **Fitting a Gaussian to a TIFF file with custom range:**

```sh
sigmaex data.tiff
```

This will:
- Read the data from `data.tiff`.
- Apply `5σ` clipping.
- Use the custom range between `0` and `100`.
- Generate a histogram with 200 bins.
- Save the plot as `sigmaex.pdf`.

### Plotting Output

- **PDF Plot**: A high-resolution plot showing the histogram and the fitted Gaussian curve. The output file is saved as a `.pdf` file (e.g., `sigmaex.pdf`).
  
- **Text Output**: A text file (`sigmaex.txt`) containing detailed statistics such as:
  - Raw statistics (mean, median, standard deviation, RMS).
  - Sigma-clipped statistics (mean, median, standard deviation, RMS).
  - Gaussian fit parameters (mean, standard deviation).

### Example Output

```
------ σEx ------
file: test.fits
sigma=3, mode='all', nbins=200

-> bin width = 0.00030774250626564026


:::::: Data ::::::
Input Data Shape: (1136, 1137)
==flatten==> length: 1291632
==3σ-clip==> length: 1254351 (2.89% clipped)

:::::: Raw Statistics ::::::
mean   = 0.00163
median = 0.000331
std    = 0.0143
rms    = 0.0144

:::::: 3σ-clip Statistics ::::::
sigma_clipped_mean   = 0.000147
sigma_clipped_median = 1.74e-05
sigma_clipped_std    = 0.0103
sigma_clipped_rms    = 0.0103

:::::: σEx Fitting ::::::
X ~ N(μ, σ^2) --- fitting range: [-0.0306, 0.0306]
μ: gaussian_fit_mu    = -5.94e-05
σ: gaussian_fit_sigma = 0.0102
```
