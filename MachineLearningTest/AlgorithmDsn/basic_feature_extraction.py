# data_preprocessor.py
import numpy as np
from sklearn.preprocessing import StandardScaler
from joblib import Parallel, delayed

# 传感器分组配置
SENSOR_GROUPS = {
    '100Hz': ['PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6', 'EPS1'],
    '10Hz': ['FS1', 'FS2'],
    '1Hz': ['TS1', 'TS2', 'TS3', 'TS4', 'VS1', 'SE', 'CE', 'CP']
}


def extract_features(data, sensor_type):
    """从传感器数据中提取基础统计特征"""
    features = [
        np.mean(data),  # 均值
        np.std(data),  # 标准差
        np.min(data),  # 最小值
        np.max(data)  # 最大值
    ]
    # 高频传感器额外计算峰峰值
    if sensor_type in ['100Hz', '10Hz']:
        features.append(np.ptp(data))  # 峰峰值
    return features


def process_sensor(sensor, freq, data_folder='./data'):
    """处理单个传感器的特征提取"""
    file_path = f'{data_folder}/{sensor}.txt'
    data = np.loadtxt(file_path)

    if freq in ['100Hz', '10Hz']:
        return np.column_stack((
            np.mean(data, axis=1),
            np.std(data, axis=1),
            np.min(data, axis=1),
            np.max(data, axis=1),
            np.ptp(data, axis=1)
        ))
    else:  # 1Hz
        return np.column_stack((
            np.mean(data, axis=1),
            np.std(data, axis=1),
            np.min(data, axis=1),
            np.max(data, axis=1)
        ))


def load_and_preprocess_data(data_folder='./data', test_size=0.2, n_jobs=-1):
    """
    加载并预处理数据

    参数:
        data_folder: 数据文件夹路径
        test_size: 测试集比例
        n_jobs: 并行任务数

    返回:
        X_train_scaled: 标准化后的训练特征
        X_test_scaled: 标准化后的测试特征
        y_train: 训练标签
        y_test: 测试标签
        scaler: 标准化器对象
    """
    # 加载标签数据
    profile_path = f'{data_folder}/profile.txt'
    profile_data = np.loadtxt(profile_path)
    pump_labels = profile_data[:, 2].astype(int)  # 泵状态
    stable_flags = profile_data[:, 4].astype(int)  # 稳定标志

    # 并行处理所有传感器
    all_features = []
    for freq, sensors in SENSOR_GROUPS.items():
        freq_features = Parallel(n_jobs=n_jobs)(
            delayed(process_sensor)(sensor, freq, data_folder) for sensor in sensors
        )
        all_features.extend(freq_features)

    # 水平拼接所有特征
    X = np.hstack(all_features)
    y = pump_labels

    # 只保留稳定状态的数据
    stable_mask = (stable_flags == 0)
    X_stable = X[stable_mask]
    y_stable = y[stable_mask]

    print(f"原始数据周期数: {X.shape[0]}")
    print(f"稳定状态周期数: {X_stable.shape[0]}")

    # 按时间顺序划分数据集
    split_idx = int((1 - test_size) * len(X_stable))
    X_train = X_stable[:split_idx]
    y_train = y_stable[:split_idx]
    X_test = X_stable[split_idx:]
    y_test = y_stable[split_idx:]

    # 标准化特征
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, X_train_scaled, X_test_scaled