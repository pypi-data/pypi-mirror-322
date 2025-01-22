from scipy import signal
from scipy.fft import fft
import numpy as np
from math import log2
from functools import reduce
from scipy.stats import skew
from scipy.stats import kurtosis as kurt

def de_origin(data, args):
    # TODO: check input and output 
    variance = np.var(signal, ddof=1)  # 求得方差
    return math.log(2 * math.pi * math.e * variance) / 2  # 微分熵求取公式


def de(data, args):
    """
        compute de feature in the first channels
        record corresponding video number
        input: [channel, down-sampled timesteps]
        ourput: eeg de features, video list
    """
    window_length = args['win_length']
    window_type  = args['win_type']
    time_sample = args['down_sample']
    frequency_sample_rate = args['freq_sample_rate']
    bands = args['bands']

    # channels = data.shape[0] - 1
    channels = data.shape[0]
    timesteps = data.shape[1]
    windows = int(timesteps / time_sample / window_length)
    bands_num = len(bands) - 1
    rate = int(frequency_sample_rate / time_sample)  # 频时采样比率
    frequency_window_points = int(window_length * frequency_sample_rate)
    # Declare DE tensor
    DE = np.zeros((channels, windows, bands_num))
    # get window function
    time_window_points = int(window_length * time_sample)
    if window_type == 'hanning':
        window_function = signal.windows.hann(time_window_points)
    else:
        return "undefined window type yet0"
    # compute DE of a sampled data
    for i in range(channels):
        for j in range(windows):
            # Apply window function
            data_mul_window = data[i, j * time_window_points:(j + 1) * time_window_points] * window_function
            # Apply DFT
            fft_data = abs(fft(data_mul_window, frequency_window_points)[:int(frequency_window_points / 2)])
            # compute DE
            for k in range(bands_num):
                bands_list = fft_data[int(bands[k] * rate):int(bands[k + 1] * rate - 1)]
                DE[i][j][k] = log2(100 * reduce(lambda x, y: x + y, map(lambda x: x * x, bands_list)) / len(bands_list))

    # TODO: check reshape
    DE = DE.reshape(channels, windows, bands_num)

    return DE

def _get_average_psd(energy_graph, freq_bands, sample_freq, stft_n=256):
    # print(stft_n, freq_bands[0] * 1.0/ sample_freq * stft_n)
    start_index = int(np.floor(freq_bands[0] * 1.0 / sample_freq * stft_n))
    end_index = int(np.floor(freq_bands[1] * 1.0 / sample_freq * stft_n))
    # print('here',start_index, end_index)
    ave_psd = np.mean(energy_graph[:, start_index - 1:end_index] ** 2, axis=1)
    # print(ave_psd)
    return ave_psd
    
def psd(data, args):
    window_length = args['win_length']
    window_type  = args['win_type']
    time_sample = args['down_sample']
    frequency_sample_rate = args['freq_sample_rate']
    bands = args['bands']
    n_channels, n_samples = data.shape

    point_per_window = int(time_sample * window_length)
    window_num = int(n_samples / time_sample / window_length)
    psd_feature = np.zeros((window_num, len(bands) - 1, n_channels))

    for window_index in range(window_num):
        start_index, end_index = point_per_window * window_index, point_per_window * (window_index + 1)
        window_data = data[:, start_index:end_index]
        if window_type == 'hanning':
            hdata = window_data * signal.windows.hann(point_per_window)
        else:
            return "undefined window type yet0"

        fft_data = np.fft.fft(hdata, n=time_sample)
        energy_graph = np.abs(fft_data[:, 0: int(time_sample / 2)])

        for i in range(len(bands) - 1):
            band_ave_psd = _get_average_psd(energy_graph, [bands[i],bands[i+1]], frequency_sample_rate, time_sample)
            psd_feature[window_index, i, :] = band_ave_psd
    
    transposed_psd_feature = np.transpose(psd_feature, axes=(2, 0, 1)) 
    return transposed_psd_feature


def mean(data, args):
    window_length = args['win_length']
    frequency_sample_rate = args['down_sample']
    n_channels, n_samples = data.shape

    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    mean_feature = np.zeros((n_channels, window_num))
    
    for window_index in range(window_num):
        mean_feature[:, window_index] = np.mean(data[:, window_index*point_per_window:(window_index+1)*point_per_window],\
                                        axis=1)
    mean_feature = np.expand_dims(mean_feature, axis=2)
    return mean_feature

def std(data, args):
    window_length = args['win_length']
    frequency_sample_rate = args['down_sample']
   
    n_channels, n_samples = data.shape

    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    feature = np.zeros((n_channels, window_num))

    for window_index in range(window_num):
        feature[:, window_index] = np.std(data[:, window_index*point_per_window:(window_index+1)*point_per_window],\
                                        axis=1)
    feature = np.expand_dims(feature, axis=2)
    return feature


