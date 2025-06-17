# ===== tests/integration/test_database.py =====
import pytest
import json
from models.database import DatabaseManager

class TestDatabaseManager:
    """Test database manager functionality"""
    
    def test_database_initialization(self, temp_db):
        """Test database initialization"""
        db_manager = DatabaseManager(temp_db)
        
        # Check that tables were created
        with db_manager.get_connection() as conn:
            cursor = conn.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = [
                'jemaah_data', 'biaya_haji', 'liability_calculations', 
                'simulation_results', 'agent_executions'
            ]
            
            for table in expected_tables:
                assert table in tables
    
    def test_liability_calculation_storage(self, temp_db, sample_liability_params):
        """Test storing liability calculation results"""
        db_manager = DatabaseManager(temp_db)
        
        # Insert calculation
        result_id = db_manager.insert_liability_calculation(
            sample_liability_params, 145.2e12, "test_user"
        )
        
        assert result_id > 0
        
        # Retrieve history
        history = db_manager.get_liability_history(limit=1)
        assert len(history) == 1
        assert history.iloc[0]['total_liability'] == 145.2e12
        assert history.iloc[0]['created_by'] == "test_user"
    
    def test_agent_execution_logging(self, temp_db):
        """Test agent execution logging"""
        db_manager = DatabaseManager(temp_db)
        
        # Log execution
        db_manager.insert_agent_execution(
            agent_name="test_agent",
            status="success",
            parameters={"param1": "value1"},
            results={"result1": 100},
            duration=1.5
        )
        
        # Get performance stats
        performance = db_manager.get_agent_performance(days=1)
        assert len(performance) == 1
        assert performance.iloc[0]['agent_name'] == "test_agent"
        assert performance.iloc[0]['total_executions'] == 1
        assert performance.iloc[0]['successful_executions'] == 1
