import streamlit as st
import pandas as pd
from datetime import date
import time
from streamlit_extras.metric_cards import style_metric_cards
import numpy as np

## Read
sheet_url = "https://docs.google.com/spreadsheets/d/1fwOqEmIXqRq43hjELFF61DpxNkYIdk7vK_mzoM-NfWM/edit#gid=0"
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
df = pd.read_csv(url_1, on_bad_lines='skip')

st.set_page_config(page_title="siAnom 5102",
        page_icon="🌴",
        layout="wide"
        )

## Sidebar
with st.sidebar:
    st.title("🌴 siAnom 5102")
    lstKategori = list(df["Kategori"].unique())
    lstKategori.insert(0, "Pilih Kategori")
                
    FirstFilter = st.selectbox("Kategori", lstKategori, 0)

    if FirstFilter != "Pilih Kategori":
        df2 = df[df["Kategori"] == FirstFilter]  

        lstAnomali = list(df2["Anomali"].unique())
        lstAnomali.insert(0, "Pilih Anomali")

        SecondFilter = st.selectbox("Anomali", lstAnomali, 0)

if FirstFilter != "Pilih Kategori" and SecondFilter != "Pilih Anomali":

    sheet_url2 = df2[df2["Anomali"] == SecondFilter].iloc[0,2]
    url_2 = sheet_url2.replace('/edit#gid=', '/export?format=csv&gid=')
    df3 = pd.read_csv(url_2, on_bad_lines='skip')
    df3.iloc[:,:-3] = df3.iloc[:,:-3].applymap(str)

    st.title(df2[df2["Anomali"] == SecondFilter].iloc[0,1])

    columns = st.multiselect("Kolom:", df3.columns)

    lstKec = list(df3["kec"].unique())
    lstKec.insert(0, "PILIH KECAMATAN")

    filter = st.selectbox("Kecamatan", lstKec, 0)

    if filter != "PILIH KECAMATAN":
        df3 = df3[df3["kec"] == filter]
    
    df4 = df3[columns]
    df4.index = np.arange(1, len(df4) + 1)

    col1, col2 = st.columns(2)
    p1 = df3['Sudah Diperbaiki'].sum()
    p2 = df3['Sudah di entry'].sum()

    n1 = len(df3['Sudah Diperbaiki'])
    n2 = len(df3['Sudah di entry'])

    m1 = int(round(p1/n1 * 100, 2))
    m2 = int(round(p2/n2 * 100, 2))

    col1.metric(label = "Persentase Sudah Diperbaiki", value = f"{str(m1)} %")
    col2.metric(label = "Persentase Sudah Dientry", value = f"{str(m2)} %")
    style_metric_cards(border_left_color = '#1E1E1E')
    
    if len(columns) > 0:

        st.checkbox("Use container width", value=False, key="use_container_width")
        st.dataframe(df4, use_container_width=st.session_state.use_container_width)
