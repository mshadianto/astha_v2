# ===== models/database.py =====
import sqlite3
import pandas as pd
from contextlib import contextmanager
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

class DatabaseManager:
    """Database manager for ASTHA application"""
    
    def __init__(self, db_path: str = "data/astha.db"):
        self.db_path = db_path
        self.logger = logging.getLogger("database")
        self._init_database()
    
    def _init_database(self):
        """Initialize database with required tables"""
        with self.get_connection() as conn:
            # Create jemaah_data table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS jemaah_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    provinsi TEXT NOT NULL,
                    total_jemaah INTEGER NOT NULL,
                    jemaah_tunggu INTEGER NOT NULL,
                    estimasi_keberangkatan INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create biaya_haji table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS biaya_haji (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tahun INTEGER NOT NULL,
                    bpih REAL NOT NULL,
                    bipih REAL NOT NULL,
                    nilai_manfaat REAL NOT NULL,
                    kurs_usd REAL,
                    kurs_sar REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create liability_calculations table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS liability_calculations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    calculation_date TIMESTAMP NOT NULL,
                    total_jemaah INTEGER NOT NULL,
                    inflasi_saudi REAL NOT NULL,
                    kurs_usd REAL NOT NULL,
                    biaya_awal REAL NOT NULL,
                    tingkat_diskonto REAL NOT NULL,
                    total_liability REAL NOT NULL,
                    created_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create simulation_results table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS simulation_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    simulation_type TEXT NOT NULL,
                    scenario_name TEXT NOT NULL,
                    parameters TEXT NOT NULL,  -- JSON
                    results TEXT NOT NULL,     -- JSON
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create agent_executions table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    execution_time TIMESTAMP NOT NULL,
                    status TEXT NOT NULL,
                    parameters TEXT,           -- JSON
                    results TEXT,              -- JSON
                    error_message TEXT,
                    duration_seconds REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            self.logger.info("Database initialized successfully")
    
    @contextmanager
    def get_connection(self):
        """Get database connection with context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def insert_liability_calculation(self, params: Dict, result: float, created_by: str = "system") -> int:
        """Insert liability calculation result"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO liability_calculations 
                (calculation_date, total_jemaah, inflasi_saudi, kurs_usd, biaya_awal, 
                 tingkat_diskonto, total_liability, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now(),
                params.get('total_jemaah'),
                params.get('inflasi_saudi'),
                params.get('kurs_usd'),
                params.get('biaya_awal'),
                params.get('tingkat_diskonto'),
                result,
                created_by
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_liability_history(self, limit: int = 100) -> pd.DataFrame:
        """Get liability calculation history"""
        with self.get_connection() as conn:
            query = """
                SELECT * FROM liability_calculations 
                ORDER BY calculation_date DESC 
                LIMIT ?
            """
            return pd.read_sql_query(query, conn, params=[limit])
    
    def insert_agent_execution(self, agent_name: str, status: str, 
                             parameters: Dict = None, results: Dict = None, 
                             error_message: str = None, duration: float = None):
        """Insert agent execution log"""
        import json
        
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO agent_executions 
                (agent_name, execution_time, status, parameters, results, error_message, duration_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                agent_name,
                datetime.now(),
                status,
                json.dumps(parameters) if parameters else None,
                json.dumps(results, default=str) if results else None,
                error_message,
                duration
            ))
            conn.commit()
    
    def get_agent_performance(self, days: int = 30) -> pd.DataFrame:
        """Get agent performance statistics"""
        with self.get_connection() as conn:
            query = """
                SELECT 
                    agent_name,
                    COUNT(*) as total_executions,
                    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_executions,
                    AVG(duration_seconds) as avg_duration,
                    MAX(execution_time) as last_execution
                FROM agent_executions 
                WHERE execution_time >= datetime('now', '-{} days')
                GROUP BY agent_name
            """.format(days)
            return pd.read_sql_query(query, conn)
