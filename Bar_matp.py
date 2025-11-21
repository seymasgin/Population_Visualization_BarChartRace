import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker
import numpy as np

# Excel verisini oku
df = pd.read_excel("nufus_pivot_2015_sonrasi.xlsx", index_col=0)
df.index.name = 'Yıl'

if 'Toplam' in df.columns:
    df = df.drop(columns='Toplam')

df = df.fillna(0)

years = df.index.tolist()
districts = df.columns.tolist()

# İlçelere özel sabit renk atama
base_colors = plt.cm.tab20.colors
if len(districts) > len(base_colors):
    cmap = plt.cm.get_cmap('tab20')
    district_colors = {district: cmap(i / len(districts)) for i, district in enumerate(districts)}
else:
    district_colors = {district: base_colors[i] for i, district in enumerate(districts)}

# Grafik boyutu ve eksen düzeni
fig = plt.figure(figsize=(12, 12), facecolor="#f7f7f7")
ax_main = fig.add_axes([0.2, 0.1, 0.6, 0.8], facecolor="#f7f7f7")  # ortalanmış eksen

max_value = df.values.max() * 1.1
ticks = np.linspace(0, max_value, 5)

def full_number_formatter(x, pos):
    return f"{int(round(x)):,}".replace(',', '.')

ax_main.set_xlim(0, max_value)
ax_main.set_xticks(ticks)
ax_main.xaxis.set_major_formatter(ticker.FuncFormatter(full_number_formatter))

def draw_bars(i):
    ax_main.clear()
    ax_main.set_facecolor("#f7f7f7")

    # Eksen çizgileri kaldır
    ax_main.spines['top'].set_visible(False)
    ax_main.spines['right'].set_visible(False)
    ax_main.spines['bottom'].set_visible(False)
    ax_main.spines['left'].set_visible(False)
    ax_main.grid(False)

    ax_main.set_xlim(0, max_value)
    ax_main.set_xticks(ticks)
    ax_main.xaxis.set_major_formatter(ticker.FuncFormatter(full_number_formatter))

    year = years[i]
    data = df.loc[year].sort_values()
    y_positions = [j * 1.5 for j in range(len(data))]
    colors = [district_colors[d] for d in data.index]
    ax_main.barh(y_positions, data.values, color=colors)
    ax_main.set_yticks(y_positions)
    ax_main.set_yticklabels(data.index, fontsize=10)

    for y_pos, value in zip(y_positions, data.values):
        ax_main.text(value, y_pos, f'{int(value):,}'.replace(',', '.'), va='center', ha='left', fontsize=8)

    for x in ticks:
        ax_main.axvline(x=x, color='lightgray', linewidth=0.7, alpha=0.3, zorder=0)

    ax_main.set_title("İstanbul İlçeleri Nüfusu Yıllık Değişimi", fontsize=18, pad=10, color='black')

    toplam_nufus = int(data.sum())
    y_middle = np.mean(y_positions)

    ax_main.text(
        max_value * 0.7,
        y_middle - 10,
        f"{year}",
        fontsize=30,
        color='dimgray',
        ha='left',
        va='center',
        fontweight='bold',
        bbox=dict(facecolor='#dcdcdc', alpha=0.7, edgecolor='none', pad=8)
    )

    ax_main.text(
        max_value * 0.7,
        y_middle - 15,
        f"Toplam: {toplam_nufus:,}".replace(',', '.'),
        fontsize=14,
        color='dimgray',
        ha='left',
        va='center',
        fontweight='semibold',
        bbox=dict(facecolor='#dcdcdc', alpha=0.7, edgecolor='none', pad=8)
    )

ani = animation.FuncAnimation(fig, draw_bars, frames=len(years), interval=1200, repeat=False)
ani.save("istanbul_ilceler_nufus.gif", writer="pillow", dpi=800)
plt.show()
