from scipy import signal
from scipy.fft import fft
import numpy as np
from math import log2
from functools import reduce


def butter_bandpass(lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], 'bandpass')
    return b, a


def DE(data, window_length, window_type, time_sample, frequency_sample_rate, bands):
    """
        compute de feature in the first 18 channels
        record corresponding video number
        input: [18channel + video list, down-sampled timesteps]
        ourput: eeg de features, video list
    """
    channels = data.shape[0] - 1
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

    # select movie induced data and record corresponding video number
    # video_list = np.zeros(windows)
    # video_tag = np.array(data[-1]).astype(int)
    # for j in range(windows):
    #     video_list[j] = max(set(video_tag[j * time_window_points:(j + 1) * time_window_points].tolist()),
    #                         key=video_tag[j * time_window_points:(j + 1) * time_window_points].tolist().count)

    return DE


def _get_average_psd(energy_graph, freq_bands, sample_freq, stft_n=256):
    # print(stft_n, freq_bands[0] * 1.0/ sample_freq * stft_n)
    start_index = int(np.floor(freq_bands[0] * 1.0 / sample_freq * stft_n))
    end_index = int(np.floor(freq_bands[1] * 1.0 / sample_freq * stft_n))
    # print('here',start_index, end_index)
    ave_psd = np.mean(energy_graph[:, start_index - 1:end_index] ** 2, axis=1)
    # print(ave_psd)
    return ave_psd


#
#
def extract_psd_feature(data, window_length, window_type, time_sample, frequency_sample_rate, bands):
    n_channels, n_samples = data.shape

    point_per_window = int(frequency_sample_rate * window_length)
    window_num = int(n_samples // point_per_window)
    psd_feature = np.zeros((window_num, len(bands), n_channels))

    for window_index in range(window_num):
        start_index, end_index = point_per_window * window_index, point_per_window * (window_index + 1)
        window_data = data[:, start_index:end_index]
        if window_type == 'hanning':
            hdata = window_data * signal.windows.hann(point_per_window)
        else:
            return "undefined window type yet0"

        fft_data = np.fft.fft(hdata, n=time_sample)
        energy_graph = np.abs(fft_data[:, 0: int(time_sample / 2)])

        for band_index, band in enumerate(bands):
            band_ave_psd = _get_average_psd(energy_graph, band, frequency_sample_rate, time_sample)
            psd_feature[window_index, band_index, :] = band_ave_psd
    return psd_feature

#
# def process_physiological(path):
#     """ process eeg, ppg, gsr signal """
#     data = loadmat(os.path.join(path, 'datas.mat'))
#     ori_eeg = data['eeg_datas']
#     ori_gsr = data['gsr_datas']
#     ori_ppg = data['ppg_datas']
#     label = data['dis_label']
#     # print(ori_eeg.shape, ori_gsr.shape, ori_ppg.shape, label.shape)
#
#     # process eeg first
#     sample_eeg = ori_eeg[:, ::3]  # downsample 300hz to 100hz
#     eeg_bands = [4, 8, 14, 31, 45]
#     eeg, video_list_eeg = process_de(sample_eeg, window_length=1, window_type='hanning', \
#                                      time_sample_rate=100, frequency_sample_rate=1024, bands=eeg_bands)
#
#     # process gsr
#     # gsr does not need downsample
#     b, a = butter_bandpass(0.01, 1.9, 4.0, 2)
#     filt_gsr = signal.filtfilt(b, a, ori_gsr[0:1, :], axis=1)  # filt the gsr signal using 2-th butter filter
#     ori_gsr[0:1, :] = filt_gsr
#     gsr_bands = [0, 0.6, 1.2, 1.8, 2.0]
#     gsr, video_list_gsr = process_de(ori_gsr, window_length=1, window_type='hanning', \
#                                      time_sample_rate=4, frequency_sample_rate=64, bands=gsr_bands)
#
#     # process ppg
#     b, a = butter_bandpass(0.01, 49, 100, 2)
#     filt_ppg = signal.filtfilt(b, a, ori_ppg[0:1, :], axis=1)
#     ori_ppg[0:1, :] = filt_ppg
#     ppg_bands = [4, 8, 14, 31, 45]
#     ppg, video_list_ppg = process_de(ori_ppg, window_length=1, window_type='hanning', \
#                                      time_sample_rate=100, frequency_sample_rate=1024, bands=ppg_bands)
#     return eeg, gsr, ppg, video_list_eeg, video_list_gsr, video_list_ppg, label
#
#
# def process_rest_sate(signal, video_list):
#     # split all sample into traing set and testing set, 8 : 2
#     signal = signal.transpose(1, 0, 2)
#     video_list = video_list.reshape(-1, 1).astype("int")
#
#     # process resting state eeg
#     trial_eeg = np.where(video_list < 40)[0]  # tag 40 represents resting state among expriment
#     signal = signal[trial_eeg]
#     video_list = video_list[trial_eeg]
#
#     return signal, video_list
#