def skewness(data, args):
    window_length = args['win_length']
    frequency_sample_rate = args['down_sample']
   
    n_channels, n_samples = data.shape

    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    feature = np.zeros((n_channels, window_num))

    for window_index in range(window_num):
        feature[:, window_index] = skew(data[:, window_index*point_per_window:(window_index+1)*point_per_window],\
                                        axis=1)
    feature = np.expand_dims(feature, axis=2)
    return feature

def kurtosis(data, args):
    window_length = args['win_length']
    frequency_sample_rate = args['down_sample']
   
    n_channels, n_samples = data.shape

    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    feature = np.zeros((n_channels, window_num))

    for window_index in range(window_num):
        feature[:, window_index] = kurt(data[:, window_index*point_per_window:(window_index+1)*point_per_window],\
                                        axis=1)
    feature = np.expand_dims(feature, axis=2)
    return feature

# TODO: 下面的特征都没有被检查过代码
def pp(data, args):
    window_length = args['win_length']
    frequency_sample_rate = args['freq_sample_rate']
   
    n_channels, n_samples = data.shape

    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    feature = np.zeros((n_channels, window_num))

    for window_index in range(window_num):
        feature[:, window_index] = np.max(data[:, window_index*point_per_window:(window_index+1)*point_per_window], axis=1) - \
                np.min(data[:, window_index*point_per_window:(window_index+1)*point_per_window], axis=1)

    return feature
# Mark: 需要写 ERP 吗？怎么定义的？

def delta(data, args):
    '''
        计算一阶差分绝对值的平均值
        input: [channel, down-sampled timesteps]
        output: 差分绝对值特征
    '''
    window_length = args['window_length']
    frequency_sample_rate = args['frequency_sample_rate']
   
    n_channels, n_samples = data.shape

    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    feature = np.zeros((n_channels, window_num))

    for window_index in range(window_num):
        feature[:, window_index] = np.mean(np.abs(
            np.diff(data[:, window_index*point_per_window:(window_index+1)*point_per_window], axis=1)
        ), axis=1)
    return feature

def gamma(data, args):
    '''
        计算二阶差分绝对值的平均值
        input: [channel, down-sampled timesteps]
        output: 差分绝对值特征
    '''
    window_length = args['window_length']
    frequency_sample_rate = args['frequency_sample_rate']

    n_channels, n_samples = data.shape

    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    feature = np.zeros((n_channels, window_num))

    for window_index in range(window_num):
        feature[:, window_index] = np.mean(np.abs(
            data[:, window_index*point_per_window + 2:(window_index+1)*point_per_window] - 
            data[:, window_index*point_per_window:(window_index+1)*point_per_window - 2]
        ), axis=1)

def delta_normal(data, args):
    '''
        计算归一化一阶差分
        input: [channel, down-sampled timesteps]
        output: 归一化差分绝对值特征
    '''
    window_length = args['window_length']
    frequency_sample_rate = args['frequency_sample_rate']
   
    n_channels, n_samples = data.shape

    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    feature = np.zeros((n_channels, window_num))

    for window_index in range(window_num):
        feature[:, window_index] = np.mean(np.abs(
            np.diff(data[:, window_index*point_per_window:(window_index+1)*point_per_window], axis=1)
        ), axis=1) \
            / np.std(data[:, window_index*point_per_window:(window_index+1)*point_per_window], axis=1)
    return feature

def gamma_normal(data, args):
    '''
        计算归一化二阶差分
        input: [channel, down-sampled timesteps]
        output: 归一化差分绝对值特征
    '''
    window_length = args['window_length']
    frequency_sample_rate = args['frequency_sample_rate']

    n_channels, n_samples = data.shape

    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    feature = np.zeros((n_channels, window_num))

    for window_index in range(window_num):
        feature[:, window_index] = np.mean(np.abs(
            data[:, window_index*point_per_window + 2:(window_index+1)*point_per_window] - 
            data[:, window_index*point_per_window:(window_index+1)*point_per_window - 2]
        ), axis=1) \
            / np.std(data[:, window_index*point_per_window:(window_index+1)*point_per_window], axis=1)
        
    return feature

def energy(data, args):
    '''
        计算能量特征
        input: [channel, down-sampled timesteps]
        output: 能量特征
    '''
    window_length = args['window_length']
    frequency_sample_rate = args['frequency_sample_rate']

    n_channels, n_samples = data.shape

    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    feature = np.zeros((n_channels, window_num))

    for window_index in range(window_num):
        feature[:, window_index] = np.sum(
            data[:, window_index*point_per_window:(window_index+1)*point_per_window] ** 2, axis=1
        )
        
    return feature

