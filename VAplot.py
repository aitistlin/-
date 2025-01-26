import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

#
# num1 = 36600+13500
# num2 = 36600+40500
#
#
# data1 = pd.read_csv(r'F:\（F盘）文件接收\至诚实验与相关数据\实验数据(未整理)\2024_1106\122.CSV')
# data2 = pd.read_csv(r'F:\（F盘）文件接收\至诚实验与相关数据\实验数据(未整理)\2024_1106\122.CSV')

num1 = 27600 + 13500
num2 = 27600 + 40500

data1 = pd.read_csv(r'F:\（F盘）文件接收\至诚实验与相关数据\实验数据(未整理)\2024_1201\123.CSV')
data2 = pd.read_csv(r'F:\（F盘）文件接收\至诚实验与相关数据\实验数据(未整理)\2024_1201\123.CSV')


def getcv(data, num):
    N = 1
    start_point = num
    fs = 8000 / (data['in s'].iloc[8000] - data['in s'].iloc[0])
    timestamp = data['in s'].iloc[start_point:start_point + 8000]

    print('采样频率：', fs)
    print('取样长度/四个周期：', int((fs / 50) * 4))
    print('取样区间：', num, '到', num + int((fs / 50) * 4))
    print('')
    T = 1 / fs
    timestamp = data['in s'].iloc[start_point:start_point + int((fs / 50) * N)]
    signal = data['C2 in A'].iloc[start_point:start_point + int((fs / 50) * N)]
    signal = signal - data['C2 in A'].mean()
    timestamp = 10 * (timestamp - timestamp.iloc[0]).reset_index(drop=True)
    voltage = data['C1 in V'].iloc[start_point:start_point + int((fs / 50) * N)].tolist()
    correlation, _ = pearsonr(signal, pd.Series(voltage))
    if correlation < 0:
        voltage = [-i for i in voltage]
    voltage = pd.Series(voltage)
    # 将电流和电压数据归一化到-1到1范围,这段代码可选，注意修改标幺值
    max_current = max(signal)
    min_current = min(signal)
    max_voltage = max(voltage)
    min_voltage = min(voltage)
    max_timestamp = max(timestamp)
    min_timestamp = min(timestamp)
    signal = 2 * (signal - min_current) / (max_current - min_current) - 1
    voltage = 2 * (voltage - min_voltage) / (max_voltage - min_voltage) - 1
    timestamp = 20 * (timestamp - min_timestamp) / (max_timestamp - min_timestamp)
    return signal, voltage, timestamp


signal1, voltage1, timestamp1 = getcv(data1, num1)
signal2, voltage2, timestamp2 = getcv(data2, num2)

# 创建子图 winter , copper_r
fig, axs = plt.subplots(1, 2, figsize=(16 / 2.54, 6.5 / 2.54))

plt.rcParams.update({'font.size': 12, 'font.family': 'serif', 'font.serif': ['Times New Roman']})

# 在第一个子图上绘制
scatter = axs[0].scatter(signal1, voltage1, c=timestamp1, cmap='winter', s=5)
axs[0].set_yticks([-1, 0, 1])
axs[0].set_xticks([-1, 0, 1])
for spine in axs[0].spines.values():
    spine.set_linewidth(2)
# axs[0].text(0.35, 0.92, 'Stage I', horizontalalignment='center', verticalalignment='center', transform=axs[0].transAxes,
#             fontsize=12, color='#00729F')

# 在第二个子图上绘制
scatter = axs[1].scatter(signal2, voltage2, c=timestamp2, cmap='winter', s=5)
axs[1].set_yticks([])
axs[1].set_xticks([-1, 0, 1])
for spine in axs[1].spines.values():
    spine.set_linewidth(2)
# axs[1].text(0.35, 0.92, 'Stage II', horizontalalignment='center', verticalalignment='center',
#             transform=axs[1].transAxes,
#             fontsize=12, color='#609B7B')

# 添加颜色条到整个图
cbar_ax = fig.add_axes([0.89, 0.2, 0.025, 0.75])  # 指定颜色条的位置和大小
colorbar = fig.colorbar(scatter, cax=cbar_ax, label='')
colorbar.ax.tick_params(labelsize=12, width=2)
new_ticks = [0, 10, 20]  # 颜色条新的刻度值
colorbar.set_ticks(new_ticks)
colorbar.outline.set_linewidth(2)

plt.subplots_adjust(left=0.1, right=0.85, top=0.95, bottom=0.2)  # 调整左右边距

# 保存图像
plt.savefig("05地面故障伏安特性.png", dpi=500)
plt.show()
