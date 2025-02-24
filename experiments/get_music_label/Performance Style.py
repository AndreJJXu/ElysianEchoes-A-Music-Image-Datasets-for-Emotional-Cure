import json
import matplotlib.pyplot as plt
import numpy
import seaborn as sns
from collections import Counter
import os
# 读取JSON文件

# 初始化类别计数
instruments_counter = Counter()

# 统计每个类别的分布
root_dir = '/mnt/ssd/BeautifulXJJ/AIGC/s2s/ElysianEchoes/datasets'
for foldername in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, foldername)
    
    json_file = os.path.join(folder_path, 'music_label.json')
    with open(json_file, 'r') as file:
        data = json.load(file)
    for key, value in data.items():
        instruments_counter.update([data[key]["Music Labels"]['Performance Style']])

instruments = instruments_counter
print("\n" * 10, instruments)
print(len(instruments))

# 定义各类乐器的关键词
categories = {
    "Instrumental Focus": ["Instrumental", "NME", "Background Music", "No Singer", "No Accompaniment", "Soft Keyboard Harmony", "Wind Instrument", "Cello Accompaniment", "Plucked String Instrument", "Performed by Percussion", "Piano Accompaniment", "No Percussion", "Synthesiser Arrangements", "Organ", "Melodic Cello", "Orchestra", "Theremin", "Xylophone Melody"],
    "Atmospheric": ["Calming", "Relaxing", "Soothing", "Peaceful", "Soft", "Mellow", "Melancholic", "Sentimental", "Sad", "Romantic", "Emotional", "Ethereal", "Meditative", "Hypnotic", "Gentle Atmosphere", "Mystical", "Haunting", "Tragic", "Sombre Mood", "Nostalgic Melancholic Romantic"],
    "Energy": ["Uplifting", "Energetic", "Easygoing", "Soft Mellow Droning", "Higher Register", "Medium Tempo", "Low Pitched", "Slow Tempo", "Simple Melody", "Vibrant", "Upbeat", "Fun", "Groovy"],
    "Ambient": ["Nature Sounds", "Nature-Inspired", "Water Flowing", "Rain", "Birds Chirping", "Breeze Sounds", "Ambient", "Atmospheric", "Natural Environment", "Background Sound", "Chimes", "Rainfall and Water Flowing"]
}


# 初始化一个字典来存储分类结果
classified_instruments = {
    "Instrumental Focus": set(),
    "Atmospheric": set(),
    "Energy": set(),
    "Ambient": set(),
}


not_instruments = set()
# 分类函数
zzhsum = 0
def classify_instruments(instruments):
    global not_instruments
    global zzhsum
    te = set()
    for instrument in instruments:
        flag = 0
        # 将乐器名称转换为小写进行关键词匹配
        instrument_lower = instrument.lower()

        # 遍历每个类别及其关键词
        for category, keywords in categories.items():
            # 如果该乐器包含该类别的关键词，则将其加入该类别中
            if any(keyword.lower() in instrument_lower for keyword in keywords) or any(instrument_lower in keyword.lower() for keyword in keywords):
                classified_instruments[category].add(instrument)
                if flag == -1:
                    zzhsum += 1
                flag = -1
        if flag == 0:
            # print('zzh', instrument)
            te.add(instrument)
    print("\n no used", te)
    
# 进行分类
classify_instruments(instruments)

labels, values = [], []

# 打印分类结果
for category, instruments in classified_instruments.items():
    sum = 0
    for instrument in instruments:
        sum += instruments_counter[instrument]
    print(f"\n{category}: {sum}")
    labels.append(category.replace(" Instruments", ""))
    values.append(sum)


def plot_and_save_distribution_instrument(title, filename):
    sorted_indices = numpy.argsort(values)[::-1]  # 获取排序索引
    sorted_labels = [labels[i] for i in sorted_indices]
    sorted_values = [values[i] for i in sorted_indices]

    colors = ['#FCE6D5', '#FADBDF', '#F5B7BF', '#ADE5FF', '#D4F4F2', '#C8E5B3']
    bar_width = 0.4

    plt.figure(figsize=(10, 6))
    print(values)
    sorted_values = [int(i) for i in sorted_values]
    # 绘制条形图
    bar_plot = sns.barplot(x=sorted_labels, y=sorted_values, palette=colors, saturation=0.85, ci=None)

    # 添加数据标签
    for p in bar_plot.patches:
        bar_plot.annotate(int(p.get_height()), 
                          (p.get_x() + p.get_width() / 2., p.get_height()), 
                          ha='center', va='bottom', 
                          fontsize=18, color='black')

    # 设置标题和标签
    plt.title(title, fontsize=25, fontweight='bold', color='#0F1423')
    # plt.xlabel('Instrument Types', fontsize=14, color='#0F1423')
    # plt.ylabel('Frequency', fontsize=14, color='#0F1423')
    
    # 美化坐标轴
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    # plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(filename)  # 保存图像
    plt.show()
plot_and_save_distribution_instrument('Performance Style Distribution', 'Performance Style Distribution.png')
print(zzhsum)
