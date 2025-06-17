# ===== config/settings.py =====
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AppConfig:
    """Application configuration"""
    APP_NAME: str = os.getenv("APP_NAME", "ASTHA - Hajj Treasury Analytics")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # API Keys
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "")
    EXCHANGE_RATE_API_KEY: str = os.getenv("EXCHANGE_RATE_API_KEY", "")
    FRED_API_KEY: str = os.getenv("FRED_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Cache settings
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    
    # Default calculation parameters
    DEFAULT_TOTAL_JEMAAH: int = 2500000
    DEFAULT_INFLASI_SAUDI: float = 3.5
    DEFAULT_KURS_USD: int = 15500
    DEFAULT_TINGKAT_DISKONTO: float = 6.5
    DEFAULT_TAHUN_PROYEKSI: int = 20
