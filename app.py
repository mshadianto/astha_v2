# app.py
"""
ASTHA - Hajj Treasury Analytics
Main entry point for Streamlit Cloud deployment
"""

import sys
import os

# Tambahkan path ke folder 'app' agar bisa import modul internal
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

# Jalankan fungsi utama dari app/main.py
try:
    from main import main  # Mengimpor fungsi main() dari app/main.py
    main()
except ImportError as e:
    import streamlit as st
    st.error(f"❌ Gagal mengimpor aplikasi utama: {e}")
    st.stop()
except Exception as e:
    import streamlit as st
    st.error(f"❌ Aplikasi gagal dijalankan: {e}")
    st.stop()
