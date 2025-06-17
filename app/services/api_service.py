# ===== services/api_service.py =====
import requests
import streamlit as st
from config.settings import AppConfig

class APIService:
    def __init__(self):
        self.config = AppConfig()
    
    @st.cache_data(ttl=3600)
    def get_exchange_rates(_self):
        """Get current exchange rates from free API"""
        try:
            # Using exchangerate-api.com (1500 requests/month free)
            if _self.config.EXCHANGE_RATE_API_KEY:
                url = f"https://v6.exchangerate-api.com/v6/{_self.config.EXCHANGE_RATE_API_KEY}/latest/USD"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    idr_rate = data['conversion_rates']['IDR']
                    sar_rate = data['conversion_rates']['SAR']
                    return {
                        'USD': idr_rate,
                        'SAR': idr_rate / sar_rate,
                        'source': 'ExchangeRate-API'
                    }
            
            # Fallback to fixer.io (100 requests/month free)
            url = "https://api.fixer.io/latest?base=USD&symbols=IDR,SAR"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'USD': data['rates']['IDR'],
                    'SAR': data['rates']['IDR'] / data['rates']['SAR'],
                    'source': 'Fixer.io'
                }
                
        except Exception as e:
            st.warning(f"⚠️ Error fetching exchange rates: {e}")
            
        # Fallback to default values
        return {
            'USD': 15500,
            'SAR': 4133,
            'source': 'Default Values'
        }
    
    @st.cache_data(ttl=86400)  # Cache for 24 hours
    def get_economic_indicators(_self):
        """Get economic indicators from free APIs"""
        indicators = {
            'saudi_inflation': 3.2,
            'indonesia_inflation': 2.8,
            'bi_rate': 6.0,
            'us_treasury_10y': 4.5,
            'source': 'Default Values'
        }
        
        try:
            # Try to get data from FRED API (free)
            if _self.config.FRED_API_KEY:
                fred_url = f"https://api.stlouisfed.org/fred/series/observations"
                params = {
                    'series_id': 'DFEDTARL',  # Federal funds rate
                    'api_key': _self.config.FRED_API_KEY,
                    'file_type': 'json',
                    'limit': 1,
                    'sort_order': 'desc'
                }
                response = requests.get(fred_url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data['observations']:
                        indicators['us_fed_rate'] = float(data['observations'][0]['value'])
                        indicators['source'] = 'FRED API'
                        
        except Exception as e:
            st.warning(f"⚠️ Error fetching economic data: {e}")
            
        return indicators
