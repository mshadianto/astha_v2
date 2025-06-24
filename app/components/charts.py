"""
Charts Component for ASTHA-HAJJ-ANALYTICS
Komponen visualisasi data untuk analitik haji dan umrah
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt

class HajjCharts:
    """Kelas untuk membuat berbagai visualisasi data haji dan umrah"""
    
    def __init__(self):
        self.color_palette = {
            'primary': '#2E8B57',    # Sea Green
            'secondary': '#FFD700',  # Gold
            'accent': '#4682B4',     # Steel Blue
            'warning': '#FF6347',    # Tomato
            'success': '#32CD32',    # Lime Green
            'info': '#20B2AA'        # Light Sea Green
        }
    
    def pilgrim_demographics_chart(self, data):
        """Grafik demografi jamaah haji"""
        if data.empty:
            st.warning("Data demografi tidak tersedia")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribusi usia
            fig_age = px.histogram(
                data, 
                x='age_group', 
                title='Distribusi Usia Jamaah',
                color_discrete_sequence=[self.color_palette['primary']]
            )
            fig_age.update_layout(
                xaxis_title="Kelompok Usia",
                yaxis_title="Jumlah Jamaah",
                showlegend=False
            )
            st.plotly_chart(fig_age, use_container_width=True)
        
        with col2:
            # Distribusi gender
            gender_counts = data['gender'].value_counts()
            fig_gender = px.pie(
                values=gender_counts.values,
                names=gender_counts.index,
                title='Distribusi Gender Jamaah',
                color_discrete_sequence=[self.color_palette['primary'], self.color_palette['secondary']]
            )
            st.plotly_chart(fig_gender, use_container_width=True)
    
    def regional_distribution_chart(self, data):
        """Grafik distribusi regional jamaah"""
        if data.empty:
            st.warning("Data regional tidak tersedia")
            return
        
        # Peta distribusi jamaah per provinsi
        fig_map = px.choropleth(
            data,
            locations='province_code',
            color='pilgrim_count',
            hover_name='province_name',
            hover_data=['pilgrim_count'],
            title='Distribusi Jamaah Haji per Provinsi',
            color_continuous_scale='Viridis',
            locationmode='geojson-id'
        )
        
        fig_map.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            )
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Bar chart top 10 provinsi
        top_provinces = data.nlargest(10, 'pilgrim_count')
        fig_bar = px.bar(
            top_provinces,
            x='pilgrim_count',
            y='province_name',
            orientation='h',
            title='Top 10 Provinsi dengan Jamaah Terbanyak',
            color='pilgrim_count',
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
    
    def health_metrics_dashboard(self, data):
        """Dashboard metrik kesehatan jamaah"""
        if data.empty:
            st.warning("Data kesehatan tidak tersedia")
            return
        
        # Metrics cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_pilgrims = len(data)
            st.metric("Total Jamaah", f"{total_pilgrims:,}")
        
        with col2:
            healthy_count = len(data[data['health_status'] == 'Sehat'])
            healthy_pct = (healthy_count / total_pilgrims) * 100
            st.metric("Jamaah Sehat", f"{healthy_pct:.1f}%")
        
        with col3:
            medical_cases = len(data[data['medical_attention'] == True])
            st.metric("Kasus Medis", medical_cases)
        
        with col4:
            avg_age = data['age'].mean()
            st.metric("Rata-rata Usia", f"{avg_age:.1f} tahun")
        
        # Health status distribution
        health_dist = data['health_status'].value_counts()
        fig_health = px.donut(
            values=health_dist.values,
            names=health_dist.index,
            title='Status Kesehatan Jamaah',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_health, use_container_width=True)
        
        # Medical incidents timeline
        if 'incident_date' in data.columns:
            daily_incidents = data.groupby('incident_date').size().reset_index(name='count')
            fig_timeline = px.line(
                daily_incidents,
                x='incident_date',
                y='count',
                title='Tren Insiden Medis Harian',
                markers=True
            )
            fig_timeline.update_traces(line_color=self.color_palette['warning'])
            st.plotly_chart(fig_timeline, use_container_width=True)
    
    def accommodation_analysis(self, data):
        """Analisis akomodasi jamaah"""
        if data.empty:
            st.warning("Data akomodasi tidak tersedia")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Occupancy rate by hotel
            fig_occupancy = px.bar(
                data,
                x='hotel_name',
                y='occupancy_rate',
                title='Tingkat Hunian Hotel',
                color='occupancy_rate',
                color_continuous_scale='RdYlGn'
            )
            fig_occupancy.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_occupancy, use_container_width=True)
        
        with col2:
            # Room type distribution
            room_dist = data['room_type'].value_counts()
            fig_rooms = px.pie(
                values=room_dist.values,
                names=room_dist.index,
                title='Distribusi Tipe Kamar',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_rooms, use_container_width=True)
        
        # Hotel satisfaction scores
        if 'satisfaction_score' in data.columns:
            fig_satisfaction = px.box(
                data,
                x='hotel_category',
                y='satisfaction_score',
                title='Skor Kepuasan per Kategori Hotel',
                color='hotel_category'
            )
            st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    def transportation_metrics(self, data):
        """Metrik transportasi jamaah"""
        if data.empty:
            st.warning("Data transportasi tidak tersedia")
            return
        
        # Transportation mode distribution
        transport_dist = data['transport_mode'].value_counts()
        fig_transport = px.bar(
            x=transport_dist.index,
            y=transport_dist.values,
            title='Distribusi Moda Transportasi',
            color=transport_dist.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_transport, use_container_width=True)
        
        # On-time performance
        col1, col2 = st.columns(2)
        
        with col1:
            ontime_pct = (data['on_time'] == True).mean() * 100
            fig_ontime = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = ontime_pct,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Ketepatan Waktu (%)"},
                delta = {'reference': 90},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': self.color_palette['success']},
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
            st.plotly_chart(fig_ontime, use_container_width=True)
        
        with col2:
            # Delay analysis
            if 'delay_minutes' in data.columns:
                avg_delay = data['delay_minutes'].mean()
                fig_delay = px.histogram(
                    data,
                    x='delay_minutes',
                    title='Distribusi Keterlambatan (Menit)',
                    nbins=20,
                    color_discrete_sequence=[self.color_palette['warning']]
                )
                st.plotly_chart(fig_delay, use_container_width=True)
    
    def financial_overview(self, data):
        """Overview keuangan haji"""
        if data.empty:
            st.warning("Data keuangan tidak tersedia")
            return
        
        # Revenue metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_revenue = data['total_payment'].sum()
            st.metric("Total Pendapatan", f"Rp {total_revenue:,.0f}")
        
        with col2:
            avg_payment = data['total_payment'].mean()
            st.metric("Rata-rata Pembayaran", f"Rp {avg_payment:,.0f}")
        
        with col3:
            outstanding = data[data['payment_status'] == 'Outstanding']['total_payment'].sum()
            st.metric("Tunggakan", f"Rp {outstanding:,.0f}")
        
        # Payment status distribution
        payment_status = data['payment_status'].value_counts()
        fig_payment = px.pie(
            values=payment_status.values,
            names=payment_status.index,
            title='Status Pembayaran Jamaah',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_payment, use_container_width=True)
        
        # Monthly payment trend
        if 'payment_date' in data.columns:
            monthly_payments = data.groupby(data['payment_date'].dt.to_period('M'))['total_payment'].sum().reset_index()
            monthly_payments['payment_date'] = monthly_payments['payment_date'].astype(str)
            
            fig_trend = px.line(
                monthly_payments,
                x='payment_date',
                y='total_payment',
                title='Tren Pembayaran Bulanan',
                markers=True
            )
            fig_trend.update_traces(line_color=self.color_palette['success'])
            st.plotly_chart(fig_trend, use_container_width=True)
    
    def liability_projection_chart(self, data, projection_years=5):
        """Grafik proyeksi kewajiban keuangan"""
        if data.empty:
            st.warning("Data proyeksi tidak tersedia")
            return
        
        # Calculate current liability
        current_liability = data['outstanding_amount'].sum()
        
        # Project future liabilities based on growth rate
        years = list(range(2024, 2024 + projection_years + 1))
        growth_rate = 0.08  # 8% annual growth assumption
        
        projections = []
        for i, year in enumerate(years):
            projected_amount = current_liability * (1 + growth_rate) ** i
            projections.append({
                'year': year,
                'projected_liability': projected_amount,
                'category': 'Proyeksi Kewajiban'
            })
        
        df_projection = pd.DataFrame(projections)
        
        # Create projection chart
        fig = px.line(
            df_projection,
            x='year',
            y='projected_liability',
            title='Proyeksi Kewajiban Keuangan 5 Tahun',
            markers=True,
            color_discrete_sequence=[self.color_palette['warning']]
        )
        
        fig.update_layout(
            xaxis_title="Tahun",
            yaxis_title="Kewajiban (Rp)",
            yaxis_tickformat='.2s'
        )
        
        # Add current year marker
        fig.add_vline(
            x=2024, 
            line_dash="dash", 
            line_color="red",
            annotation_text="Tahun Ini"
        )
        
        return fig
    
    def service_quality_metrics(self, data):
        """Metrik kualitas layanan"""
        if data.empty:
            st.warning("Data kualitas layanan tidak tersedia")
            return
        
        # Service rating overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_rating = data['service_rating'].mean()
            st.metric("Rating Rata-rata", f"{avg_rating:.2f}/5.0")
        
        with col2:
            satisfaction_rate = (data['satisfaction_level'] == 'Puas').mean() * 100
            st.metric("Tingkat Kepuasan", f"{satisfaction_rate:.1f}%")
        
        with col3:
            complaint_count = len(data[data['has_complaint'] == True])
            st.metric("Jumlah Keluhan", complaint_count)
        
        with col4:
            response_time = data['response_time_hours'].mean()
            st.metric("Waktu Respon Avg", f"{response_time:.1f} jam")
        
        # Service rating distribution
        rating_dist = data['service_rating'].value_counts().sort_index()
        fig_rating = px.bar(
            x=rating_dist.index,
            y=rating_dist.values,
            title='Distribusi Rating Layanan',
            color=rating_dist.values,
            color_continuous_scale='RdYlGn'
        )
        fig_rating.update_layout(
            xaxis_title="Rating (1-5)",
            yaxis_title="Jumlah Response"
        )
        st.plotly_chart(fig_rating, use_container_width=True)
        
        # Complaint categories
        if 'complaint_category' in data.columns:
            complaint_cats = data[data['has_complaint'] == True]['complaint_category'].value_counts()
            fig_complaints = px.pie(
                values=complaint_cats.values,
                names=complaint_cats.index,
                title='Kategori Keluhan',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_complaints, use_container_width=True)


# Standalone functions for backward compatibility
def create_liability_projection_chart(data, projection_years=5):
    """Fungsi standalone untuk membuat grafik proyeksi kewajiban"""
    charts = HajjCharts()
    return charts.liability_projection_chart(data, projection_years)

def create_pilgrim_demographics_chart(data):
    """Fungsi standalone untuk grafik demografi jamaah"""
    charts = HajjCharts()
    return charts.pilgrim_demographics_chart(data)

def create_regional_distribution_chart(data):
    """Fungsi standalone untuk grafik distribusi regional"""
    charts = HajjCharts()
    return charts.regional_distribution_chart(data)

def create_health_dashboard(data):
    """Fungsi standalone untuk dashboard kesehatan"""
    charts = HajjCharts()
    return charts.health_metrics_dashboard(data)

def create_accommodation_analysis(data):
    """Fungsi standalone untuk analisis akomodasi"""
    charts = HajjCharts()
    return charts.accommodation_analysis(data)

def create_transportation_metrics(data):
    """Fungsi standalone untuk metrik transportasi"""
    charts = HajjCharts()
    return charts.transportation_metrics(data)

def create_financial_overview(data):
    """Fungsi standalone untuk overview keuangan"""
    charts = HajjCharts()
    return charts.financial_overview(data)

def create_service_quality_metrics(data):
    """Fungsi standalone untuk metrik kualitas layanan"""
    charts = HajjCharts()
    return charts.service_quality_metrics(data)

# Additional utility functions
def generate_sample_data(data_type="pilgrims", num_records=1000):
    """Generate sample data for testing purposes"""
    np.random.seed(42)
    
    if data_type == "pilgrims":
        return pd.DataFrame({
            'id': range(1, num_records + 1),
            'name': [f'Jamaah_{i}' for i in range(1, num_records + 1)],
            'age': np.random.randint(25, 80, num_records),
            'age_group': np.random.choice(['25-35', '36-45', '46-55', '56-65', '65+'], num_records),
            'gender': np.random.choice(['Laki-laki', 'Perempuan'], num_records),
            'province_name': np.random.choice(['Jawa Barat', 'Jawa Timur', 'Jawa Tengah', 'Sumatra Utara', 'DKI Jakarta'], num_records),
            'health_status': np.random.choice(['Sehat', 'Perlu Perhatian', 'Berisiko Tinggi'], num_records, p=[0.8, 0.15, 0.05]),
            'medical_attention': np.random.choice([True, False], num_records, p=[0.1, 0.9]),
            'total_payment': np.random.randint(35000000, 45000000, num_records),
            'payment_status': np.random.choice(['Lunas', 'Cicilan', 'Outstanding'], num_records, p=[0.7, 0.25, 0.05]),
            'service_rating': np.random.randint(1, 6, num_records),
            'satisfaction_level': np.random.choice(['Sangat Puas', 'Puas', 'Cukup', 'Kurang Puas'], num_records, p=[0.3, 0.5, 0.15, 0.05]),
            'has_complaint': np.random.choice([True, False], num_records, p=[0.1, 0.9])
        })
    
    elif data_type == "liability":
        return pd.DataFrame({
            'year': [2024, 2025, 2026, 2027, 2028, 2029],
            'outstanding_amount': [1000000000, 1080000000, 1166400000, 1259712000, 1320488960, 1426128157]
        })
    
    return pd.DataFrame()

def apply_custom_styling():
    """Apply custom CSS styling for charts"""
    st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
    }
    
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .dashboard-header {
        color: #2E8B57;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)