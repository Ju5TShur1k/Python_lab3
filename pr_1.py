import matplotlib.pyplot as plt
import numpy as np


tablets_compact = [
    {
        "model": "iPad Pro 12.9",
        "screen_size_in": 12.9,
        "resolution_px": "2732x2048",
        "ram_gb": 16,
        "storage_gb": 256,
        "battery_mah": 10758,
        "weight_g": 682,
        "stylus_support": True,
        "price_rub": 119990,
    },
    {
        "model": "Samsung Galaxy Tab S9 Ultra",
        "screen_size_in": 14.6,
        "resolution_px": "2960x1848",
        "ram_gb": 12,
        "storage_gb": 256,
        "battery_mah": 11200,
        "weight_g": 732,
        "stylus_support": True,
        "price_rub": 99990,
    },
    {
        "model": "Microsoft Surface Pro 9",
        "screen_size_in": 13.0,
        "resolution_px": "2880x1920",
        "ram_gb": 16,
        "storage_gb": 512,
        "battery_mah": 5070,
        "weight_g": 891,
        "stylus_support": True,
        "price_rub": 129990,
    },
    {
        "model": "Xiaomi Pad 6",
        "screen_size_in": 11.0,
        "resolution_px": "2880x1800",
        "ram_gb": 8,
        "storage_gb": 256,
        "battery_mah": 8840,
        "weight_g": 490,
        "stylus_support": False,
        "price_rub": 39990,
    },
]

models = [t["model"] for t in tablets_compact]

name_char = [
    "Размер экрана (дюймы)",
    "Разрешение (пиксели)",
    "ОЗУ (ГБ)",
    "ПЗУ (ГБ)",
    "Батарея (мАч)",
    "Вес (обратный)",
    "Цена (обратная)",
    "Поддержка стилуса"
]


def convert_resolution(res_str):
    width, height = map(int, res_str.split('x'))
    return width * height


def convert_stylus(stylus_bool):
    return 1 if stylus_bool else 0


char = []
for tablet in tablets_compact:
    row = [
        tablet["screen_size_in"],
        convert_resolution(tablet["resolution_px"]),
        tablet["ram_gb"],
        tablet["storage_gb"],
        tablet["battery_mah"],
        1000 / tablet["weight_g"],
        100000 / tablet["price_rub"],
        convert_stylus(tablet["stylus_support"])
    ]
    char.append(row)


def get_normal(char):

    normal = []
    for item in char:

        normalized_row = []
        for i, (a, b) in enumerate(zip(item, char[0])):
            if i in [5, 6]:
                normalized_row.append(b / a if a != 0 else 0)
            else:
                normalized_row.append(a / b if b != 0 else 0)
        normal.append(normalized_row)
    return normal


def get_quality(normal):

    result = []
    for item in normal:
        result.append(round(sum(item) / len(item), 2))
    return result


def create_bar(name, values):

    plt.figure(figsize=(12, 7))
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    bars = plt.bar(name, values, color=colors[:len(name)])

    plt.xlabel("Модель планшета", fontsize=12)
    plt.ylabel("Kту (коэффициент качества)", fontsize=12)
    plt.title("Сравнение планшетов по интегральному показателю качества", fontsize=14)
    plt.xticks(rotation=15, ha='right', fontsize=10)
    plt.grid(axis='y', alpha=0.3)


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
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']


    all_values = [val for sublist in values for val in sublist]
    max_value = max(all_values) * 1.1  # Добавляем 10% запаса

    for i in range(len(values_copy)):
        ax.plot(angles, values_copy[i], "o-", linewidth=2,
                label=models[i], color=colors[i % len(colors)])
        ax.fill(angles, values_copy[i], alpha=0.15, color=colors[i % len(colors)])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(name, fontsize=10, ha='center')
    ax.set_ylim(0, max_value)
    ax.set_yticks(np.linspace(0, max_value, 5))
    ax.set_yticklabels([f'{x:.1f}' for x in np.linspace(0, max_value, 5)], fontsize=8)
    ax.grid(True, alpha=0.3)

    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.0), fontsize=10)
    plt.title("Сравнение относительных характеристик планшетов", pad=20, fontsize=14)
    plt.tight_layout()
    plt.show()



print("Матрица характеристик:")
for i, row in enumerate(char):
    print(f"{models[i]}: {row}")

print("\nНормализованные данные:")
normalized_data = get_normal(char)
for i, row in enumerate(normalized_data):
    print(f"{models[i]}: {[round(x, 3) for x in row]}")


data = get_quality(normalized_data)
print(f"\nИнтегральные показатели качества:")
for model, value in zip(models, data):
    print(f"{model}: {value}")

create_bar(models, data)
create_radial(models, name_char, normalized_data)