import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style='dark')

def total_count_day(data_day):
    day_count=data_day.groupby(by="weekday").cnt.sum().sort_values(ascending=False).reset_index()
    day_count.rename(columns={
        "cnt":"order_count"
    },inplace=True)
    return day_count

def total_count_weather(data_hour):
    weather_count=data_hour.groupby(by="weathersit").cnt.sum().sort_values(ascending=False).reset_index()
    weather_count.rename(columns={
        "cnt":"order_count"
    },inplace=True)
    return weather_count

def regis_monthly_orders(data_day):
    #Resample data menjadi bulanan untuk Registered
    monthly_orders_regis=data_day.resample(rule='ME', on='dteday').agg({
    "registered": ["sum"],
    })
    monthly_orders_regis.index = monthly_orders_regis.index.strftime('%Y-%m')
    monthly_orders_regis = monthly_orders_regis.reset_index()
    monthly_orders_regis.rename(columns={
    "registered": "order_registered",
    }, inplace=True)
    return monthly_orders_regis

def cas_monthly_orders(data_day):
    #Resample data menjadi bulanan untuk casual
    monthly_orders_cas = data_day.resample(rule='ME', on='dteday').agg({
    "casual": "sum",
    })
    monthly_orders_cas.index = monthly_orders_cas.index.strftime('%Y-%m')
    monthly_orders_cas = monthly_orders_cas.reset_index()
    monthly_orders_cas.rename(columns={
    "casual": "order_casual",
    }, inplace=True)
    return monthly_orders_cas

def create_bytemp(data_hour):
    sum_order_item_temp=data_hour.groupby(by="temp_category").cnt.sum().sort_values(ascending=False).reset_index()
    sum_order_item_temp.rename(columns={
        "cnt":"order_count"
    },inplace=True)
    return sum_order_item_temp

def create_bytime(data_hour):
    sum_order=data_hour.groupby(by="hour_category").cnt.sum().sort_values(ascending=False).reset_index()
    sum_order.rename(columns={
        "cnt":"order_count"
    },inplace=True)
    return sum_order

data_day=pd.read_csv("dashboard/data_dayclean.csv")
data_hour=pd.read_csv("dashboard/data_hourclean.csv")

datetime_columns = ["dteday"]
data_day.sort_values(by="dteday", inplace=True)
data_day.reset_index(inplace=True)   

data_hour.sort_values(by="dteday", inplace=True)
data_hour.reset_index(inplace=True)

for column in datetime_columns:
    data_day[column] = pd.to_datetime(data_day[column])
    data_hour[column] = pd.to_datetime(data_hour[column])

min_date_days = data_day["dteday"].min()
max_date_days = data_day["dteday"].max()

min_date_hour = data_hour["dteday"].min()
max_date_hour = data_hour["dteday"].max()
with st.sidebar:
    # Menambah gambar
    st.image("https://savvycyclist.co/wp-content/uploads/2023/04/lady-on-a-bicycle-with-big-butt-scaled-800x400.jpeg")
    
    # Mengambil start_date & end_date 
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
    
#Filter data
main_day = data_day[(data_day["dteday"] >= str(start_date)) & 
                (data_day["dteday"] <= str(end_date))]
main_hour = data_hour[(data_hour["dteday"] >= str(start_date)) & 
                (data_hour["dteday"] <= str(end_date))]

day_count= total_count_day(main_day)
weather_count=total_count_weather(main_hour)
regis_monthly_count=regis_monthly_orders(main_day)
cas_monthly_count=cas_monthly_orders(main_day)
temp_count=create_bytemp(main_hour)
time_count=create_bytime(main_hour)

#Filling dashboard
st.header('Bike Sharing Dashboard :man-biking:')

st.subheader('Monthly Casual and Registered Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    total_registered_orders = regis_monthly_count.order_registered.sum()
    st.metric("Registered orders", value=total_registered_orders)
 
with col2:
    total_cas_orders = cas_monthly_count.order_casual.sum()
    st.metric("Casual orders", value=total_cas_orders)

#Plotting
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(regis_monthly_count["dteday"], regis_monthly_count["order_registered"],label="Registered", marker='o', linewidth=2, color="#72BCD4") 
ax.plot(cas_monthly_count["dteday"], cas_monthly_count["order_casual"],label="Casual", marker='o', linewidth=2, color="#FFA500") 
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='x',rotation=45)
ax.legend()
st.pyplot(fig)

#By Days
st.subheader("Highest & Lowest Order Days")
fig, ax = plt.subplots(figsize=(30, 10))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3","#EE4B2B"] 
sns.barplot(
    y="weekday", 
    x="order_count",
    data=day_count.sort_values(by="order_count", ascending=False),
    palette=colors
)
ax.set_ylabel(None)
ax.set_xlabel("Number of Order", fontsize=30)
ax.set_title("Highest & Lowest Days", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)

#By Season
st.subheader("Highest Order Season")
fig, ax= plt.subplots(figsize=(30,10))
sns.barplot(
    y="order_count", 
    x="weathersit",
    data=weather_count.sort_values(by="order_count", ascending=False),
    palette=colors
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title("Highest Season", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)

#By Temp
st.subheader("Highest Order Temperature")
fig,ax=plt.subplots(figsize=(30,10))
sns.barplot(
    y="temp_category", 
    x="order_count",
    data=temp_count.sort_values(by="order_count", ascending=False),
    palette=colors
)
ax.set_ylabel(None)
ax.set_xlabel("Number of Order", fontsize=30)
ax.set_title("Highest Order Temperature", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)
#By Time
st.subheader("Highest Order Time")
fig,ax=plt.subplots(figsize=(30,10))
sns.barplot(
    y="order_count", 
    x="hour_category",
    data=time_count.sort_values(by="order_count", ascending=False),
    palette=colors
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title("Highest Order Time", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)



