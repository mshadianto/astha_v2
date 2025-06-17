# ===== tests/conftest.py =====
import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add app directory to Python path
app_dir = Path(__file__).parent.parent / "app"
sys.path.insert(0, str(app_dir))

@pytest.fixture
def temp_db():
    """Create temporary database for testing"""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    yield db_path
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def sample_liability_params():
    """Sample parameters for liability calculation"""
    return {
        'total_jemaah': 2500000,
        'inflasi_saudi': 3.5,
        'kurs_usd': 15500,
        'biaya_awal': 94482028,
        'tingkat_diskonto': 6.5,
        'tahun_proyeksi': 20
    }

@pytest.fixture
def sample_historical_data():
    """Sample historical hajj cost data"""
    import pandas as pd
    return pd.DataFrame({
        'Tahun': [2022, 2023, 2024, 2025],
        'BPIH': [85452883, 89629474, 94482028, 91493896],
        'Bipih': [39886009, 49812700, 56046172, 60559399],
        'NilaiManfaat': [45566874, 39816774, 38435856, 30934497]
    })
