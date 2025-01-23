# -*- encoding: utf-8 -*-
'''
@File    :   sigmaex.py
@Time    :   2025/01/18
@Author  :   Mingyu Li
@Contact :   lmytime@hotmail.com
'''


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from astropy.stats import sigma_clip
from astropy.io import fits
import tifffile as tiff
import argparse
from lmfit.models import GaussianModel
from scipy.stats import norm
import time

class SigmaEx:
    def __init__(self, data, sigma=3, mode="1sigma", nbins=200, xmin=None, xmax=None, sample=1e7, path=None):
        self.data = data
        self.sigma = sigma
        self.mode = mode
        self.nbins = nbins
        self.xmin = xmin
        self.xmax = xmax
        self.sample = int(sample)
        self.sample_flag = False
        self.path = path

        self.data_flatten = self.data.flatten()

        # if data is too large, sample it
        if len(self.data_flatten) > self.sample:
            self.sample_flag = True
            self.data_flatten = np.random.choice(self.data_flatten, int(sample), replace=False)

        self.mean = np.nanmean(self.data)
        self.median = np.nanmedian(self.data)
        self.std = np.nanstd(self.data)
        self.rms = np.sqrt(np.nanmean(self.data**2))

        data_flatten_sigma_clipped = sigma_clip(self.data_flatten, sigma=self.sigma, masked=False)
        self.data_sigma_clipped = data_flatten_sigma_clipped

        ## sigma clipped mean, median, std
        self.sigma_clipped_mean = np.mean(data_flatten_sigma_clipped)
        self.sigma_clipped_median = np.median(data_flatten_sigma_clipped)
        self.sigma_clipped_std = np.std(data_flatten_sigma_clipped)
        self.sigma_clipped_rms = np.sqrt(np.mean(data_flatten_sigma_clipped**2))

        ## run sigma_ex
        self.n_all, self.bin_centers_all, self.n, self.bins, self.bin_centers, self.gaussian_fit_mu, self.gaussian_fit_sigma, self.gaussian_fit_A = self.__sigma_ex__(nbins, mode, xmin, xmax)

    @classmethod
    def from_fits(cls, path, ext=0, **kwargs):
        with fits.open(path) as hdulist:
            data = hdulist[ext].data
        return cls(data, path=path, **kwargs)

    @classmethod
    def from_tiff(cls, path, **kwargs):
        data = tiff.imread(path)
        return cls(data, path=path, **kwargs)

    def __1D_gaussian__(self, x, mu, sigma, A):
        return A/np.sqrt(2*np.pi)/sigma*np.exp(-0.5*np.power((x-mu)/sigma, 2))

    def __sigma_ex__(self, nbins=1000, mode="1sigma", xmin=None, xmax=None):
        n_all, bins = np.histogram(self.data_sigma_clipped, bins=nbins, density=True)
        bin_centers_all = (bins[:-1] + bins[1:])/2
        bin_width = bins[1] - bins[0]

        if mode == "all":
            n = n_all
            bin_centers = bin_centers_all
        elif mode == "positive":
            n = n_all[bin_centers_all>0]
            bin_centers = bin_centers_all[bin_centers_all>0]
        elif mode == "negative":
            n = n_all[bin_centers_all<0]
            bin_centers = bin_centers_all[bin_centers_all<0]
        elif mode == "le_mean":
            n = n_all[bin_centers_all<self.sigma_clipped_mean]
            bin_centers = bin_centers_all[bin_centers_all<self.sigma_clipped_mean]
        elif mode == "ge_mean":
            n = n_all[bin_centers_all>self.sigma_clipped_mean]
            bin_centers = bin_centers_all[bin_centers_all>self.sigma_clipped_mean]
        elif mode == "le_median":
            n = n_all[bin_centers_all<self.sigma_clipped_median]
            bin_centers = bin_centers_all[bin_centers_all<self.sigma_clipped_median]
        elif mode == "ge_median":
            n = n_all[bin_centers_all>self.sigma_clipped_median]
            bin_centers = bin_centers_all[bin_centers_all>self.sigma_clipped_median]
        elif mode == "le_std":
            n = n_all[bin_centers_all<self.sigma_clipped_std]
            bin_centers = bin_centers_all[bin_centers_all<self.sigma_clipped_std]
        elif mode == "ge_std":
            n = n_all[bin_centers_all>self.sigma_clipped_std]
            bin_centers = bin_centers_all[bin_centers_all>self.sigma_clipped_std]
        elif mode == "1sigma":
            n = n_all[bin_centers_all<self.sigma_clipped_mean+self.sigma_clipped_std]
            bin_centers = bin_centers_all[bin_centers_all<self.sigma_clipped_mean+self.sigma_clipped_std]
        elif mode == "custom":
            n = n_all[(bin_centers_all>xmin) & (bin_centers_all<xmax)]
            bin_centers = bin_centers_all[(bin_centers_all>xmin) & (bin_centers_all<xmax)]
        else:
            raise ValueError("mode should be one of 'all', 'positive', 'negative', 'le_mean', 'ge_mean', 'le_median', 'ge_median', 'le_std', 'ge_std', '1sigma', 'custom'")

        # Using curve_fit
        # popt, _ = curve_fit(self.__1D_gaussian__, bin_centers, n, p0=[self.sigma_clipped_mean, self.sigma_clipped_std, np.max(n)])
        # gaussian_fit_mu, gaussian_fit_sigma, gaussian_fit_A = popt

        # Using lmfit
        model = GaussianModel()
        params = model.make_params(amplitude=np.max(n), center=self.sigma_clipped_mean, sigma=self.sigma_clipped_std)
        result = model.fit(n, params, x=bin_centers)
        self.fit_result = result
        gaussian_fit_mu, gaussian_fit_sigma, gaussian_fit_A = result.best_values['center'], result.best_values['sigma'], result.best_values['amplitude']
        # Estimate the reduced chi2
        std = self.bi_std(result.best_fit, result.best_values['center'], result.best_values['sigma'], bin_centers, bin_width)
        chi2 = np.sum(((result.best_fit - n)/std)**2)
        redchi2 = chi2/(result.ndata-3)
        self.redchi2 = redchi2

        return n_all, bin_centers_all, n, bins, bin_centers, gaussian_fit_mu, gaussian_fit_sigma, gaussian_fit_A


    def bi_std(self, N, mu, sigma, x_cen, dx):
        p = norm.cdf((x_cen + dx/2 - mu) / sigma) - norm.cdf((x_cen - dx/2 - mu) / sigma)
        std = np.sqrt(N * p * (1-p))
        return std

    def plot(self, ax=None, filename=None, **kwargs):
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(10,6), dpi=100)

        ax.hist(self.data_sigma_clipped, bins=self.bins, histtype='step', color='k', density=True,
                label='Input Data {:d}σ-clip\nmean = {:.2e}\nmed = {:.2e}\nstd = {:.2e}'.format(self.sigma, self.sigma_clipped_mean, self.sigma_clipped_median, self.sigma_clipped_std))

        ax.plot(self.bin_centers, self.__1D_gaussian__(self.bin_centers, self.gaussian_fit_mu, self.gaussian_fit_sigma, self.gaussian_fit_A), color='#f40',
                lw=8, alpha=0.4, label="σEx Fit Range")
        ax.plot(self.bin_centers_all, self.__1D_gaussian__(self.bin_centers_all, self.gaussian_fit_mu, self.gaussian_fit_sigma, self.gaussian_fit_A), 'r-', lw=1,
                label='Gaussian Fit\nμ = {:.2e}\nσ = {:.2e}'.format(self.gaussian_fit_mu, self.gaussian_fit_sigma, self.gaussian_fit_A))

        ax.axvline(self.gaussian_fit_mu, color='r', linestyle='-.')
        ax.errorbar(self.gaussian_fit_mu, self.gaussian_fit_A/self.gaussian_fit_sigma/25, xerr=self.gaussian_fit_sigma, fmt='None', color='r',
                    elinewidth=2, capsize=5, capthick=2)

        ax.axvline(self.sigma_clipped_mean, color='k', linestyle='-.')
        ax.errorbar(self.sigma_clipped_mean, self.gaussian_fit_A/self.gaussian_fit_sigma/22, xerr=self.sigma_clipped_std, fmt='None', color='k',
                    elinewidth=1, capsize=3, capthick=1)

        ax.text(0.04, 0.96, f"nbins = {self.nbins}\nbin width = {self.bins[1]-self.bins[0]:.2e}\nReduced χ2 = {self.redchi2:.2f}", ha='left', va='top', transform=ax.transAxes)
        ax.set_xlabel('Pixel Value')
        ax.set_ylabel('Density')


        ax.legend(bbox_to_anchor=(1, 1))

        if filename is not None:
            plt.savefig(filename, bbox_inches='tight', **kwargs)

        if ax is None:
            return fig, ax
        else:
            return None

    def __round__(self, number, n):
        return float(f"{number:.{n}e}")

    def __repr__(self):
        self.plot()
        return self.__str__()

    def __str__(self):

        # get parameters
        sigma = self.sigma
        mode = self.mode
        nbins = self.nbins
        xmin = self.xmin
        xmax = self.xmax
        sample = self.sample
        path = self.path

        parameter_str = ""

        if path is not None:
            parameter_str = f"file: {path}\n"

        if xmin is None and xmax is None:
            parameter_str += f"{sigma=}, {mode=}, {nbins=}"
        elif xmin is not None and xmax is None:
            parameter_str += f"{sigma=}, {mode=}, {nbins=}, {xmin=}"
        elif xmin is None and xmax is not None:
            parameter_str += f"{sigma=}, {mode=}, {nbins=}, {xmax=}"
        else:
            parameter_str += f"{sigma=}, {mode=}, {nbins=}, {xmin=}, {xmax=}"

        if sample != 1e7:
            parameter_str += f", sample={sample}"


        sample_flag_str = f"-! These results are based on a N={sample} subsample" if self.sample_flag else ""

        n = 2
        mean = self.__round__(self.mean, n)
        median = self.__round__(self.median, n)
        std = self.__round__(self.std, n)
        rms = self.__round__(self.rms, n)
        sigma_clipped_mean = self.__round__(self.sigma_clipped_mean, n)
        sigma_clipped_median = self.__round__(self.sigma_clipped_median, n)
        sigma_clipped_std = self.__round__(self.sigma_clipped_std, n)
        sigma_clipped_rms = self.__round__(self.sigma_clipped_rms, n)
        gaussian_fit_mu = self.__round__(self.gaussian_fit_mu, n)
        gaussian_fit_sigma = self.__round__(self.gaussian_fit_sigma, n)
        bin_centers_min = self.__round__(self.bin_centers[0], n)
        bin_centers_max = self.__round__(self.bin_centers[-1], n)
        redchi2 = f"{self.redchi2:.2f}"

        return f"------ σEx ------\
\n{parameter_str}\n\
\n-> bin width = {self.bins[1]-self.bins[0]}\
\n{sample_flag_str}\
\n\n:::::: Data ::::::\
\nInput Data Shape: {self.data.shape}\
\n==flatten==> length: {len(self.data_flatten)}\
\n=={self.sigma}σ-clip==> length: {len(self.data_sigma_clipped)} ({100-100*len(self.data_sigma_clipped)/len(self.data_flatten):.2f}% clipped)\
\n\n:::::: Raw Statistics ::::::\
\nmean   = {mean}\
\nmedian = {median}\
\nstd    = {std}\
\nrms    = {rms}\
\n\n:::::: {self.sigma}σ-clip Statistics ::::::\
\nsigma_clipped_mean   = {sigma_clipped_mean}\
\nsigma_clipped_median = {sigma_clipped_median}\
\nsigma_clipped_std    = {sigma_clipped_std}\
\nsigma_clipped_rms    = {sigma_clipped_rms}\
\n\n:::::: σEx Fitting ::::::\
\nX ~ N(μ, σ^2) --- fitting range: [{bin_centers_min}, {bin_centers_max}]\
\nReduced χ^2 = {redchi2}\
\nμ: gaussian_fit_mu    = {gaussian_fit_mu}\
\nσ: gaussian_fit_sigma = {gaussian_fit_sigma}"

