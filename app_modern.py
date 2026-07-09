import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(
    page_title="Dashboard PERKIN 2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

/* ===== Background ===== */

.stApp{
    background:#F5F8FD;
}

/* Hilangkan menu */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    background:transparent !important;
}

/* ===== Sidebar ===== */

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#0C2D68,#0B4EA2);
}

[data-testid="stSidebar"]{
    min-width:280px;
    max-width:280px;
}

[data-testid="stSidebar"] *{
    color:white;
}

/* tombol sidebar */

.menu-box{

background:rgba(255,255,255,.10);

padding:16px;

border-radius:14px;

margin-bottom:12px;

font-size:18px;

font-weight:600;

transition:.3s;

}

.menu-active{

background:#2F80ED;

box-shadow:0 10px 25px rgba(0,0,0,.25);

}

/* HEADER */

.header-card{

background:linear-gradient(135deg,#0B4EA2,#1F7AE0);

border-radius:28px;

padding:28px 35px;

box-shadow:0 15px 35px rgba(0,0,0,.12);

margin-bottom:20px;

margin-top:-18px;

position:relative;

overflow:hidden;

color:white;

}

/* FILTER */

.filter-card{

background:white;

border-radius:20px;

padding:18px 22px;

box-shadow:0 8px 20px rgba(0,0,0,.08);

height:115px;

display:flex;

flex-direction:column;

justify-content:center;

}

/* KPI */

.kpi-card{

background:white;

border-radius:18px;

padding:20px;

box-shadow:0 5px 18px rgba(0,0,0,.08);

text-align:center;

transition:.3s;

}

.kpi-card:hover{

transform:translateY(-5px);

}

.kpi-icon{

font-size:40px;

}

.kpi-title{

font-size:15px;

color:#666;

margin-top:8px;

}

.kpi-value{

font-size:34px;

font-weight:bold;

color:#0C2D68;

}

/* CARD */

.chart-card{

background:white;

padding:20px;

border-radius:20px;

box-shadow:0 5px 18px rgba(0,0,0,.08);

margin-top:20px;

}

.info-card{

background:white;

padding:25px;

border-radius:20px;

box-shadow:0 5px 18px rgba(0,0,0,.08);

margin-top:20px;

}

/* ============================
KPI CARD MODERN
============================ */

.kpi-card{

background:white;

border-radius:20px;

padding:22px;

box-shadow:0 8px 22px rgba(0,0,0,.08);

height:160px;

display:flex;

align-items:center;

gap:18px;

}

.kpi-card:hover{

transform:translateY(-8px);

}

.kpi-icon{

width:60px;

height:60px;

border-radius:50%;

display:flex;

align-items:center;

justify-content:center;

font-size:28px;

margin-bottom:18px;

}

.kpi-title{

color:#666;

font-size:15px;

}

.kpi-value{

font-size:34px;

font-weight:bold;

color:#0B4EA2;

margin-top:8px;

}

/* =============================
CHART CARD
============================= */

.chart-card{

background:white;

border-radius:22px;

padding:20px;

box-shadow:0 10px 25px rgba(0,0,0,.08);

margin-top:25px;

}

.chart-title{

font-size:22px;

font-weight:700;

color:#123B7A;

margin-bottom:15px;

}

/* FOOTER */

.footer{

background:#0C2D68;

padding:18px;

color:white;

border-radius:15px;

margin-top:25px;

text-align:center;

}

/* =====================================
RANKING CARD
===================================== */

.rank-card{

background:white;

border-radius:22px;

padding:25px;

box-shadow:0 10px 25px rgba(0,0,0,.08);

margin-top:25px;

}

.badge-gold{

background:#FFD700;
padding:6px 12px;
border-radius:30px;
font-weight:bold;

}

.badge-silver{

background:#D9D9D9;
padding:6px 12px;
border-radius:30px;
font-weight:bold;

}

.badge-bronze{

background:#D08C3F;
color:white;
padding:6px 12px;
border-radius:30px;
font-weight:bold;

}

/* ==================================
INFO CARD
================================== */

.info-card{

background:white;

border-radius:22px;

padding:25px;

box-shadow:0 10px 25px rgba(0,0,0,.08);

margin-top:25px;

}

/* STATUS */

.status-bagus{

background:#DFF7E8;

color:#0A7D32;

padding:8px 18px;

border-radius:30px;

font-weight:bold;

display:inline-block;

}

.status-sedang{

background:#FFF4D6;

color:#CC8400;

padding:8px 18px;

border-radius:30px;

font-weight:bold;

display:inline-block;

}

.status-buruk{

background:#FFE3E3;

color:#D92D20;

padding:8px 18px;

border-radius:30px;

font-weight:bold;

display:inline-block;

}

/* FOOTER */

.footer{

margin-top:40px;

padding:25px;

border-radius:20px;

background:linear-gradient(90deg,#0B4EA2,#1976D2);

color:white;

text-align:center;

}           

</style>
""", unsafe_allow_html=True)

sheet_id="13TQ-GJ9cpEkLmDhfi31bcgs5GmZGNBvpLJIrjQeddc8"

bulan_sheet={

"Januari":"JAN",
"Februari":"FEB",
"Maret":"MAR",
"April":"APRIL",
"Mei":"MEI",
"Juni":"JUNI",
"Juli":"JULI",
"Agustus":"AGS",
"September":"SEP",
"Oktober":"OKT",
"November":"NOV",
"Desember":"DES"

}

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.image(
        "logo_bkkbn.png",
        width=180
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="menu-box menu-active">
    🏠 Dashboard
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="menu-box">
    📊 Data Indikator
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="menu-box">
    ℹ️ Tentang PERKIN
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
    background:rgba(255,255,255,.08);
    border-radius:20px;
    padding:20px;
    text-align:center;
    ">

    <img width="90"
    src="https://cdn-icons-png.flaticon.com/512/3048/3048398.png">

    <br><br>

    <b>
    Berencana Itu Keren
    </b>

    <br>

    Cegah Stunting,
    Itu Penting

    </div>
    """, unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================

col1, col2 = st.columns([8,2])

with col1:

    st.markdown(f"""
    <div class="header-card">


<h1 style="
color:white;
font-size:50px;
font-weight:700;
margin-bottom:2px;
line-height:1.1;">

    Dashboard PERKIN 2026

    </h1>

<div style="
color:#EAF3FF;
font-size:18px;
margin-top:4px;">

    Kementerian Kependudukan dan
    Pembangunan Keluarga / BKKBN

    </div>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.image(
        "logo_bkkbn_biru.png",
        width=150
    )

# ======================================================
# FILTER
# ======================================================

k1, k2 = st.columns(2)

with k1:

    st.markdown("""
<b style="font-size:18px;color:#143B7A;">
📅 Pilih Bulan
</b>
""",unsafe_allow_html=True)

bulan = st.selectbox(
"",
list(bulan_sheet.keys()),
label_visibility="collapsed"
)

  

with k2:

    nama_sheet = bulan_sheet[bulan]

    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nama_sheet}"

    df = pd.read_csv(url)

    df.columns = df.columns.str.strip()

    df["Indikator"] = df["Indikator"].astype(str).str.strip()

    df["Kabupaten"] = df["Kabupaten"].astype(str).str.strip()

    df["Target"] = pd.to_numeric(df["Target"], errors="coerce")

    df["Realisasi"] = pd.to_numeric(df["Realisasi"], errors="coerce")

    st.markdown("""
    <div class="filter-card">
    """, unsafe_allow_html=True)

    indikator = st.selectbox(
        "📊 Pilih Indikator",
        sorted(df["Indikator"].unique())
    )

    st.markdown("</div>", unsafe_allow_html=True)

df_filter = df[df["Indikator"] == indikator].copy()

df_filter["Capaian"] = (
    df_filter["Realisasi"] /
    df_filter["Target"] * 100
).fillna(0).round(2)

# ======================================================
# HITUNG KPI
# ======================================================

total_target = df_filter["Target"].sum()

total_realisasi = df_filter["Realisasi"].sum()

persentase = (
    total_realisasi / total_target * 100
    if total_target > 0 else 0
)

jumlah_kabupaten = df_filter["Kabupaten"].nunique()

# ======================================================
# KPI CARD
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

c1,c2,c3,c4=st.columns(4)

with c1:

    st.markdown(f"""

<div class="kpi-card">

<div class="kpi-icon"
style="background:#D9ECFF;">
🎯
</div>

<div class="kpi-title">

Total Target

</div>

<div class="kpi-value">

{total_target:,.0f}

</div>

</div>

""",unsafe_allow_html=True)

with c2:

    st.markdown(f"""

<div class="kpi-card">

<div class="kpi-icon"
style="background:#DCFCE7;">
✅
</div>

<div class="kpi-title">

Total Realisasi

</div>

<div class="kpi-value">

{total_realisasi:,.0f}

</div>

</div>

""",unsafe_allow_html=True)

with c3:

    st.markdown(f"""

<div class="kpi-card">

<div class="kpi-icon"
style="background:#FFF4D8;">
📈
</div>

<div class="kpi-title">

Persentase

</div>

<div class="kpi-value">

{persentase:.2f}%

</div>

</div>

""",unsafe_allow_html=True)

with c4:

    st.markdown(f"""

<div class="kpi-card">

<div class="kpi-icon"
style="background:#F5E4FF;">
🏛
</div>

<div class="kpi-title">

Kabupaten/Kota

</div>

<div class="kpi-value">

{jumlah_kabupaten}

</div>

</div>

""",unsafe_allow_html=True)

# ======================================================
# TARGET VS REALISASI
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

kiri, kanan = st.columns([2,1])

with kiri:

    st.markdown("""
    <div class="chart-card">
    <div class="chart-title">
    📊 Target vs Realisasi
    </div>
    """, unsafe_allow_html=True)

    df_bar = pd.melt(

        df_filter,

        id_vars=["Kabupaten"],

        value_vars=["Target","Realisasi"],

        var_name="Kategori",

        value_name="Nilai"

    )

    fig1 = px.bar(

        df_bar,

        x="Kabupaten",

        y="Nilai",

        color="Kategori",

        barmode="group",

        text="Nilai",

        color_discrete_map={

            "Target":"#0B5ED7",

            "Realisasi":"#34A853"

        }

    )

    fig1.update_traces(

        texttemplate="%{text:,.0f}",

        textposition="outside"

    )

    fig1.update_layout(

        height=470,

        plot_bgcolor="white",

        paper_bgcolor="white",

        legend_title="",

        margin=dict(

            l=15,
            r=15,
            t=15,
            b=15

        ),

        xaxis_title="",

        yaxis_title="Jumlah"

    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

with kanan:

    st.markdown("""
    <div class="chart-card">
    <div class="chart-title">
    🎯 Ringkasan
    </div>
    """, unsafe_allow_html=True)

    donut = pd.DataFrame({

        "Kategori":[
            "Target",
            "Realisasi"
        ],

        "Nilai":[
            total_target,
            total_realisasi
        ]

    })

    fig2 = px.pie(

        donut,

        names="Kategori",

        values="Nilai",

        hole=.72,

        color="Kategori",

        color_discrete_map={

            "Target":"#0B5ED7",

            "Realisasi":"#34A853"

        }

    )

    fig2.update_layout(

        height=400,

        showlegend=True,

        paper_bgcolor="white",

        margin=dict(
            l=0,
            r=0,
            t=10,
            b=0
        )

    )

    fig2.update_traces(

        textinfo="percent+label"

    )

    st.plotly_chart(

        fig2,

        use_container_width=True

    )

    st.markdown(f"""

    <h1 style="text-align:center;
               color:#0B5ED7;
               margin-top:-15px;">

    {persentase:.2f}%

    </h1>

    <p style="text-align:center;
              color:gray;">

    Total Capaian

    </p>

    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ======================================================
# PERSENTASE CAPAIAN
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="chart-card">
<div class="chart-title">
📈 Persentase Capaian Kabupaten/Kota
</div>
""", unsafe_allow_html=True)

fig3 = px.bar(

    df_filter.sort_values(

        "Capaian",

        ascending=False

    ),

    x="Kabupaten",

    y="Capaian",

    color="Capaian",

    text="Capaian",

    color_continuous_scale="Blues"

)

fig3.update_traces(

    texttemplate="%{text:.2f}%",

    textposition="outside"

)

fig3.update_layout(

    height=500,

    plot_bgcolor="white",

    paper_bgcolor="white",

    coloraxis_showscale=False,

    margin=dict(

        l=20,
        r=20,
        t=15,
        b=15

    ),

    xaxis_title="",

    yaxis_title="Persentase (%)",

    yaxis_range=[0,110]

)

st.plotly_chart(

    fig3,

    use_container_width=True

)

st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# SEARCH
# ======================================================

cari = st.text_input(

    "🔍 Cari Kabupaten/Kota"

)

if cari != "":

    df_filter = df_filter[
        df_filter["Kabupaten"].str.contains(
            cari,
            case=False,
            na=False
        )
    ]

# ======================================================
# RANKING KABUPATEN
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="rank-card">

<h3>
🏆 Ranking Kabupaten/Kota
</h3>

""", unsafe_allow_html=True)

ranking = df_filter.sort_values(
    "Capaian",
    ascending=False
).reset_index(drop=True)

ranking.index += 1

st.dataframe(

    ranking[[
        "Kabupaten",
        "Target",
        "Realisasi",
        "Capaian"
    ]].style.format({

        "Target":"{:,.0f}",

        "Realisasi":"{:,.0f}",

        "Capaian":"{:.2f}%"

    }),

    use_container_width=True,

    hide_index=False

)

st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# DOWNLOAD
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""

<div class="rank-card">

<h3>

📥 Download Laporan

</h3>

""", unsafe_allow_html=True)

d1,d2,d3 = st.columns(3)

with d1:

    csv = ranking.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(

        "⬇ Download CSV",

        csv,

        f"PERKIN_{bulan}.csv",

        "text/csv",

        use_container_width=True

    )

with d2:

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        ranking.to_excel(
            writer,
            index=False
        )

    st.download_button(

        "📊 Download Excel",

        output.getvalue(),

        f"PERKIN_{bulan}.xlsx",

        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        use_container_width=True

    )

with d3:

    st.info("📄 PDF akan ditambahkan pada tahap berikutnya.")

st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# TENTANG INDIKATOR
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

left,right=st.columns([2,1])

with left:

    st.markdown("""

<div class="info-card">

<h3>

📌 Tentang Indikator

</h3>

""",unsafe_allow_html=True)

    st.markdown(f"""

### {indikator}

Dashboard ini menampilkan perkembangan capaian indikator PERKIN
berdasarkan data yang berasal dari Google Sheets secara **realtime**.

Nilai capaian dihitung menggunakan rumus:

> **Realisasi / Target × 100%**

Semakin tinggi persentasenya, maka semakin baik pencapaian indikator.

""")

    if persentase >= 100:

        st.markdown("""
<div class="status-bagus">
🟢 Target Tercapai
</div>
""",unsafe_allow_html=True)

    elif persentase >= 80:

        st.markdown("""
<div class="status-sedang">
🟡 Perlu Sedikit Peningkatan
</div>
""",unsafe_allow_html=True)

    else:

        st.markdown("""
<div class="status-buruk">
🔴 Perlu Perhatian
</div>
""",unsafe_allow_html=True)

    st.progress(min(persentase/100,1.0))

    st.markdown("</div>",unsafe_allow_html=True)

with right:

    st.markdown("""

<div class="info-card">

<h3>

💡 Insight

</h3>

""",unsafe_allow_html=True)

    terbaik = ranking.iloc[0]

    terendah = ranking.iloc[-1]

    st.metric(
        "Kabupaten Terbaik",
        terbaik["Kabupaten"]
    )

    st.metric(
        "Persentase",
        f'{terbaik["Capaian"]:.2f}%'
    )

    st.divider()

    st.metric(
        "Perlu Perhatian",
        terendah["Kabupaten"]
    )

    st.metric(
        "Persentase",
        f'{terendah["Capaian"]:.2f}%'
    )

    st.markdown("</div>",unsafe_allow_html=True)

# ======================================================
# FOOTER
# ======================================================

st.markdown("<br>",unsafe_allow_html=True)

st.markdown(f"""

<div class="footer">

<h2>

Dashboard PERKIN 2026

</h2>

<p>

Kementerian Kependudukan dan Pembangunan Keluarga

<br>

BKKBN Provinsi Kepulauan Bangka Belitung

</p>

<hr style="opacity:.3;">

<div style="display:flex;
justify-content:space-around;
flex-wrap:wrap;">

<div>

📊

<br>

Realtime Google Sheets

</div>

<div>

⚡

<br>

Streamlit Dashboard

</div>

<div>

📈

<br>

Plotly Interactive

</div>

<div>

❤️

<br>

Developed for Monitoring PERKIN

</div>

</div>

<br>

<small>

© 2026 BKKBN Provinsi Kepulauan Bangka Belitung

</small>

</div>

""",unsafe_allow_html=True)
