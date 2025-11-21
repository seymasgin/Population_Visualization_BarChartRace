import pandas as pd
import bar_chart_race as bcr



# Veriyi oku
df = pd.read_excel("nufus_pivot_2015_sonrasi.xlsx", index_col=0)
df.index.name = 'Yıl'

# 'Toplam' sütununu kaldır
if 'Toplam' in df.columns:
    df = df.drop(columns='Toplam')

df = df.fillna(0)

# 2015 ve 2024 verileri
yil_2015 = df.loc[2015] if 2015 in df.index else df.loc['2015']
yil_2024 = df.loc[2024] if 2024 in df.index else df.loc['2024']

# Değişim hesapla
degisim = (yil_2024 - yil_2015).abs()
n = 15
en_fazla_degisen_ilceler = degisim.sort_values(ascending=False).head(n).index.tolist()
df_filtered = df[en_fazla_degisen_ilceler]

# Yıl indeksini string yap
df_filtered.index = [f"{year}" for year in df.index]

# Bar chart race çizimi
bcr.bar_chart_race(
    df=df_filtered,
    filename='istanbul_degisim_en_fazla.gif',
    orientation='h',
    sort='desc',
    n_bars=n,
    fixed_order=False,
    fixed_max=True,
    steps_per_period=20,
    period_length=1500,
    title=f'2015-2024 Arası Nüfusu En Fazla Değişen {n} İstanbul İlçesi',
    bar_size=.95,
    dpi=300,
    figsize=(6, 3.5),
    tick_label_size=4,
    bar_label_size=5,
    period_label={'x': .95, 'y': .15, 'ha': 'right', 'va': 'center', 'fontsize': 24},

)
