import pandas as pd
import bar_chart_race as bcr

# Excel dosyasını oku
df = pd.read_excel("nufus-bilgileri.xlsx")

# İlk 3 sütundan sonrakileri topla (satır bazında)
df["Toplam"] = df.iloc[:, 3:].sum(axis=1)

df_cleaned = df.drop(columns=[
    'Erkek ve 0-4', 'Erkek ve 5-9', 'Erkek ve 10-14', 'Erkek ve 15-19', 'Erkek ve 20-24', 'Erkek ve 25-29', 'Erkek ve 30-34',
    'Erkek ve 35-39', 'Erkek ve 40-44', 'Erkek ve 30-34', 'Erkek ve 45-49', 'Erkek ve 50-54', 'Erkek ve 55-59', 'Erkek ve 60-64', 'Erkek ve 65-69', 'Erkek ve 70-74',
    'Erkek ve 75-79', 'Erkek ve 80-84', 'Erkek ve 85-89', 'Erkek ve 90+', 'Kadın ve 0-4', 'Kadın ve 5-9', 'Kadın ve 10-14', 'Kadın ve 15-19', 'Kadın ve 20-24', 'Kadın ve 25-29', 'Kadın ve 30-34',
    'Kadın ve 35-39', 'Kadın ve 40-44', 'Kadın ve 30-34', 'Kadın ve 45-49', 'Kadın ve 50-54', 'Kadın ve 55-59', 'Kadın ve 60-64', 'Kadın ve 65-69', 'Kadın ve 70-74',
    'Kadın ve 75-79', 'Kadın ve 80-84', 'Kadın ve 85-89', 'Kadın ve 90+'
])

print(df_cleaned)

# 2015 ve sonrası verileri filtrele
df_filtered = df_cleaned[df_cleaned['Yıl'] >= 2015]

print(df_filtered.head())

# Pivot işlemi: Yıl satıra, ilçe sütuna, değer olarak Toplam
df_pivot = df_filtered.pivot(index='Yıl', columns='İlçe', values='Toplam')

# Eksik değerleri sıfırla ve yılları sırala
df_pivot = df_pivot.fillna(0).sort_index()
print(df_pivot.head())

# Satır bazında toplam hesapla ve 'Toplam' sütunu olarak ekle
df_pivot['Toplam'] = df_pivot.sum(axis=1)

# Kontrol et
print(df_pivot.head())

df_pivot.to_excel("nufus_pivot_2015_sonrasi.xlsx")


