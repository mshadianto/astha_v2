# ===== app/pages/01_🏠_Dashboard.py =====
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.api_service import APIService
from utils.formatters import format_rupiah, format_percentage
from components.metrics import render_kpi_cards, render_trend_chart
from components.charts import create_liability_projection_chart

st.set_page_config(
    page_title="Dashboard - ASTHA",
    page_icon="🏠",
    layout="wide"
)

def main():
    st.title("🏠 Dashboard Monitoring Keberlanjutan")
    
    # Initialize services
    api_service = APIService()
    
    # Get real-time data
    with st.spinner("📡 Mengambil data real-time..."):
        exchange_rates = api_service.get_exchange_rates()
        economic_indicators = api_service.get_economic_indicators()
    
    # Display last update time
    st.caption(f"⏰ Terakhir diperbarui: {datetime.now().strftime('%d %B %Y, %H:%M WIB')}")
    
    # Main KPI metrics
    render_kpi_cards()
    
    # Real-time indicators
    st.subheader("📊 Indikator Ekonomi Real-time")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_usd = "↗️ 0.5%" if exchange_rates.get('USD', 15500) > 15400 else "↘️ 0.3%"
        st.metric(
            "💵 USD/IDR", 
            f"Rp {exchange_rates.get('USD', 15500):,}",
            delta_usd
        )
    
    with col2:
        delta_sar = "↗️ 0.3%" if exchange_rates.get('SAR', 4133) > 4100 else "↘️ 0.2%"
        st.metric(
            "🇸🇦 SAR/IDR", 
            f"Rp {exchange_rates.get('SAR', 4133):,}",
            delta_sar
        )
    
    with col3:
        st.metric(
            "📈 Inflasi Saudi", 
            f"{economic_indicators.get('saudi_inflation', 3.2)}%",
            "↘️ 0.2%"
        )
    
    with col4:
        st.metric(
            "🏦 BI Rate", 
            f"{economic_indicators.get('bi_rate', 6.0)}%",
            "→ 0%"
        )
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        render_trend_chart()
    
    with col2:
        # Jemaah distribution pie chart
        st.subheader("🗺️ Sebaran Jemaah per Provinsi")
        provinces_data = {
            'Provinsi': ['Jawa Barat', 'Jawa Timur', 'Jawa Tengah', 'Sumatera Utara', 'Lampung', 'Lainnya'],
            'Jemaah': [420000, 380000, 340000, 180000, 160000, 1020000]
        }
        df_provinces = pd.DataFrame(provinces_data)
        
        fig = px.pie(
            df_provinces, 
            values='Jemaah', 
            names='Provinsi',
            title="Distribusi 2.5M Jemaah Tunggu",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Alert system
    st.subheader("🚨 Sistem Peringatan Dini")
    
    # Check for alerts based on current metrics
    alerts = []
    solvency_ratio = 1.24
    ytd_return = 8.2
    
    if solvency_ratio < 1.1:
        alerts.append({
            'level': 'danger',
            'title': 'Rasio Solvabilitas Rendah',
            'message': f'Rasio solvabilitas {solvency_ratio:.2f} mendekati batas minimum.'
        })
    
    if ytd_return < 5.0:
        alerts.append({
            'level': 'warning', 
            'title': 'Imbal Hasil di Bawah Target',
            'message': f'Imbal hasil YTD {ytd_return}% di bawah target 6.5%.'
        })
    
    if exchange_rates.get('USD', 15500) > 16000:
        alerts.append({
            'level': 'warning',
            'title': 'Kurs USD Tinggi',
            'message': 'Kurs USD/IDR melampaui level waspada Rp 16.000.'
        })
    
    if not alerts:
        st.success("✅ Semua indikator dalam kondisi normal")
    else:
        for alert in alerts:
            if alert['level'] == 'danger':
                st.error(f"🚨 **{alert['title']}**: {alert['message']}")
            else:
                st.warning(f"⚠️ **{alert['title']}**: {alert['message']}")
    
    # Auto-refresh option
    if st.button("🔄 Refresh Data", type="primary"):
        st.cache_data.clear()
        st.rerun()

if __name__ == "__main__":
    main()
