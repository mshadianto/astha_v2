"""
Sidebar Navigation Component untuk ASTHA-HAJJ-ANALYTICS
Mengatasi masalah navigation yang tidak berfungsi
"""

import streamlit as st
from pathlib import Path

def show_sidebar_navigation():
    """Tampilkan custom sidebar navigation"""
    
    # Logo dan title
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #2E8B57; margin: 0;">🕌</h1>
        <h3 style="color: #2E8B57; margin: 0;">ASTHA HAJJ</h3>
        <p style="color: #666; margin: 0; font-size: 0.9em;">ANALYTICS</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Current page detection
    current_page = st.session_state.get('current_page', 'main')
    
    # Navigation menu
    st.sidebar.subheader("📍 Navigation")
    
    # Main Dashboard
    if st.sidebar.button(
        "🏠 Dashboard", 
        use_container_width=True,
        type="primary" if current_page == "dashboard" else "secondary"
    ):
        st.session_state.current_page = "dashboard"
        st.switch_page("pages/01_🏠_Dashboard.py")
    
    # Liability Calculator
    if st.sidebar.button(
        "🧮 Kalkulasi Liabilitas", 
        use_container_width=True,
        type="primary" if current_page == "liability" else "secondary"
    ):
        st.session_state.current_page = "liability"
        st.switch_page("pages/02_🧮_Liability_Calculator.py")
    
    # Simulation & Stress Test
    if st.sidebar.button(
        "📊 Simulasi & Stress Test", 
        use_container_width=True,
        type="primary" if current_page == "simulation" else "secondary"
    ):
        st.session_state.current_page = "simulation"
        st.switch_page("pages/03_📊_Simulation.py")
    
    # AI Assistant
    if st.sidebar.button(
        "🤖 AI Assistant", 
        use_container_width=True,
        type="primary" if current_page == "ai" else "secondary"
    ):
        st.session_state.current_page = "ai"
        st.switch_page("pages/04_🤖_AI_Assistant.py")
    
    # Analytics
    if st.sidebar.button(
        "📈 Analytics", 
        use_container_width=True,
        type="primary" if current_page == "analytics" else "secondary"
    ):
        st.session_state.current_page = "analytics"
        st.switch_page("pages/05_📈_Analytics.py")
    
    # Reports
    if st.sidebar.button(
        "📋 Reports", 
        use_container_width=True,
        type="primary" if current_page == "reports" else "secondary"
    ):
        st.session_state.current_page = "reports"
        st.switch_page("pages/06_📋_Reports.py")
    
    st.sidebar.markdown("---")
    
    # System info
    st.sidebar.subheader("ℹ️ System Info")
    st.sidebar.info(f"""
    **Status**: Online ✅  
    **Version**: v1.0.0  
    **Last Update**: June 2024
    """)

def show_sidebar_with_option_menu():
    """Alternative navigation menggunakan streamlit-option-menu"""
    
    try:
        from streamlit_option_menu import option_menu
        
        with st.sidebar:
            # Logo
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h1 style="color: #2E8B57;">🕌 ASTHA HAJJ</h1>
                <p style="color: #666;">ANALYTICS</p>
            </div>
            """, unsafe_allow_html=True)
            
            selected = option_menu(
                menu_title="Main Menu",
                options=[
                    "Dashboard", 
                    "Liability Calculator", 
                    "Simulation", 
                    "AI Assistant", 
                    "Analytics", 
                    "Reports"
                ],
                icons=[
                    "house", 
                    "calculator", 
                    "graph-up", 
                    "robot", 
                    "bar-chart", 
                    "file-text"
                ],
                menu_icon="cast",
                default_index=0,
                orientation="vertical",
                styles={
                    "container": {"padding": "0!important", "background-color": "transparent"},
                    "icon": {"color": "#2E8B57", "font-size": "16px"},
                    "nav-link": {
                        "font-size": "14px",
                        "text-align": "left",
                        "margin": "0px",
                        "padding": "10px",
                        "--hover-color": "#f0f2f6",
                    },
                    "nav-link-selected": {"background-color": "#2E8B57"},
                },
            )
            
            # Navigation logic
            page_mapping = {
                "Dashboard": "pages/01_🏠_Dashboard.py",
                "Liability Calculator": "pages/02_🧮_Liability_Calculator.py",
                "Simulation": "pages/03_📊_Simulation.py",
                "AI Assistant": "pages/04_🤖_AI_Assistant.py",
                "Analytics": "pages/05_📈_Analytics.py",
                "Reports": "pages/06_📋_Reports.py"
            }
            
            if selected in page_mapping:
                target_page = page_mapping[selected]
                if st.session_state.get('current_page') != selected:
                    st.session_state.current_page = selected
                    st.switch_page(target_page)
    
    except ImportError:
        # Fallback ke navigation biasa jika streamlit-option-menu tidak tersedia
        show_sidebar_navigation()

def check_page_exists(page_path):
    """Check apakah file halaman ada"""
    return Path(page_path).exists()

def safe_switch_page(page_path, page_name=""):
    """Safe page switching dengan error handling"""
    try:
        if check_page_exists(page_path):
            st.switch_page(page_path)
        else:
            st.sidebar.error(f"Halaman {page_name} tidak ditemukan: {page_path}")
    except Exception as e:
        st.sidebar.error(f"Error navigating to {page_name}: {str(e)}")

def show_navigation_debug():
    """Debug information untuk troubleshooting navigation"""
    
    if st.sidebar.checkbox("🔧 Debug Mode"):
        st.sidebar.subheader("Debug Info")
        
        # Current working directory
        current_dir = Path.cwd()
        st.sidebar.text(f"Current Dir: {current_dir}")
        
        # List pages directory
        pages_dir = current_dir / "pages"
        if pages_dir.exists():
            st.sidebar.text("Available pages:")
            for page_file in pages_dir.glob("*.py"):
                st.sidebar.text(f"- {page_file.name}")
        else:
            st.sidebar.error("Pages directory not found!")
        
        # Session state
        st.sidebar.text("Session State:")
        for key, value in st.session_state.items():
            if not key.startswith('_'):
                st.sidebar.text(f"- {key}: {value}")

# Main navigation function yang akan dipanggil
def render_sidebar():
    """Main function untuk render sidebar - pilih method yang diinginkan"""
    
    # Pilihan 1: Navigation biasa
    show_sidebar_navigation()
    
    # Pilihan 2: Dengan option menu (uncomment jika ingin pakai)
    # show_sidebar_with_option_menu()
    
    # Debug mode (uncomment jika perlu troubleshoot)
    # show_navigation_debug()