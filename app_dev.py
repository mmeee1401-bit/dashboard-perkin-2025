import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================

st.set_page_config(
    page_title="Dashboard PERKIN 2026",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# CSS
# ======================================================

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

header{
visibility:hidden;
}

footer{
visibility:hidden;
}

.stApp{
background:#F4F8FC;
}

/* HEADER */

.header-box{

background:linear-gradient(135deg,#0B5ED7,#2F80ED);

padding:30px;

border-radius:20px;

box-shadow:0px 8px 25px rgba(0,0,0,.15);

margin-bottom:25px;

}

.header-title{

font-size:42px;

font-weight:700;

color:white;

margin-bottom:5px;

}

.header-sub{

font-size:18px;

color:white;

opacity:.9;

}

/* FILTER */

.filter-box{

background:white;

padding:18px;

border-radius:18px;

box-shadow:0 5px 15px rgba(0,0,0,.08);

margin-bottom:25px;

}

/* KPI */

.kpi{

background:white;

border-radius:18px;

padding:22px;

box-shadow:0 8px 18px rgba(0,0,0,.08);

text-align:center;

transition:.25s;

}

.kpi:hover{

transform:translateY(-5px);

}

.kpi-icon{

font-size:38px;

}

.kpi-title{

font-size:16px;

color:#777;

}

.kpi-value{

font-size:34px;

font-weight:bold;

color:#0B5ED7;

}

/* CARD */

.card{

background:white;

padding:20px;

border-radius:18px;

box-shadow:0 6px 18px rgba(0,0,0,.08);

margin-top:20px;

}

</style>
""", unsafe_allow_html=True)

# ======================================================
# GOOGLE SHEETS
# ======================================================

sheet_id = "13TQ-GJ9cpEkLmDhfi31bcgs5GmZGNBvpLJIrjQeddc8"

bulan_sheet = {
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
# LOAD DATA
# ======================================================

@st.cache_data(show_spinner=False)

def load_data(sheet_name):

    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

    df = pd.read_csv(url)

    df.columns = df.columns.str.strip()

    df["Indikator"] = df["Indikator"].astype(str).str.strip()

    df["Kabupaten"] = df["Kabupaten"].astype(str).str.strip()

    df["Target"] = pd.to_numeric(df["Target"], errors="coerce")

    df["Realisasi"] = pd.to_numeric(df["Realisasi"], errors="coerce")

    return df

# ======================================================
# HEADER
# ======================================================

col_logo,col_title=st.columns([1,8])

with col_logo:

    st.image(
        "logo_bkkbn.png",
        width=90
    )

with col_title:

    st.markdown("""

<div class="header-box">

<div class="header-title">

Dashboard PERKIN 2026

</div>

<div class="header-sub">

Monitoring Kinerja Program

<br>

Kementerian Kependudukan dan Pembangunan Keluarga / BKKBN

</div>

</div>

""", unsafe_allow_html=True)

# ======================================================
# FILTER
# ======================================================

st.markdown("<div class='filter-box'>", unsafe_allow_html=True)

c1,c2=st.columns(2)

with c1:

    bulan=st.selectbox(
        "📅 Pilih Bulan",
        list(bulan_sheet.keys())
    )

with c2:

    nama_sheet=bulan_sheet[bulan]

    df=load_data(nama_sheet)

    indikator=st.selectbox(
        "📊 Pilih Indikator",
        sorted(df["Indikator"].unique())
    )

st.markdown("</div>", unsafe_allow_html=True)

df_filter=df[df["Indikator"]==indikator].copy()

df_filter["Capaian"]=(
df_filter["Realisasi"]/
df_filter["Target"]*100
).fillna(0).round(2)
# ======================================================
# KPI
# ======================================================

total_target = df_filter["Target"].sum()

total_realisasi = df_filter["Realisasi"].sum()

persentase = (
    (total_realisasi / total_target) * 100
    if total_target > 0 else 0
)

jumlah_kabupaten = df_filter["Kabupaten"].nunique()

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# =============================
# KPI 1
# =============================

with col1:

    st.markdown(f"""
    <div class="kpi">

        <div class="kpi-icon">🎯</div>

        <div class="kpi-title">
        Total Target
        </div>

        <div class="kpi-value">
        {total_target:,.0f}
        </div>

    </div>
    """, unsafe_allow_html=True)

# =============================
# KPI 2
# =============================

with col2:

    st.markdown(f"""
    <div class="kpi">

        <div class="kpi-icon">✅</div>

        <div class="kpi-title">
        Total Realisasi
        </div>

        <div class="kpi-value">
        {total_realisasi:,.0f}
        </div>

    </div>
    """, unsafe_allow_html=True)

# =============================
# KPI 3
# =============================

with col3:

    warna = "#16A34A"

    if persentase < 80:
        warna = "#DC2626"

    elif persentase < 100:
        warna = "#F59E0B"

    st.markdown(f"""
    <div class="kpi">

        <div class="kpi-icon">📈</div>

        <div class="kpi-title">
        Persentase Capaian
        </div>

        <div
        class="kpi-value"
        style="color:{warna};">

        {persentase:.2f}%

        </div>

    </div>
    """, unsafe_allow_html=True)

# =============================
# KPI 4
# =============================

with col4:

    st.markdown(f"""
    <div class="kpi">

        <div class="kpi-icon">🏛️</div>

        <div class="kpi-title">
        Kabupaten/Kota
        </div>

        <div class="kpi-value">
        {jumlah_kabupaten}
        </div>

    </div>
    """, unsafe_allow_html=True)

# ======================================================
# GRAFIK 1
# TARGET VS REALISASI
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<h3 style="margin-top:0;">
📊 Target vs Realisasi per Kabupaten/Kota
</h3>
""", unsafe_allow_html=True)

df_bar = pd.melt(
    df_filter,
    id_vars=["Kabupaten"],
    value_vars=["Target", "Realisasi"],
    var_name="Kategori",
    value_name="Nilai"
)

fig = px.bar(
    df_bar,
    x="Kabupaten",
    y="Nilai",
    color="Kategori",
    barmode="group",
    text="Nilai",
    color_discrete_map={
        "Target":"#0B5ED7",
        "Realisasi":"#2ECC71"
    }
)

fig.update_traces(

    texttemplate="%{text:,.0f}",

    textposition="outside",

    marker_line_width=0,

    marker=dict(
        line=dict(width=0)
    )

)

fig.update_layout(

    height=550,

    plot_bgcolor="white",

    paper_bgcolor="white",

    legend_title="",

    font=dict(
        family="Segoe UI",
        size=13
    ),

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    xaxis=dict(

        title="Kabupaten/Kota",

        showgrid=False,

        tickangle=-20

    ),

    yaxis=dict(

        title="Jumlah",

        gridcolor="#ECECEC"

    )

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# ROW 2
# PERSENTASE & DONUT CHART
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([2,1])

# ======================================================
# GRAFIK PERSENTASE
# ======================================================

with left:

    st.markdown("""
    <div class="card">
    <h3>📈 Persentase Capaian (%)</h3>
    """, unsafe_allow_html=True)

    fig2 = px.bar(
        df_filter.sort_values("Capaian", ascending=False),
        x="Kabupaten",
        y="Capaian",
        text="Capaian",
        color="Capaian",
        color_continuous_scale="Blues"
    )

    fig2.update_traces(

        texttemplate="%{text:.2f}%",
        textposition="outside"

    )

    fig2.update_layout(

        height=500,

        plot_bgcolor="white",

        paper_bgcolor="white",

        coloraxis_showscale=False,

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        xaxis=dict(
            title="Kabupaten/Kota",
            tickangle=-20
        ),

        yaxis=dict(
            title="Persentase (%)",
            range=[0,110]
        )

    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# DONUT CHART
# ======================================================

with right:

    st.markdown("""
    <div class="card">
    <h3>🍩 Ringkasan</h3>
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

    fig3 = px.pie(

        donut,

        names="Kategori",

        values="Nilai",

        hole=.65,

        color="Kategori",

        color_discrete_map={

            "Target":"#0B5ED7",

            "Realisasi":"#2ECC71"

        }

    )

    fig3.update_layout(

        height=420,

        showlegend=True,

        margin=dict(
            l=10,
            r=10,
            t=20,
            b=20
        )

    )

    fig3.update_traces(

        textinfo="percent+label"

    )

    st.plotly_chart(

        fig3,

        use_container_width=True

    )

    st.markdown(f"""

    <div style="text-align:center;
                margin-top:-15px;">

    <h2 style="color:#0B5ED7;">
    {persentase:.2f}%
    </h2>

    <p>Total Capaian</p>

    </div>

    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# DOWNLOAD DATA
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<h3>📥 Download Data</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# ============================
# Download CSV
# ============================

with col1:

    csv = tampil.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name=f"PERKIN_{bulan}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ============================
# Download Excel
# ============================

with col2:

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        tampil.to_excel(
            writer,
            index=False,
            sheet_name="PERKIN"
        )

    st.download_button(
        label="📊 Download Excel",
        data=output.getvalue(),
        file_name=f"PERKIN_{bulan}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.markdown("</div>", unsafe_allow_html=True)

cari = st.text_input("🔍 Cari Kabupaten/Kota")

if cari:
    tampil = tampil[
        tampil["Kabupaten"].str.contains(
            cari,
            case=False,
            na=False
        )
    ]
# ======================================================
# DOWNLOAD PDF
# ======================================================

from reportlab.pdfgen import canvas

def create_pdf():

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 800, "Dashboard PERKIN 2026")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, 770, f"Bulan : {bulan}")
    pdf.drawString(50, 750, f"Indikator : {indikator}")

    pdf.drawString(50, 715, f"Total Target : {total_target:,.0f}")
    pdf.drawString(50, 695, f"Total Realisasi : {total_realisasi:,.0f}")
    pdf.drawString(50, 675, f"Persentase : {persentase:.2f}%")
    pdf.drawString(50, 655, f"Jumlah Kabupaten : {jumlah_kabupaten}")

    pdf.line(50,640,550,640)

    y = 615

    pdf.setFont("Helvetica-Bold",10)

    pdf.drawString(50,y,"Kabupaten")
    pdf.drawString(220,y,"Target")
    pdf.drawString(330,y,"Realisasi")
    pdf.drawString(460,y,"Capaian")

    y -= 20

    pdf.setFont("Helvetica",9)

    for _, row in tampil.iterrows():

        pdf.drawString(50,y,str(row["Kabupaten"]))
        pdf.drawString(220,y,f'{row["Target"]:,.0f}')
        pdf.drawString(330,y,f'{row["Realisasi"]:,.0f}')
        pdf.drawString(470,y,f'{row["Capaian"]:.2f}%')

        y -= 18

        if y < 60:
            pdf.showPage()
            y = 800

    pdf.save()

    buffer.seek(0)

    return buffer

pdf_file = create_pdf()

st.download_button(

    "📄 Download PDF",

    data=pdf_file,

    file_name=f"Dashboard_PERKIN_{bulan}.pdf",

    mime="application/pdf",

    use_container_width=True

)
# ======================================================
# FOOTER
# ======================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""

---

<div style="text-align:center;
padding:25px;">

<h4 style="color:#0B5ED7;">
Dashboard PERKIN 2026
</h4>

<p style="color:#666;">

Kementerian Kependudukan dan Pembangunan Keluarga /
BKKBN Provinsi Kepulauan Bangka Belitung

</p>

<p style="color:#999;font-size:14px;">

📊 Realtime Data • Google Sheets • Streamlit • Plotly

</p>

</div>

""", unsafe_allow_html=True)
