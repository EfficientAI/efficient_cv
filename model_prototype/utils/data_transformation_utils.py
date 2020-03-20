import numpy as np
from scipy.signal import resample
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler


def upsample_signal(data, sampling_factor, sampler=None):
    """
    data is a time series sequence(nd_array) numpy data
    upsampling uses fourier interpolation.
    """
    return resample(data, sampling_factor*data.shape[0])


def downsample_signal(data, sampling_factor, sampler=None):
    """
    data is time series sequenced (nd_array) numpy data
    downsample just takes the average sampling_factor points.
    nr_data points should be divisible by sampling_factor
    """
    reshaped = data.reshape(data.shape[0]//sampling_factor, sampling_factor,
                            -1)
    return reshaped.mean(axis=1)


def generic_sampler(data, sampling_rate, sampler):
    """
    apply sampler on numpy data with sampling rate
    """
    data = data.reshape((int(data.shape[0]/sampling_rate)), sampling_rate)
    data = sampler(data, axis=1)
    return data


def standardizer_z_score(data, verbose=False):
    """
    data is a time seriese sequence (nd_array) numpy data
    normalize the data across time series by calculating mean and variance
    print the mean and variance if verbose is true.
    Here we standardize the data with z-score normalization.
    This is supposedly work only if data has gaussian distribution.

    Other normalization procedure to explore:
    * Median normalization
    * Sigmoid normalization
    * Tanh normalization
    """
    scaler = StandardScaler()
    scaler.fit(data)
    scaled_data = scaler.transform(data)
    if verbose:
        print("mean: ", scaler.mean_, " var: ", scaler.var_)
    return scaled_data


def normalizer_min_max(data, verbose=False):
    """
    Normalize the data in range 0 to 1. Supresses the scaler variations,
    but do not assume any gaussian distribution (this assumption is with
    standardization)
    """
    scaler = MinMaxScaler()
    scaler.fit(data)
    scaled_data = scaler.transform(data)
    if verbose:
        print("min: ", scaler.data_min_, " max: ", scaler.data_max_)
    return scaled_data


def normalizer_median_quantiles(data, verbose=False):
    """
    Normalize the data in range 75th and 25th percentile
    This normalization is robust to outliers
    """
    scaler = RobustScaler()
    scaler.fit(data)
    scaled_data = scaler.transform(data)
    if verbose:
        print("center: ", scaler.center_, " scale: ", scaler.scale_)
    return scaled_data

# #################################### Test ###################################


def test_upsample_signal():
    a = np.array([[1, 6], [2, 7], [3, 8], [4, 9]])
    b = downsample_signal(a, 2)
    print(b)


def test_downsample_signal():
    a = np.array([[1, 6], [2, 7], [3, 8], [4, 9]])
    b = downsample_signal(a, 2)
    print(b)


def test_standardizer_z_score():
    a = np.random.multivariate_normal(mean=[12, 3], cov=[[2, 0], [0, 5]],
                                      size=100)
    b = standardizer_z_score(a, True)
    print(b)


def test_normalizer_min_max():
    a = np.random.multivariate_normal(mean=[12, 3], cov=[[2, 0], [0, 5]],
                                      size=100)
    b = normalizer_min_max(a, True)
    print(b)


def test_normalizer_median_quantiles():
    a = np.random.multivariate_normal(mean=[12, 3], cov=[[2, 0], [0, 5]],
                                      size=100)
    b = normalizer_median_quantiles(a, True)
    print(b)


if __name__ == "__main__":
    pass
