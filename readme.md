# ===== README.md =====
"""
# 🕌 ASTHA - Agentic Sustainability for Hajj Treasury Analytics

Aplikasi analisis keuangan haji berbasis AI untuk Badan Pengelola Keuangan Haji (BPKH) Republik Indonesia.

## 🎯 Fitur Utama

- **📊 Dashboard Monitoring**: KPI real-time dan visualisasi data
- **🧮 Kalkulasi Liabilitas**: Perhitungan aktuaria berbasis AI
- **📈 Simulasi & Stress Test**: Analisis skenario risiko  
- **🤖 AI Assistant**: Chatbot cerdas untuk query data
- **📋 Laporan Otomatis**: Generasi laporan komprehensif

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone repository
git clone <repository-url>
cd astha-hajj-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Run setup script
python setup.py
```

### 2. Configure API Keys
Edit file `.env` dengan API keys Anda:
```env
ALPHA_VANTAGE_API_KEY=your_key_here
EXCHANGE_RATE_API_KEY=your_key_here
FRED_API_KEY=your_key_here
```

### 3. Run Application
```bash
# Method 1: Using launcher
python run_app.py

# Method 2: Direct streamlit
streamlit run app/main.py
```

### 4. Access Application
Buka browser di: http://localhost:8501

## 🔑 Free API Keys

### Alpha Vantage (Financial Data)
- Website: https://www.alphavantage.co/support/#api-key
- Free tier: 500 requests/day

### Exchange Rate API (Currency)  
- Website: https://exchangerate-api.com
- Free tier: 1500 requests/month

### FRED API (Economic Data)
- Website: https://fred.stlouisfed.org/docs/api/api_key.html
- Free tier: Unlimited requests

## 📊 Data Sources

Aplikasi menggunakan data historis biaya haji dan API eksternal untuk:
- Kurs mata uang real-time
- Indikator ekonomi terkini
- Data inflasi dan suku bunga

## 🏗️ Arsitektur

```
astha-hajj-analytics/
├── app/                # Main application
│   ├── main.py        # Entry point  
│   ├── pages/         # Multi-page components
│   ├── services/      # Business logic
│   └── utils/         # Utilities
├── config/            # Configuration
├── data/              # Data files
└── requirements.txt   # Dependencies
```

## 🧮 Formula Aktuaria

**Total Liabilitas = Σ (C_t × J_t) / (1+r)^t**

Dimana:
- C_t: Biaya per jemaah tahun t
- J_t: Jumlah jemaah tahun t  
- r: Tingkat diskonto

## 📈 Analisis yang Tersedia

- **Kalkulasi Liabilitas**: Present value kewajiban haji
- **Stress Testing**: 5 skenario risiko berbeda
- **Monte Carlo**: Simulasi 1000 iterasi
- **Sensitivity Analysis**: Analisis sensitivitas parameter
- **Forecasting**: Proyeksi biaya masa depan

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib
- **Calculations**: SciPy, scikit-learn
- **APIs**: Requests, HTTPx

## 📋 Requirements

- Python 3.8+
- 2GB RAM minimum
- Internet connection (untuk API calls)

## 🚀 Deployment

### Docker
```bash
docker build -t astha-app .
docker run -p 8501:8501 astha-app
```

### Cloud Deployment
- **Streamlit Cloud**: Deploy langsung dari GitHub
- **Heroku**: Gunakan Procfile yang disediakan
- **AWS/GCP**: Deploy sebagai containerized app

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch  
5. Create Pull Request

## 📝 License

© 2025 MS Hadianto

## 📞 Support

Untuk bantuan teknis atau pertanyaan:
- Email: sopian.hadianto@gmail.com
- Documentation: [Link to docs]
- Issues: [GitHub Issues]

---

**Made with ❤️ for sustainable hajj financial management**
"""
Claude