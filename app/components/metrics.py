# ===== app/components/metrics.py =====
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render_kpi_cards():
    """Render main KPI metric cards"""
    
    # Load sample data
    kpi_data = {
        'total_assets': 180.5e12,
        'total_liability': 145.2e12, 
        'solvency_ratio': 1.24,
        'ytd_return': 8.2
    }
    
    st.subheader("📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_assets = "8.2% YTD"
        st.metric(
            label="💰 Total Aset Kelolaan",
            value=f"Rp {kpi_data['total_assets']/1e12:.1f}T",
            delta=delta_assets,
            delta_color="normal"
        )
    
    with col2:
        delta_liability = "3.1% dari proyeksi"
        st.metric(
            label="📊 Total Liabilitas", 
            value=f"Rp {kpi_data['total_liability']/1e12:.1f}T",
            delta=delta_liability,
            delta_color="normal"
        )
    
    with col3:
        delta_solvency = "0.05 dari target"
        color = "normal" if kpi_data['solvency_ratio'] >= 1.2 else "inverse"
        st.metric(
            label="🛡️ Rasio Solvabilitas",
            value=f"{kpi_data['solvency_ratio']:.2f}",
            delta=delta_solvency,
            delta_color=color
        )
    
    with col4:
        delta_return = "1.7% di atas target"
        st.metric(
            label="📈 Imbal Hasil (YTD)",
            value=f"{kpi_data['ytd_return']:.1f}%",
            delta=delta_return,
            delta_color="normal"
        )

def render_trend_chart():
    """Render historical trend chart"""
    st.subheader("📈 Tren Biaya Haji Historis")
    
    # Historical data
    historical_data = pd.DataFrame({
        'Tahun': [2022, 2023, 2024, 2025],
        'BPIH': [85452883, 89629474, 94482028, 91493896],
        'Bipih': [39886009, 49812700, 56046172, 60559399],
        'NilaiManfaat': [45566874, 39816774, 38435856, 30934497]
    })
    
    # Create figure
    fig = go.Figure()
    
    # Add BPIH line
    fig.add_trace(go.Scatter(
        x=historical_data['Tahun'],
        y=historical_data['BPIH'],
        mode='lines+markers',
        name='BPIH',
        line=dict(color='#10b981', width=3),
        marker=dict(size=8)
    ))
    
    # Add Nilai Manfaat line
    fig.add_trace(go.Scatter(
        x=historical_data['Tahun'],
        y=historical_data['NilaiManfaat'],
        mode='lines+markers',
        name='Nilai Manfaat',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Evolusi Biaya dan Nilai Manfaat",
        xaxis_title="Tahun",
        yaxis_title="Rupiah",
        height=400,
        showlegend=True,
        hovermode='x unified'
    )
    
    # Format y-axis to show in millions
    fig.update_yaxis(tickformat='.0s')
    
    st.plotly_chart(fig, use_container_width=True)
