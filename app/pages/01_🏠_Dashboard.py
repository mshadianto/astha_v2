"""
Dashboard.py - Main Dashboard untuk ASTHA HAJJ ANALYTICS
Updated version dengan perbaikan import dan fitur lengkap
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Dashboard - ASTHA HAJJ ANALYTICS",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Path setup untuk import components
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
app_root = current_file.parent.parent

# Add paths to sys.path
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(app_root))

# Import components dengan error handling
try:
    from services.api_service import APIService
except ImportError:
    # Mock API service jika tidak ada
    class APIService:
        def get_exchange_rates(self):
            return {'USD': 15485, 'SAR': 4129, 'EUR': 16250}
        
        def get_economic_indicators(self):
            return {
                'saudi_inflation': 3.2,
                'bi_rate': 6.0,
                'indonesia_inflation': 2.8,
                'saudi_gdp_growth': 3.1
            }

try:
    from utils.formatters import format_rupiah, format_percentage
except ImportError:
    # Mock formatters
    def format_rupiah(amount):
        return f"Rp {amount:,.0f}"
    
    def format_percentage(value):
        return f"{value:.2f}%"

try:
    from components.metrics import render_kpi_cards, render_trend_chart
except ImportError:
    # Mock functions akan didefinisikan di bawah
    pass

try:
    from components.charts import create_liability_projection_chart
except ImportError:
    # Mock function
    def create_liability_projection_chart(data):
        return None

try:
    from components.sidebar import render_sidebar
except ImportError:
    # Simple sidebar fallback
    def render_sidebar():
        st.sidebar.title("🕌 ASTHA HAJJ ANALYTICS")
        st.sidebar.markdown("---")
        
        # Navigation buttons
        if st.sidebar.button("🏠 Dashboard", use_container_width=True, type="primary"):
            st.rerun()
        
        if st.sidebar.button("🧮 Liability Calculator", use_container_width=True):
            st.switch_page("pages/02_🧮_Liability_Calculator.py")
        
        if st.sidebar.button("📊 Simulation", use_container_width=True):
            st.switch_page("pages/03_📊_Simulation.py")
        
        if st.sidebar.button("🤖 AI Assistant", use_container_width=True):
            st.switch_page("pages/04_🤖_AI_Assistant.py")
        
        if st.sidebar.button("📈 Analytics", use_container_width=True):
            st.switch_page("pages/05_📈_Analytics.py")
        
        if st.sidebar.button("📋 Reports", use_container_width=True):
            st.switch_page("pages/06_📋_Reports.py")

# Mock functions untuk components yang mungkin tidak ada
def render_kpi_cards():
    """Render KPI cards untuk dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Dana Kelola",
            value="Rp 47.8 T",
            delta="2.3% dari bulan lalu",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="👥 Jemaah Tunggu",
            value="2.5 Juta",
            delta="-15,420 dari tahun lalu",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="📊 Rasio Solvabilitas",
            value="124%",
            delta="4% dari quarter lalu",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="📈 Imbal Hasil YTD",
            value="8.2%",
            delta="↗️ 0.8% dari target",
            delta_color="normal"
        )

