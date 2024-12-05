import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
sns.set(style='dark')

st.set_page_config(page_title="Air Pollution from Dongsi Analysis by Benedictus Ryu")
st.title('Air Pollution Analysis Dashboard: Dongsi Station')
st.markdown("""
### About Me
- **Name**: Benedictus Ryu Gunawan
- **Email Address**: benedictusryugunawan@gmail.com
- **Dicoding ID**: Benedictus Ryu Gunawan
""")

months = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "../Data/FINISHED_Dongsi_df.csv")
dongsi_df = pd.read_csv(file_path)

def dongsi_year_PM(df,PM):
    dongsi_year_PM_df = df.groupby(by="year").agg({
        PM: "mean",
    }) 
    return dongsi_year_PM_df

def dongsi_date_PM(df,PM):
    dongsi_date_PM_df = df.groupby(by="datetime").agg({
        PM: "mean",
    }) 
    return dongsi_date_PM_df

def dongsi_substance(df,substance):
    dongsi_substance_df = df.groupby(by="month").agg({substance: "mean"})
    dongsi_substance_df.index = dongsi_substance_df.index.map(months)
    return dongsi_substance_df

# Menambahkan kolom untuk date
dongsi_df['datetime'] = pd.to_datetime(dongsi_df[['year', 'month', 'day']])
print(dongsi_df)

min_date = dongsi_df["datetime"].min()
max_date = dongsi_df["datetime"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.subheader("User Input:")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = dongsi_df[(dongsi_df["datetime"] >= str(start_date)) & (dongsi_df["datetime"] <= str(end_date))]

dongsi_SO2_df = dongsi_substance(dongsi_df,"SO2")
dongsi_NO2_df = dongsi_substance(dongsi_df,"NO2")
dongsi_CO_df = dongsi_substance(dongsi_df,"CO")
dongsi_O3_df = dongsi_substance(dongsi_df,"O3")
dongsi_year_PM25_df = dongsi_year_PM(dongsi_df,"PM2.5")
dongsi_year_PM10_df = dongsi_year_PM(dongsi_df,"PM10")
dongsi_date_PM25_df = dongsi_date_PM(main_df,"PM2.5")
dongsi_date_PM10_df = dongsi_date_PM(main_df,"PM10")
corr_df = pd.DataFrame({
    "SO2": main_df["SO2"],
    "NO2": main_df["NO2"],
    "CO": main_df["CO"],
    "O3": main_df["O3"],
    "PM2.5": main_df["PM2.5"],
    "PM10": main_df["PM10"]
})

st.markdown("<h5 style='text-align: center;'>Air Pollution Trend Based on PM2.5 and PM10 in Dongsi Station </h5>", unsafe_allow_html=True)

# Data Visual 1
fig, axes = plt.subplots(2, figsize=(12, 10))
axes[0].plot(dongsi_date_PM25_df, marker='.', linewidth=0.5, color="red")
axes[1].plot(dongsi_date_PM10_df, marker='.', linewidth=0.5, color="blue")
st.pyplot(fig)

# Data Visual 2
st.markdown("<h5 style='text-align: center;'>Pollutant Substance Correlation with Pollutant Matter (PM) </h5>", unsafe_allow_html=True)
correlation_matrix = corr_df.corr()
fig = plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="YlOrBr", fmt=".2f", linewidths=0.5)
st.pyplot(fig)

# Data Visual 3
st.markdown("<h5 style='text-align: center;'>Air Pollution Trend Based on PM2.5 and PM10 in Dongsi Station (By Year) </h5>", unsafe_allow_html=True)
fig = plt.figure(figsize=(10, 5))
plt.plot(dongsi_year_PM25_df, marker='o', linewidth=2, color="red")
plt.ylim([0, 150])

for i, row in dongsi_year_PM25_df.iterrows():
    plt.annotate(f'{round(row['PM2.5'],2)}', (i,row['PM2.5']), textcoords="offset points", xytext=(0, 10), ha='center')

plt.plot(dongsi_year_PM10_df, marker='o', linewidth=2, color="blue")

for i, row in dongsi_year_PM10_df.iterrows():
    plt.annotate(f'{round(row['PM10'],2)}', (i,row['PM10']), textcoords="offset points", xytext=(0, 10), ha='center')

x_ticks = np.arange(dongsi_year_PM25_df.index.min(), dongsi_year_PM25_df.index.max() + 1, 1)
plt.xticks(ticks=x_ticks, labels=x_ticks)
plt.legend(['PM2.5','PM10']) 
st.pyplot(fig)
 
st.markdown("<br>", unsafe_allow_html=True)
 
# Data Visual 4
st.markdown("<h5 style='text-align: center;'>Average Monthly Pollutant Substance in Dongsi Station</h5>", unsafe_allow_html=True)
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

so2_bar = axes[0, 0].bar(dongsi_SO2_df.index, dongsi_SO2_df["SO2"], color="red")
for bar in so2_bar:
    axes[0, 0].text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=12)

axes[0, 0].set_title("Average Monthly SO2 Levels")
axes[0, 0].set_ylabel("SO2 Mean")
axes[0, 0].set_xlabel("Month")
axes[0, 0].tick_params(axis='x', rotation=45) 

no2_bar = axes[0, 1].bar(dongsi_NO2_df.index, dongsi_NO2_df["NO2"], color="blue")
for bar in no2_bar:
    axes[0, 1].text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=12)

axes[0, 1].set_title("Average Monthly NO2 Levels")
axes[0, 1].set_ylabel("NO2 Mean")
axes[0, 1].set_xlabel("Month")
axes[0, 1].tick_params(axis='x', rotation=45) 

co_bar = axes[1, 0].bar(dongsi_CO_df.index, dongsi_CO_df["CO"], color="yellow")
for bar in co_bar:
    axes[1, 0].text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=9)

axes[1, 0].set_title("Average Monthly CO Levels")
axes[1, 0].set_ylabel("CO Mean")
axes[1, 0].set_xlabel("Month")
axes[1, 0].tick_params(axis='x', rotation=45) 

o3_bar = axes[1, 1].bar(dongsi_O3_df.index, dongsi_O3_df["O3"], color="green")
for bar in o3_bar:
    axes[1, 1].text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=12)

axes[1, 1].set_title("Average Monthly O3 Levels")
axes[1, 1].set_ylabel("O3 Mean")
axes[1, 1].set_xlabel("Month")
axes[1, 1].tick_params(axis='x', rotation=45)  

plt.tight_layout()
st.pyplot(fig)


 
# Conclusion
st.markdown("""
### Conclusion:
  - PM2.5 and PM10 air pollution levels tend to remain stable but experienced a significant increase in 2017.  
- PM2.5 and PM10 values have a positive correlation.  
- The month influences pollutant levels.  
- The SO2 graph shows a decrease in SO2 gas levels until August, followed by an increase in September.  
- The NO2 graph is relatively fluctuating during the first three months, stabilizes over the next five months, and increases in September and October.  
- The CO graph indicates a decline until April, then stabilizes until August, and rises from September to December.  
- The O3 graph forms a normal distribution pattern, with levels increasing on average until May, stabilizing over the next three months, and experiencing a sharp decline in September.  
""")

 