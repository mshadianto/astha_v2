"""
Metrics Component for ASTHA-HAJJ-ANALYTICS
Komponen metrik dan KPI untuk dashboard analitik haji
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def render_kpi_cards():
    """Render KPI cards untuk dashboard utama"""
    
    # Sample data - ganti dengan data real dari database
    total_pilgrims = 125000
    total_revenue = 5250000000000  # 5.25 Trillion IDR
    satisfaction_rate = 92.5
    health_incidents = 234
    
    # Create 4 columns for KPI cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Jamaah",
            value=f"{total_pilgrims:,}",
            delta="1,250 dari bulan lalu",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Total Pendapatan",
            value=f"Rp {total_revenue/1000000000:.1f}M",
            delta="5.2% dari bulan lalu",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="Tingkat Kepuasan",
            value=f"{satisfaction_rate}%",
            delta="2.3% dari bulan lalu",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Insiden Kesehatan",
            value=health_incidents,
            delta="-12 dari bulan lalu",
            delta_color="inverse"
        )

def render_trend_chart():
    """Render grafik tren untuk dashboard"""
    
    # Generate sample trend data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    pilgrim_trend = np.random.randint(8000, 12000, len(dates))
    revenue_trend = pilgrim_trend * np.random.randint(35000000, 45000000, len(dates))
    
    df_trend = pd.DataFrame({
        'month': dates,
        'pilgrims': pilgrim_trend,
        'revenue': revenue_trend
    })
    
    # Create subplot with secondary y-axis
    fig = make_subplots(
        specs=[[{"secondary_y": True}]],
        subplot_titles=("Tren Jamaah dan Pendapatan 2024",)
    )
    
    # Add pilgrim trend
    fig.add_trace(
        go.Scatter(
            x=df_trend['month'],
            y=df_trend['pilgrims'],
            name="Jumlah Jamaah",
            line=dict(color='#2E8B57', width=3),
            mode='lines+markers'
        ),
        secondary_y=False,
    )
    
    # Add revenue trend
    fig.add_trace(
        go.Scatter(
            x=df_trend['month'],
            y=df_trend['revenue'],
            name="Pendapatan (Rp)",
            line=dict(color='#FFD700', width=3),
            mode='lines+markers'
        ),
        secondary_y=True,
    )
    
    # Update layout with correct method
    fig.update_layout(
        title="Tren Jamaah dan Pendapatan 2024",
        xaxis_title="Bulan",
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Set y-axes titles with correct method
    fig.update_yaxes(
        title_text="Jumlah Jamaah", 
        tickformat='.0f',
        secondary_y=False
    )
    fig.update_yaxes(
        title_text="Pendapatan (Rp)", 
        tickformat='.2s',
        secondary_y=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_pilgrim_status_chart():
    """Render grafik status jamaah"""
    
    # Sample data
    status_data = {
        'Status': ['Terdaftar', 'Dalam Proses', 'Siap Berangkat', 'Di Arab Saudi', 'Kembali'],
        'Jumlah': [45000, 32000, 25000, 18000, 5000],
        'Persentase': [36, 25.6, 20, 14.4, 4]
    }
    
    df_status = pd.DataFrame(status_data)
    
    # Create horizontal bar chart
    fig = px.bar(
        df_status,
        x='Jumlah',
        y='Status',
        orientation='h',
        title='Status Jamaah Haji 2024',
        color='Persentase',
        color_continuous_scale='Viridis',
        text='Jumlah'
    )
    
    # Update layout
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False,
        height=400
    )
    
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    
    st.plotly_chart(fig, use_container_width=True)

def render_regional_distribution():
    """Render distribusi regional jamaah"""
    
    # Sample regional data
    regional_data = {
        'Provinsi': ['Jawa Barat', 'Jawa Timur', 'Jawa Tengah', 'Sumatra Utara', 
                    'DKI Jakarta', 'Sumatra Selatan', 'Lampung', 'Banten', 
                    'Sumatra Barat', 'Kalimantan Selatan'],
        'Jamaah': [18500, 16200, 14800, 9500, 8900, 7200, 6800, 6500, 6100, 5500],
        'Kuota': [20000, 17000, 15500, 10000, 9500, 7500, 7000, 7000, 6500, 6000]
    }
    
    df_regional = pd.DataFrame(regional_data)
    
    # Create grouped bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Jamaah Terdaftar',
        x=df_regional['Provinsi'],
        y=df_regional['Jamaah'],
        marker_color='#2E8B57'
    ))
    
    fig.add_trace(go.Bar(
        name='Kuota',
        x=df_regional['Provinsi'],
        y=df_regional['Kuota'],
        marker_color='#FFD700',
        opacity=0.7
    ))
    
    fig.update_layout(
        title='Distribusi Jamaah per Provinsi (Top 10)',
        xaxis_title='Provinsi',
        yaxis_title='Jumlah Jamaah',
        barmode='group',
        xaxis_tickangle=-45,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_health_metrics():
    """Render metrik kesehatan jamaah"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Health status pie chart
        health_data = {
            'Status': ['Sehat', 'Perlu Monitoring', 'Berisiko Tinggi'],
            'Jumlah': [98500, 16200, 10300]
        }
        
        df_health = pd.DataFrame(health_data)
        
        fig_pie = px.pie(
            df_health,
            values='Jumlah',
            names='Status',
            title='Status Kesehatan Jamaah',
            color_discrete_sequence=['#32CD32', '#FFD700', '#FF6347']
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Medical incidents by age group
        age_incidents = {
            'Kelompok Usia': ['25-35', '36-45', '46-55', '56-65', '65+'],
            'Insiden': [15, 28, 45, 89, 127]
        }
        
        df_incidents = pd.DataFrame(age_incidents)
        
        fig_bar = px.bar(
            df_incidents,
            x='Kelompok Usia',
            y='Insiden',
            title='Insiden Medis per Kelompok Usia',
            color='Insiden',
            color_continuous_scale='Reds'
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)

def render_financial_metrics():
    """Render metrik keuangan"""
    
    # Payment status
    col1, col2 = st.columns(2)
    
    with col1:
        payment_data = {
            'Status Pembayaran': ['Lunas', 'Cicilan', 'Tunggakan'],
            'Jumlah': [87500, 31250, 6250],
            'Nilai': [3500000000000, 1250000000000, 250000000000]
        }
        
        df_payment = pd.DataFrame(payment_data)
        
        fig_payment = px.pie(
            df_payment,
            values='Jumlah',
            names='Status Pembayaran',
            title='Status Pembayaran Jamaah',
            color_discrete_sequence=['#32CD32', '#FFD700', '#FF6347']
        )
        
        st.plotly_chart(fig_payment, use_container_width=True)
    
    with col2:
        # Monthly revenue trend
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        revenue = [420, 380, 450, 520, 480, 380, 420, 520, 580, 480, 350, 280]
        
        fig_revenue = px.line(
            x=months,
            y=revenue,
            title='Tren Pendapatan Bulanan (Miliar Rp)',
            markers=True
        )
        
        fig_revenue.update_traces(line_color='#2E8B57', line_width=3)
        fig_revenue.update_layout(
            xaxis_title='Bulan',
            yaxis_title='Pendapatan (Miliar Rp)'
        )
        
        st.plotly_chart(fig_revenue, use_container_width=True)

def render_service_quality_metrics():
    """Render metrik kualitas layanan"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Satisfaction gauge
        satisfaction_score = 92.5
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = satisfaction_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Kepuasan Jamaah (%)"},
            delta = {'reference': 90},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#2E8B57"},
                'steps': [
                    {'range': [0, 70], 'color': "lightgray"},
                    {'range': [70, 90], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        # Response time metrics
        response_data = {
            'Kategori': ['Email', 'Telepon', 'WhatsApp', 'Langsung'],
            'Waktu (Jam)': [24, 2, 1, 0.5]
        }
        
        df_response = pd.DataFrame(response_data)
        
        fig_response = px.bar(
            df_response,
            x='Kategori',
            y='Waktu (Jam)',
            title='Waktu Respon Layanan',
            color='Waktu (Jam)',
            color_continuous_scale='RdYlGn_r'
        )
        
        fig_response.update_layout(height=300)
        st.plotly_chart(fig_response, use_container_width=True)
    
    with col3:
        # Complaint categories
        complaint_data = {
            'Kategori': ['Akomodasi', 'Transportasi', 'Makanan', 'Layanan', 'Lainnya'],
            'Jumlah': [45, 32, 28, 18, 12]
        }
        
        df_complaints = pd.DataFrame(complaint_data)
        
        fig_complaints = px.pie(
            df_complaints,
            values='Jumlah',
            names='Kategori',
            title='Kategori Keluhan',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig_complaints.update_layout(height=300)
        st.plotly_chart(fig_complaints, use_container_width=True)

def calculate_pilgrim_metrics(data=None):
    """Hitung metrik jamaah dari data"""
    if data is None:
        # Return sample metrics if no data provided
        return {
            'total_pilgrims': 125000,
            'registered': 87500,
            'in_process': 25000,
            'ready_to_depart': 12500,
            'growth_rate': 8.5
        }
    
    # Calculate actual metrics from data
    metrics = {
        'total_pilgrims': len(data),
        'registered': len(data[data['status'] == 'registered']),
        'in_process': len(data[data['status'] == 'in_process']),
        'ready_to_depart': len(data[data['status'] == 'ready']),
    }
    
    return metrics

def calculate_financial_metrics(data=None):
    """Hitung metrik keuangan dari data"""
    if data is None:
        # Return sample metrics if no data provided
        return {
            'total_revenue': 5250000000000,
            'outstanding': 250000000000,
            'collection_rate': 95.2,
            'avg_payment': 42000000
        }
    
    # Calculate actual metrics from data
    metrics = {
        'total_revenue': data['payment_amount'].sum(),
        'outstanding': data[data['status'] == 'outstanding']['payment_amount'].sum(),
        'collection_rate': (data['payment_amount'].sum() / data['total_due'].sum()) * 100,
        'avg_payment': data['payment_amount'].mean()
    }
    
    return metrics

def export_metrics_to_excel(metrics_data, filename="hajj_metrics.xlsx"):
    """Export metrik ke file Excel"""
    try:
        import openpyxl
        from io import BytesIO
        
        # Create DataFrame from metrics
        df = pd.DataFrame(metrics_data)
        
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Metrics', index=False)
        
        output.seek(0)
        
        return output.getvalue()
    
    except ImportError:
        st.error("Openpyxl library tidak tersedia untuk export Excel")
        return None

# Additional utility functions
def format_currency(amount):
    """Format angka menjadi format mata uang Rupiah"""
    if amount >= 1_000_000_000_000:  # Triliun
        return f"Rp {amount/1_000_000_000_000:.1f}T"
    elif amount >= 1_000_000_000:  # Miliar
        return f"Rp {amount/1_000_000_000:.1f}M"
    elif amount >= 1_000_000:  # Juta
        return f"Rp {amount/1_000_000:.1f}Jt"
    else:
        return f"Rp {amount:,.0f}"

def format_number(number):
    """Format angka dengan separator ribuan"""
    return f"{number:,}"

def get_color_palette():
    """Return color palette untuk konsistensi visualisasi"""
    return {
        'primary': '#2E8B57',    # Sea Green
        'secondary': '#FFD700',  # Gold
        'accent': '#4682B4',     # Steel Blue
        'warning': '#FF6347',    # Tomato
        'success': '#32CD32',    # Lime Green
        'info': '#20B2AA'        # Light Sea Green
    }