def power(data, args):
    '''
        计算功率特征
        input: [channel, down-sampled timesteps]
        output: 功率特征
    '''
    window_length = args['window_length']
    frequency_sample_rate = args['frequency_sample_rate']

    n_channels, n_samples = data.shape

    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    feature = np.zeros((n_channels, window_num))

    for window_index in range(window_num):
        feature[:, window_index] = np.mean(
            data[:, window_index*point_per_window:(window_index+1)*point_per_window] ** 2, axis=1
        )
        
    return feature

# Hjorth 参数特征：张琦的工作已经涉及了这一块，这里就跳过了

def hoc_calc(data, M):
    '''
        将 data 变成均值为 0 的序列，并依次通过 M 个高通滤波器，用以计算 HOC 特征
    '''
    mean = np.mean(data)
    data = data - mean
    print(data)
    data_len = data.shape[0]
    hoc = []
    for k in range(1, M + 1):
        filtered_data = []
        for i in range(k - 1, data_len):
            ele = 0
            for j in range(k):
                ele = ele + comb(k - 1, j) * ((-1) ** j) * data[i - j]
            filtered_data.append(1 if ele > 0 else 0)
        hoc.append(np.sum(np.abs(np.diff(np.array(filtered_data)))).tolist())
    return np.array(hoc)

def hoc(data, args):
    '''
        计算 HOC 特征
        input: [channel, down-sampled timesteps]
        output: HOC 特征
        parameter: wave_filter_count - 要通过的高通滤波器数量
    '''
    window_length = args['window_length']
    frequency_sample_rate = args['frequency_sample_rate']
    M = args['wave_filter_count']

    n_channels, n_samples = data.shape

    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    feature = np.zeros((n_channels, window_num, M))

    for window_index in range(window_num):
        for i in range(n_channels):
            feature[i, window_index] = hoc_calc(data[i, window_index*point_per_window:(window_index+1)*point_per_window], M)
        
    return feature

def nsi_calc(data, N):
    '''
        计算 NSI 特征
        input: [channel, down-sampled timesteps]
        output: NSI 特征
        parameter: N - 段数
    '''
    n_channels, data_len = data.shape
    nsi_tmp_val = np.zeros((n_channels, N))
    for k in range(1, N + 1):
        nsi_tmp_val[:, k] = np.mean(data[:, int((k - 1) * data_len / N):int(k * data_len / N)], axis=1)
    return np.std(nsi_tmp_val, axis=1)

def nsi(data, args):
    '''
        计算 NSI 特征
        input: [channel, down-sampled timesteps]
        output: NSI 特征
        parameter: segment_count - 每个时间窗要分割成的段数
    '''
    window_length = args['window_length']
    frequency_sample_rate = args['frequency_sample_rate']
    N = args['segment_count']

    n_channels, n_samples = data.shape
    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    feature = np.zeros((n_channels, window_num))

    for window_index in range(window_num):
        feature[:, window_index] = nsi_calc(data[:, window_index*point_per_window:(window_index+1)*point_per_window], N)
    return feature

# 计算 Hilbert-Huang 谱分解
def hhsd_calc(data, args):
    '''
        输入*一维*数据，计算其 HHS 分解熵
        input: [down-sampled timesteps]
        output: entropy
    '''
    bands = args['bands']
    sample_rate = args['frequency_sample_rate']
    imf_cnt = args['imf_cnt']
    time_sample = args['time_sample']
    bands_num = len(bands) - 1
    # 进行 EMD 分解
    imf = emd.sift.mask_sift(data, max_imfs=imf_cnt)
    _, IF, IA = emd.spectra.frequency_transform(imf, sample_rate, 'nht')
    # 计算每个 imf 的 Hilbert-Huang 谱
    f, spec_weighted = emd.spectra.hilberthuang(IF, IA, sample_rate=sample_rate, mode='power')
    energy = []
    spec_cnt = len(f)
    for i in range(bands_num - 1):
        for j in range(spec_cnt):
            _power = 0
            if bands[i] <= f[j] < bands[i + 1]:
                _power += spec_weighted[j]
        energy.append(_power)
    # 计算熵
    energy = np.array(energy)
    energy = energy / np.sum(energy)
    entropy = - np.sum(energy * np.log(energy))
    return entropy

def hhsd_entropy(data, args):
    '''
        计算 HHS 分解熵
        input: [channel, down-sampled timesteps]
        output: HHS 分解熵
        parameter: imf_cnt - IMF 分解的层数
    '''
    window_length = args['window_length']
    frequency_sample_rate = args['frequency_sample_rate']
    bands = args['bands']

    n_channels, n_samples = data.shape
    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    bands_num = len(bands) - 1
    feature = np.zeros((n_channels, window_num, bands_num))

    for window_index in range(window_num):
        for i in range(n_channels):
            feature[i, window_index] = hhsd_calc(data[i, window_index*point_per_window:(window_index+1)*point_per_window], args)
        
    return feature
    
# TODO List： 相干性特征矩阵