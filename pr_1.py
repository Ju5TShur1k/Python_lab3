import matplotlib.pyplot as plt
import numpy as np

models = ["iPad Pro 12.9", "Samsung Galaxy Tab S9 Ultra", "Microsoft Surface Pro 9", "Xiaomi Pad 6"]
name_char = [
    "screen_size_in",
    "resolution_px",
    "ram_gb",
    "storage_gb",
    "battery_mah",
    "weight_g",
    "stylus_support",
    "price_rub"
]
char = [
    [12.9, "2732x2048", 16, 256, 10758, 682, True, 119990],
    [14.6, "2960x1848", 12, 256, 11200, 732, True, 99990],
    [13.0, "2880x1920", 16, 512, 5070, 891, True, 129990],
    [11.0, "2880x1800", 8, 256, 8840, 490, False, 39990],
]


def convert_resolution(res_str):
    width, height = map(int, res_str.split('x'))
    return width * height


def convert_stylus(stylus_bool):
    return 1 if stylus_bool else 0


def get_numeric_data():
    numeric_data = []
    for device in char:
        numeric_device = []
        for i, value in enumerate(device):
            if i == 1:  # resolution_px
                numeric_device.append(convert_resolution(value))
            elif i == 6:  # stylus_support
                numeric_device.append(convert_stylus(value))
            elif isinstance(value, (int, float)) and not isinstance(value, bool):
                numeric_device.append(value)
        numeric_data.append(numeric_device)
    return numeric_data


def get_normal(char):
    normal = []
    numeric_char = get_numeric_data()

    for item in numeric_char:
        normal.append([a / b for a, b in zip(item, numeric_char[0])])
    return normal


def get_quality(normal):
    result = []
    for item in normal:
        result.append(round(sum(item) / len(item), 2))
    return result


def create_bar(name, values):
    plt.figure(figsize=(10, 6))
    bars = plt.bar(name, values, color=['skyblue', 'skyblue', 'skyblue', 'skyblue'])
    plt.xlabel("Модель", fontsize=12)
    plt.ylabel("Kту", fontsize=12)
    plt.title("Интегральный показатель качества", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                 f'{value:.2f}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()


def create_radial(models, name, values):
    values_copy = [item.copy() for item in values]
    for item in values_copy:
        item += item[:1]
    angles = np.linspace(0, 2 * np.pi, len(name), endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection="polar"))
    colors = ['blue', 'green', 'red', 'orange']
    for i in range(len(values_copy)):
        ax.plot(angles, values_copy[i], 'o-', linewidth=2, label=models[i], color=colors[i])
        ax.fill(angles, values_copy[i], alpha=0.1, color=colors[i])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(name, fontsize=10)
    ax.set_ylim(0, 2)
    ax.set_yticks([0.5, 1.0, 1.5, 2.0])
    ax.set_yticklabels(['0.5', '1.0', '1.5', '2.0'], fontsize=8)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.0))
    plt.title("Сравнение относительных характеристик", pad=20, fontsize=14)
    plt.tight_layout()
    plt.show()


numeric_data = get_numeric_data()
normalized_data = get_normal(char)
data = get_quality(get_normal(char))
create_bar(models, data)
create_radial(models, name_char, normalized_data)