def main():
    parser = argparse.ArgumentParser(description='A python package for checking the gaussian histogram of data array.')
    parser.add_argument('data', type=str, help='Path to the data file.')
    parser.add_argument('-s', '--sigma', type=float, default=3, help='Sigma for sigma clipping.')
    parser.add_argument('-m', '--mode', type=str, default='1sigma', help='Mode for sigma_ex. One of "all", "positive", "negative", "le_mean", "ge_mean", "le_median", "ge_median", "le_std", "ge_std", "1sigma", "custom".')
    parser.add_argument('-n', '--nbins', type=int, default=200, help='Number of bins for the histogram.')
    parser.add_argument('--xmin', type=float, default=None, help='Minimum value for the custom mode.')
    parser.add_argument('--xmax', type=float, default=None, help='Maximum value for the custom mode.')
    parser.add_argument('--sample', type=float, default=1e7, help='Sample size for the data. If the data is too large, it will be sampled to this size.')
    parser.add_argument('-o', '--output', type=str, default="sigmaex_"+time.strftime("%Y%m%d_%H%M%S", time.localtime()), help='Output filename for the plot.')
    args = parser.parse_args()

    if args.data.endswith('.fits'):
        sigmaex = SigmaEx.from_fits(args.data, sigma=args.sigma, mode=args.mode, nbins=args.nbins, xmin=args.xmin, xmax=args.xmax, sample=args.sample)
    elif args.data.endswith('.tif') or args.data.endswith('.tiff'):
        sigmaex = SigmaEx.from_tiff(args.data, sigma=args.sigma, mode=args.mode, nbins=args.nbins, xmin=args.xmin, xmax=args.xmax, sample=args.sample)
    else:
        raise ValueError("Data file should be a fits or tiff file.")

    # Using non-interactive backend
    matplotlib.use('Agg')
    # Setting the plot style
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams['mathtext.fontset'] = 'dejavuserif'
    plt.rcParams['font.size']=15
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams["xtick.minor.visible"] =  True
    plt.rcParams["ytick.minor.visible"] =  True
    plt.rcParams['axes.edgecolor']='black'
    plt.rcParams['xtick.color']='k'
    plt.rcParams['ytick.color']='k'
    plt.rcParams['xtick.labelcolor']='k'
    plt.rcParams['ytick.labelcolor']='k'
    plt.rcParams['xtick.major.size'] = 10
    plt.rcParams['xtick.major.width'] = 1
    plt.rcParams['xtick.minor.size'] = 5
    plt.rcParams['xtick.minor.width'] = 0.75
    plt.rcParams['ytick.major.size'] = 10
    plt.rcParams['ytick.major.width'] = 1
    plt.rcParams['ytick.minor.size'] = 5
    plt.rcParams['ytick.minor.width'] = 0.75
    plt.rcParams["xtick.top"] = True
    plt.rcParams["ytick.right"] = True
    plt.rcParams["font.size"] = 15

    # Plotting
    fig, ax = plt.subplots(1, 1, figsize=(10,6), dpi=300)
    sigmaex.plot(ax=ax)
    plt.savefig(args.output + ".pdf", bbox_inches='tight')
    plt.close()

    # Print the results
    print(sigmaex)
    # Save the results
    with open(args.output + ".txt", "w") as f:
        f.write(str(sigmaex))

if __name__ == "__main__":
    main()