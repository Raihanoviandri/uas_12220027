#Nama : Raihan Oviandri
#NIM  : 12220027
#UAS Pemograman Komputer


#import library

import streamlit as st
import time
import numpy as np
import pandas as pd
import altair as alt

import inspect
import textwrap
from collections import OrderedDict
import streamlit as st
from streamlit.logger import get_logger

from PIL import Image

#-------create function def-------------
footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Created by 12220027 Raihan Oviandri</p>
</div>
"""

page_bg_img = '''
<style>
body {
background-image: url("https://static.vecteezy.com/system/resources/previews/000/080/280/original/sunset-oil-rig-background-vector.jpg");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown(footer,unsafe_allow_html=True)

# import & linking json with csv
df_kode_negara = pd.read_json("kode_negara_lengkap.json")
df_produksi = pd.read_csv("produksi_minyak_mentah.csv")
df = pd.merge(df_produksi,df_kode_negara,left_on='kode_negara',right_on='alpha-3')

list_negara = df["name"].unique().tolist()
list_negara.sort()

#home
def home():

    #box command
    st.sidebar.success("Please select the available features")

    image = Image.open('images.png')
    st.image(image, width=200)
    #desc
    st.markdown(

        """
        ### Streamlit produksi minyak mentah

        \n
        """
        
    )

#No 1.A
def no1a():

    data_negara = df["name"].unique().tolist()
    data_negara.sort()

    negara = st.sidebar.selectbox("Select country", data_negara)

    kode = df_kode_negara[(df_kode_negara["name"] == negara)]["alpha-3"].to_list()[0]
    df_states = df_produksi[(df_produksi.kode_negara == kode)].copy().set_index("tahun")
    st.subheader(f'Berikut adalah grafik berbentuk bar chart dari negara {negara}.')

    origin = df[(df["name"] == negara)]
    
    chart = alt.Chart(origin).mark_bar(opacity=1).encode(
        x='tahun:N',
        y='produksi'
    )
    st.altair_chart(chart, use_container_width=True)

    a = origin.set_index("tahun").rename(columns={"produksi": "Produksi"})["Produksi"]

#No 1.B
def no1b():

    #command control streamlit
    jumlah_negara = st.sidebar.selectbox("Pilih negara", range(1, len(list_negara)), 9)
    tahun = st.sidebar.selectbox("Pilih tahun", range(1971, 2016), 44)

    st.subheader(f'{jumlah_negara} besar negara dengan jumlah produksi terbesar pada tahun {tahun}')

    res = df[(df.tahun == tahun)][["name", "produksi"]].sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    res.index += 1

    source = res.iloc[:jumlah_negara]
    
    #making graph with altair
    bars = alt.Chart(source).mark_bar().encode(
        x=alt.Y(
                "name",
                sort=alt.EncodingSortField(field="produksi", order="descending"),
                title="Negara"),

        y='produksi'
        
            
    )


    text = bars.mark_text(
        align='left',
        baseline='middle',
        color='black',
        dx=3 
    ).encode(
        text='produksi'
    )
    chart = (bars).configure_view(
    strokeWidth=10
)
    
    st.altair_chart(chart, use_container_width=True)
    

#No 1.C
def no1c():

    #command control streamlit
    jumlah_negara = st.sidebar.selectbox("Pilih negara", range(1, len(list_negara)), 9)

    st.subheader(f'{jumlah_negara} besar negara dengan jumlah produksi keseluruhan terbesar')

    res = df[["name", "produksi"]].groupby(['name'])['produksi'].sum().reset_index().sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    res.index += 1

    source = res.iloc[:jumlah_negara]
    
    #making graph with altair
    bars = alt.Chart(source).mark_bar().encode(
        x='produksi',
        y=alt.Y(
                "name",
                sort=alt.EncodingSortField(field="produksi", order="descending"),
                title="Negara",
            )
    )


    text = bars.mark_text(
        align='left',
        baseline='middle',
        color='white',
        dx=3 
    ).encode(
        text='produksi'
    )
    chart = (bars+text).configure_view(
    strokeWidth=0
)
    
    st.altair_chart(chart, use_container_width=True)
    st.dataframe(source.rename(columns={"name": "Negara", "produksi":"Total Produksi"}))


#No 1.D
def no1d():

    #command control streamlit
    tahun = st.sidebar.selectbox("Pilih tahun", range(1971, 2016), 44)

    total_produksi = df.groupby(['name', 'kode_negara', 'region', 'sub-region'])['produksi'].sum().reset_index().sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    total_produksi_max = total_produksi[(total_produksi["produksi"] > 0)].iloc[0]
    total_produksi_min = total_produksi[(total_produksi["produksi"] > 0)].iloc[-1]
    total_produksi_nol = total_produksi[(total_produksi["produksi"] == 0)].sort_values(by=['name']).reset_index(drop=True)
    total_produksi_nol.index += 1

    produksi_tahun = df[(df["tahun"] == tahun)][['name', 'kode_negara', 'region', 'sub-region', 'produksi']].sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    produksi_tahun_max = produksi_tahun[(produksi_tahun["produksi"] > 0)].iloc[0]
    produksi_tahun_min = produksi_tahun[(produksi_tahun["produksi"] > 0)].iloc[-1]
    produksi_tahun_nol = produksi_tahun[(produksi_tahun["produksi"] == 0)].sort_values(by=['name']).reset_index(drop=True)
    produksi_tahun_nol.index += 1

    
    st.markdown(
        f"""
        #### Negara dengan total produksi keseluruhan tahun terbesar
        Negara: {total_produksi_max["name"]}\n
        Kode negara: {total_produksi_max["kode_negara"]}\n
        Region: {total_produksi_max["region"]}\n
        Sub-region: {total_produksi_max["sub-region"]}\n
        Jumlah produksi: {total_produksi_max["produksi"]}\n

        #### Negara dengan jumlah produksi terbesar pada tahun {tahun}  
        Negara: {produksi_tahun_max["name"]}\n
        Kode negara: {produksi_tahun_max["kode_negara"]}\n
        Region: {produksi_tahun_max["region"]}\n
        Sub-region: {produksi_tahun_max["sub-region"]}\n
        Jumlah produksi: {produksi_tahun_max["produksi"]}\n

        #### Negara dengan total produksi keseluruhan tahun terkecil
        Negara: {total_produksi_min["name"]}\n
        Kode negara: {total_produksi_min["kode_negara"]}\n
        Region: {total_produksi_min["region"]}\n
        Sub-region: {total_produksi_min["sub-region"]}\n
        Jumlah produksi: {total_produksi_min["produksi"]}\n

        #### Negara dengan jumlah produksi terkecil pada tahun {tahun}  
        Negara: {produksi_tahun_min["name"]}\n
        Kode negara: {produksi_tahun_min["kode_negara"]}\n
        Region: {produksi_tahun_min["region"]}\n
        Sub-region: {produksi_tahun_min["sub-region"]}\n
        Jumlah produksi: {produksi_tahun_min["produksi"]}\n
    """
    )
    st.markdown(
        """
        #### Negara dengan total produksi keseluruhan tahun sama dengan nol
        
    """
    )
    total_produksi_nol = total_produksi_nol.drop(['produksi'], axis=1).rename(columns={"name":"Negara", "kode_negara":"Kode Negara", "region":"Region", "sub-region":"Sub Region"})
    st.dataframe(total_produksi_nol)
    st.markdown(
        f"""
        #### Negara dengan jumlah produksi sama dengan nol pada tahun {tahun}
        
    """
    )
    produksi_tahun_nol = produksi_tahun_nol.drop(['produksi'], axis=1).rename(columns={"name":"Negara", "kode_negara":"Kode Negara", "region":"Region", "sub-region":"Sub Region"})
    st.dataframe(produksi_tahun_nol)

#panggil fungsi yang telah dibuat

LOGGER = get_logger(__name__)


FITUR = OrderedDict(
    [
        ("HOME", (home, None)),
        (
            "Soal Nomor 1.a",
            (
                no1a,
                """
                Grafik jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara
                """,
            ),
        ),
        (
            "Soal Nomor 1.b",
            (
                no1b,
                """
                Negara dengan produksi minyak mentah terbesar pada suatu tahun
                """,
            ),
        ),
        (
            "Soal Nomor 1.c",
            (
                no1c,
                """
                Negara dengan total produksi minyak mentah keseluruhan tahun terbesar
                """,
            ),
        ),
        (
            "Soal Nomor 1.d",
            (
                no1d,
                """
                Informasi tentang kesimpulan yang didapat:
                """,
            ),
        ),

    ]
)


def run():
    demo_name = st.sidebar.selectbox("Pilih fitur pada nomor", list(FITUR.keys()), 0)
    demo = FITUR[demo_name][0]
    if demo_name == "HOME":
        pass
    else:
        st.markdown("# %s" % demo_name)
        description = FITUR[demo_name][1]
        if description:
            st.write(description)

        for i in range(10):
            st.empty()

    demo()


if __name__ == "__main__":
    run()
