import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import matplotlib
matplotlib.use('Agg')  # Atau 'Cairo'
import matplotlib.pyplot as plt

# Dataframe contoh (gantilah dengan data Anda)
data = pd.read_csv("main_data.csv")


# Judul halaman
st.set_page_config(page_title="Dashboard",layout="wide")
st.header("ANALYTICS E-COMMERCE DASHBOARD")

def Home():
    #compute top analytics
    TotalCus = float(pd.Series(data['customer_id']).nunique())
    mostRecency = float(pd.Series(data['recency']).max())
    mostFrequency = float(pd.Series(data['frequency']).max())
    mostMonetary = float(pd.Series(data['monetary']).max()) 
    mostCity = data['customer_city'].value_counts().idxmax()

    total1,total2,total3,total4,total5=st.columns(5,gap='small')
    with total1:
        st.info('Total Custommer',icon="👤")
        st.metric(label="Sum E-Commerce",value=f"{TotalCus:.0f}")

    with total2:
        st.info('Most Recency',icon="⌛")
        st.metric(label="Recency E-Commerce",value=f"{mostRecency:,.0f}")

    with total3:
        st.info('Most Frequency',icon="🔍")
        st.metric(label="Frequency E-Commerce",value=f"{mostFrequency:,.0f}")

    with total4:
        st.info('Most Monetary',icon="💰")
        st.metric(label="Median E-Commerce",value=f"{mostMonetary:,.0f}")

    with total5:
        st.info('city with the most shopping',icon="⭐")
        st.metric(label="Customer City",value=f"{mostCity}")
    

def MostProduct():
  # Buat daftar pilihan kota
  city_options = data['customer_city'].unique().tolist()


  # Pilih kota dari dropdown (tambahkan key unik)
  selected_city = st.selectbox('Pilih Kota', city_options, key='select_city')  # Unique key
  selected_city = "sao paulo"

  # Filter data berdasarkan kota terpilih
  filterCity = data.set_index('customer_city').loc[selected_city]

  # Kelompokkan berdasarkan kategori produk dan hitung total item terjual
  top5Product = filterCity.groupby('product_category_name')['quantity'].sum().nlargest(5)

  # Buat plot batang
  fig, ax = plt.subplots(figsize=(10, 5))
  ax.bar(top5Product.index, top5Product.values, color='skyblue')
  ax.set_xlabel('Nama Produk')
  ax.set_ylabel('Jumlah Terjual')
  ax.set_title(f'5 Produk Terbanyak di {selected_city}')
  # ax.set_xticks(rotation=45)
  plt.tight_layout()

  # Tampilkan plot di Streamlit
  st.pyplot(fig)



def RateCustomer():
    ratingCus = data['review_score'].value_counts().sort_values(ascending=False)
    hightScore = ratingCus.idxmax()
    cmap = plt.get_cmap("Blues")

    # Create a bar chart with different colors for the highest value
    fig, ax = plt.subplots(figsize=(12, 7))  # Create a Figure and Axes object
    ax.bar(range(1, len(ratingCus.values) + 1), ratingCus.values, color=cmap(ratingCus.values / max(ratingCus.values)))

    # Add value labels to each bar
    for i in range(len(ratingCus.values)):
        ax.text(i + 1, ratingCus.values[i], str(ratingCus.values[i]), ha='center', va='bottom')

    # Customize x-axis labels
    ax.set_xticks(range(1, len(ratingCus.index) + 1))
    ax.set_xticklabels(ratingCus.index)

    plt.title("Rating customers", fontsize=15)
    plt.xlabel("Rate")
    plt.ylabel("Customer")
    plt.xticks(fontsize=12)

    # Display the plot in Streamlit
    st.pyplot(fig)


# Call the function
Home()
col1, col2 = st.columns(2)
with col1:
    MostProduct()
with col2:
    RateCustomer()
