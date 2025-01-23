import scipy.signal as signal


def eeg_acc_reshape(acc, *args):
    # 直接在原始数据上进行操作，不创建新的数组
    # acc只进行了长度裁剪，没有进行重采样
    # 15 * 50 表示每15秒有750个点，说明acc原始采样率为50Hz
    acc = acc[:, : acc.shape[1] // (15 * 50) * (15 * 50)]

    # 使用列表推导式和切片来进行原地操作
    # EEG信号重采样：500Hz -> 100Hz
    # 原始：30秒 * 500Hz = 15000个点
    # 重采样后：30秒 * 100Hz = 3000个点
    eeg_reshaped = [
        signal.resample(eeg[:eeg.shape[0] // (30 * 500) * (30 * 500)].reshape(-1, 30 * 500), 100 * 30, axis=1).ravel()
        for eeg in args]

    # 返回结果，使用解包来返回多个值
    return acc, *eeg_reshaped


def ecg_emg_reshape(ecg, emg):
    # ECG和EMG信号重采样：500Hz -> 50Hz
    # 原始：30秒 * 500Hz = 15000个点
    # 重采样后：30秒 * 50Hz = 1500个点
    ecg = signal.resample(ecg[:ecg.shape[0] // (30 * 500) * (30 * 500)].reshape(-1, 30 * 500), 50 * 30, axis=1).ravel()
    emg = signal.resample(emg[:emg.shape[0] // (30 * 500) * (30 * 500)].reshape(-1, 30 * 500), 50 * 30, axis=1).ravel()

    # 返回结果，使用解包来返回多个值
    return ecg, emg