def render_trend_chart():
    """Render trend chart untuk dashboard"""
    st.subheader("📈 Tren Dana Kelola & Jemaah (12 Bulan)")
    
    # Generate sample data
    months = pd.date_range(start='2023-07-01', end='2024-06-30', freq='M')
    dana_kelola = [45.2, 45.8, 46.1, 46.7, 47.0, 47.2, 47.5, 47.8, 47.6, 47.9, 48.1, 47.8]
    jemaah_tunggu = [2.65, 2.62, 2.58, 2.55, 2.52, 2.50, 2.48, 2.46, 2.44, 2.42, 2.41, 2.50]
    
    # Create subplot with secondary y-axis
    fig = make_subplots(
        specs=[[{"secondary_y": True}]],
        subplot_titles=("Tren Dana Kelola dan Jemaah Tunggu",)
    )
    
    # Add dana kelola trend
    fig.add_trace(
        go.Scatter(
            x=months,
            y=dana_kelola,
            name="Dana Kelola (T)",
            line=dict(color='#2E8B57', width=3),
            mode='lines+markers'
        ),
        secondary_y=False,
    )
    
    # Add jemaah trend
    fig.add_trace(
        go.Scatter(
            x=months,
            y=jemaah_tunggu,
            name="Jemaah Tunggu (Juta)",
            line=dict(color='#FFD700', width=3),
            mode='lines+markers'
        ),
        secondary_y=True,
    )
    
    # Update layout
    fig.update_layout(
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=400
    )
    
    # Set y-axes titles
    fig.update_yaxes(
        title_text="Dana Kelola (Triliun Rp)",
        secondary_y=False
    )
    fig.update_yaxes(
        title_text="Jemaah Tunggu (Juta Orang)",
        secondary_y=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_portfolio_allocation():
    """Render alokasi portofolio"""
    st.subheader("🏦 Alokasi Portofolio Dana Haji")
    
    # Sample portfolio data
    portfolio_data = {
        'Instrumen': [
            'Sukuk Negara', 'Deposito Syariah', 'Saham Syariah',
            'Sukuk Korporasi', 'Emas', 'Properti', 'Lainnya'
        ],
        'Alokasi': [45.2, 25.8, 12.5, 8.3, 4.2, 2.8, 1.2],
        'Nilai': [21.6, 12.3, 6.0, 4.0, 2.0, 1.3, 0.6]
    }
    
    df_portfolio = pd.DataFrame(portfolio_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart alokasi
        fig_pie = px.pie(
            df_portfolio, 
            values='Alokasi', 
            names='Instrumen',
            title="Persentase Alokasi (%)",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart nilai
        fig_bar = px.bar(
            df_portfolio.sort_values('Nilai', ascending=True),
            x='Nilai',
            y='Instrumen',
            orientation='h',
            title="Nilai Investasi (Triliun Rp)",
            color='Nilai',
            color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

def render_risk_metrics():
    """Render metrik risiko"""
    st.subheader("⚠️ Metrik Risiko & Compliance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Value at Risk gauge
        var_value = 2.8
        fig_var = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = var_value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "VaR 99% (%)"},
            delta = {'reference': 3.0},
            gauge = {
                'axis': {'range': [None, 5]},
                'bar': {'color': "#FF6347"},
                'steps': [
                    {'range': [0, 2], 'color': "lightgreen"},
                    {'range': [2, 3.5], 'color': "yellow"},
                    {'range': [3.5, 5], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 3.0
                }
            }
        ))
        fig_var.update_layout(height=300)
        st.plotly_chart(fig_var, use_container_width=True)
    
    with col2:
        # Sharpe Ratio
        sharpe = 1.42
        st.metric("📊 Sharpe Ratio", f"{sharpe:.2f}", "↗️ 0.12")
        
        # Maximum Drawdown
        max_dd = -3.2
        st.metric("📉 Max Drawdown", f"{max_dd}%", "↗️ 0.5%")
    
    with col3:
        # Compliance Score
        compliance = 96.8
        st.metric("✅ Compliance Score", f"{compliance}%", "↗️ 1.2%")
        
        # ESG Rating
        esg_rating = "A+"
        st.metric("🌱 ESG Rating", esg_rating, "→ Stable")
    
    with col4:
        # Liquidity Ratio
        liquidity = 18.5
        st.metric("💧 Liquidity Ratio", f"{liquidity}%", "↘️ 2.1%")
        
        # Duration
        duration = 4.2
        st.metric("⏱️ Duration", f"{duration} years", "→ 0.1")

def render_regional_distribution():
    """Render distribusi regional yang lebih detail"""
    st.subheader("🗺️ Distribusi Jemaah & Setoran per Provinsi")
    
    # Sample data yang lebih lengkap
    regional_data = {
        'Provinsi': [
            'Jawa Barat', 'Jawa Timur', 'Jawa Tengah', 'Sumatera Utara', 
            'DKI Jakarta', 'Lampung', 'Sumatera Selatan', 'Banten',
            'Sumatera Barat', 'Kalimantan Selatan', 'Jawa', 'Lainnya'
        ],
        'Jemaah': [420000, 380000, 340000, 180000, 160000, 150000, 140000, 130000, 120000, 110000, 90000, 680000],
        'Setoran_Bulanan': [1.2, 1.1, 0.95, 0.52, 0.48, 0.42, 0.38, 0.35, 0.32, 0.28, 0.25, 1.74],
        'Rata_Setoran': [2.86, 2.89, 2.79, 2.89, 3.00, 2.80, 2.71, 2.69, 2.67, 2.55, 2.78, 2.56]
    }
    
    df_regional = pd.DataFrame(regional_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Horizontal bar chart jemaah
        fig_jemaah = px.bar(
            df_regional.head(10).sort_values('Jemaah', ascending=True),
            x='Jemaah',
            y='Provinsi',
            orientation='h',
            title="Top 10 Provinsi - Jumlah Jemaah Tunggu",
            color='Jemaah',
            color_continuous_scale='Blues',
            text='Jemaah'
        )
        fig_jemaah.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_jemaah.update_layout(height=500)
        st.plotly_chart(fig_jemaah, use_container_width=True)
    
    with col2:
        # Scatter plot setoran vs jemaah
        fig_scatter = px.scatter(
            df_regional,
            x='Jemaah',
            y='Setoran_Bulanan',
            size='Rata_Setoran',
            color='Rata_Setoran',
            hover_name='Provinsi',
            title="Korelasi Jemaah vs Setoran Bulanan",
            labels={
                'Jemaah': 'Jumlah Jemaah',
                'Setoran_Bulanan': 'Setoran Bulanan (T Rp)',
                'Rata_Setoran': 'Rata-rata Setoran (Juta Rp)'
            },
            color_continuous_scale='Viridis'
        )
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)

def render_market_alerts():
    """Render sistem peringatan pasar"""
    st.subheader("🚨 Sistem Peringatan Dini")
    
    # Ambil data real-time
    api_service = APIService()
    exchange_rates = api_service.get_exchange_rates()
    economic_indicators = api_service.get_economic_indicators()
    
    # Check untuk berbagai alerts
    alerts = []
    
    # Currency alerts
    usd_rate = exchange_rates.get('USD', 15485)
    sar_rate = exchange_rates.get('SAR', 4129)
    
    if usd_rate > 16000:
        alerts.append({
            'level': 'danger',
            'title': '💱 Kurs USD Tinggi',
            'message': f'USD/IDR {usd_rate:,} melampaui batas waspada Rp 16.000',
            'action': 'Pertimbangkan hedging mata uang'
        })
    elif usd_rate > 15800:
        alerts.append({
            'level': 'warning',
            'title': '💱 Kurs USD Naik',
            'message': f'USD/IDR {usd_rate:,} mendekati level waspada',
            'action': 'Monitor pergerakan kurs'
        })
    
    # Solvency alerts
    solvency_ratio = 124
    if solvency_ratio < 110:
        alerts.append({
            'level': 'danger',
            'title': '📊 Rasio Solvabilitas Rendah',
            'message': f'Rasio solvabilitas {solvency_ratio}% di bawah minimum 110%',
            'action': 'Review alokasi aset segera'
        })
    elif solvency_ratio < 120:
        alerts.append({
            'level': 'warning',
            'title': '📊 Rasio Solvabilitas Menurun',
            'message': f'Rasio solvabilitas {solvency_ratio}% mendekati batas minimum',
            'action': 'Pantau performa portofolio'
        })
    
    # Performance alerts
    ytd_return = 8.2
    target_return = 6.5
    
    if ytd_return < target_return * 0.8:
        alerts.append({
            'level': 'warning',
            'title': '📈 Imbal Hasil di Bawah Target',
            'message': f'YTD return {ytd_return}% jauh di bawah target {target_return}%',
            'action': 'Review strategi investasi'
        })
    
    # Market volatility alert
    market_volatility = np.random.uniform(15, 25)  # Simulated
    if market_volatility > 20:
        alerts.append({
            'level': 'info',
            'title': '📊 Volatilitas Pasar Tinggi',
            'message': f'Volatilitas pasar {market_volatility:.1f}% di atas normal',
            'action': 'Tingkatkan monitoring risiko'
        })
    
    # Display alerts
    if not alerts:
        st.success("✅ Semua indikator dalam kondisi normal")
        st.balloons()
    else:
        for alert in alerts:
            if alert['level'] == 'danger':
                st.error(f"🚨 **{alert['title']}**\n\n{alert['message']}\n\n**Tindakan:** {alert['action']}")
            elif alert['level'] == 'warning':
                st.warning(f"⚠️ **{alert['title']}**\n\n{alert['message']}\n\n**Tindakan:** {alert['action']}")
            else:
                st.info(f"ℹ️ **{alert['title']}**\n\n{alert['message']}\n\n**Tindakan:** {alert['action']}")

def main():
    """Main function untuk dashboard"""
    
    # Render sidebar navigation
    render_sidebar()
    
    # Header dengan timestamp
    st.title("🏠 Dashboard Monitoring Keberlanjutan")
    st.caption(f"⏰ Terakhir diperbarui: {datetime.now().strftime('%d %B %Y, %H:%M WIB')}")
    
    # Initialize API service
    api_service = APIService()
    
    # Main content dengan tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🏦 Portofolio", "⚠️ Risiko", "🗺️ Regional"])
    
    with tab1:
        # Get real-time data
        with st.spinner("📡 Mengambil data real-time..."):
            exchange_rates = api_service.get_exchange_rates()
            economic_indicators = api_service.get_economic_indicators()
        
        # Main KPI metrics
        render_kpi_cards()
        
        st.markdown("---")
        
        # Real-time indicators
        st.subheader("📊 Indikator Ekonomi Real-time")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            usd_rate = exchange_rates.get('USD', 15485)
            delta_usd = "↗️ 0.5%" if usd_rate > 15400 else "↘️ 0.3%"
            st.metric(
                "💵 USD/IDR", 
                f"Rp {usd_rate:,}",
                delta_usd
            )
        
        with col2:
            sar_rate = exchange_rates.get('SAR', 4129)
            delta_sar = "↗️ 0.3%" if sar_rate > 4100 else "↘️ 0.2%"
            st.metric(
                "🇸🇦 SAR/IDR", 
                f"Rp {sar_rate:,}",
                delta_sar
            )
        
        with col3:
            saudi_inflation = economic_indicators.get('saudi_inflation', 3.2)
            st.metric(
                "📈 Inflasi Saudi", 
                f"{saudi_inflation}%",
                "↘️ 0.2%"
            )
        
        with col4:
            bi_rate = economic_indicators.get('bi_rate', 6.0)
            st.metric(
                "🏦 BI Rate", 
                f"{bi_rate}%",
                "→ 0%"
            )
        
        st.markdown("---")
        
        # Trend chart
        render_trend_chart()
        
        st.markdown("---")
        
        # Alert system
        render_market_alerts()
    
    with tab2:
        render_portfolio_allocation()
    
    with tab3:
        render_risk_metrics()
    
    with tab4:
        render_regional_distribution()
    
    # Footer dengan quick actions
    st.markdown("---")
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🔄 Refresh Data", type="primary", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        if st.button("📊 Lihat Analytics", use_container_width=True):
            st.switch_page("pages/05_📈_Analytics.py")
    
    with col3:
        if st.button("📋 Generate Report", use_container_width=True):
            st.switch_page("pages/06_📋_Reports.py")
    
    with col4:
        if st.button("🧮 Risk Calculator", use_container_width=True):
            st.switch_page("pages/02_🧮_Liability_Calculator.py")
    
    with col5:
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.switch_page("pages/04_🤖_AI_Assistant.py")

if __name__ == "__main__":
    main()