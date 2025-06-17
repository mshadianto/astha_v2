# ===== tests/unit/test_calculations.py =====
import pytest
import numpy as np
from utils.calculations import LiabilityCalculator, StressTestEngine

class TestLiabilityCalculator:
    """Test liability calculation functions"""
    
    def test_basic_liability_calculation(self, sample_liability_params):
        """Test basic liability calculation"""
        total_liability, projections = LiabilityCalculator.calculate_total_liability(
            **sample_liability_params
        )
        
        # Assert results are reasonable
        assert total_liability > 0
        assert len(projections) == sample_liability_params['tahun_proyeksi']
        assert all(proj['present_value'] > 0 for proj in projections)
        
        # Test that liability is in expected range (100-300 trillion)
        assert 100e12 < total_liability < 300e12
    
    def test_inflation_impact(self, sample_liability_params):
        """Test that higher inflation increases liability"""
        # Base case
        base_liability, _ = LiabilityCalculator.calculate_total_liability(
            **sample_liability_params
        )
        
        # High inflation case
        high_inflation_params = sample_liability_params.copy()
        high_inflation_params['inflasi_saudi'] = 6.0
        
        high_liability, _ = LiabilityCalculator.calculate_total_liability(
            **high_inflation_params
        )
        
        # Higher inflation should increase liability
        assert high_liability > base_liability
    
    def test_discount_rate_impact(self, sample_liability_params):
        """Test that higher discount rate decreases present value"""
        # Low discount rate
        low_discount_params = sample_liability_params.copy()
        low_discount_params['tingkat_diskonto'] = 4.0
        
        low_liability, _ = LiabilityCalculator.calculate_total_liability(
            **low_discount_params
        )
        
        # High discount rate
        high_discount_params = sample_liability_params.copy()
        high_discount_params['tingkat_diskonto'] = 10.0
        
        high_liability, _ = LiabilityCalculator.calculate_total_liability(
            **high_discount_params
        )
        
        # Higher discount rate should decrease present value
        assert low_liability > high_liability
    
    def test_sensitivity_analysis(self, sample_liability_params):
        """Test sensitivity analysis function"""
        sensitivity_params = {
            'inflasi_saudi': [2.0, 3.5, 5.0],
            'kurs_usd': [14000, 15500, 17000]
        }
        
        results = LiabilityCalculator.sensitivity_analysis(
            sample_liability_params, sensitivity_params
        )
        
        assert len(results) == 6  # 3 + 3 scenarios
        assert all('parameter' in result for result in results)
        assert all('liability' in result for result in results)
        assert all('change_percent' in result for result in results)

class TestStressTestEngine:
    """Test stress testing functions"""
    
    def test_stress_scenarios(self):
        """Test stress test scenarios"""
        base_assets = 180.5e12
        base_liability = 145.2e12
        
        results = StressTestEngine.run_stress_scenarios(base_assets, base_liability)
        
        assert len(results) == 5  # 5 scenarios
        assert all('solvency_ratio' in result for result in results)
        assert all('status' in result for result in results)
        
        # Base scenario should have ratio > 1
        base_scenario = next(r for r in results if r['scenario'] == 'Skenario Dasar')
        assert base_scenario['solvency_ratio'] > 1.0
    
    def test_monte_carlo_simulation(self):
        """Test Monte Carlo simulation"""
        base_assets = 180.5e12
        base_liability = 145.2e12
        
        results = StressTestEngine.monte_carlo_simulation(
            base_assets, base_liability, n_simulations=100
        )
        
        assert 'solvency_ratios' in results
        assert len(results['solvency_ratios']) == 100
        assert 'mean_solvency' in results
        assert 'safe_probability' in results
        assert 0 <= results['safe_probability'] <= 100

# ===== tests/unit/test_agents.py =====
import pytest
from unittest.mock import Mock, patch
from agents.data_collector_agent import DataCollectorAgent
from agents.liability_analyst_agent import LiabilityAnalystAgent
from agents.orchestrator import AgentOrchestrator

class TestDataCollectorAgent:
    """Test data collector agent"""
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        agent = DataCollectorAgent()
        assert agent.name == "data_collector"
        assert agent.status == "idle"
    
    @patch('services.api_service.APIService.get_exchange_rates')
    @patch('services.api_service.APIService.get_economic_indicators')
    def test_data_collection(self, mock_economic, mock_exchange):
        """Test data collection execution"""
        # Mock API responses
        mock_exchange.return_value = {'USD': 15500, 'SAR': 4133}
        mock_economic.return_value = {'saudi_inflation': 3.2, 'bi_rate': 6.0}
        
        agent = DataCollectorAgent()
        result = agent.execute(['exchange_rates', 'economic_indicators'])
        
        assert result['status'] == 'success'
        assert 'data' in result
        assert 'exchange_rates' in result['data']
        assert 'economic_indicators' in result['data']

class TestLiabilityAnalystAgent:
    """Test liability analyst agent"""
    
    def test_basic_analysis(self, sample_liability_params):
        """Test basic liability analysis"""
        agent = LiabilityAnalystAgent()
        result = agent.execute(analysis_type="basic", **sample_liability_params)
        
        assert result['status'] == 'success'
        assert 'total_liability' in result
        assert 'projections' in result
        assert result['total_liability'] > 0
    
    def test_full_analysis(self, sample_liability_params):
        """Test full liability analysis"""
        agent = LiabilityAnalystAgent()
        result = agent.execute(analysis_type="full", **sample_liability_params)
        
        assert result['status'] == 'success'
        assert 'total_liability' in result
        assert 'sensitivity_analysis' in result
        assert 'scenarios' in result

class TestAgentOrchestrator:
    """Test agent orchestrator"""
    
    def test_orchestrator_initialization(self):
        """Test orchestrator initialization"""
        orchestrator = AgentOrchestrator()
        assert len(orchestrator.agents) == 3
        assert 'data_collector' in orchestrator.agents
        assert 'liability_analyst' in orchestrator.agents
        assert 'investment_simulation' in orchestrator.agents
    
    def test_agent_status_retrieval(self):
        """Test getting all agents status"""
        orchestrator = AgentOrchestrator()
        status = orchestrator.get_all_agents_status()
        
        assert len(status) == 3
        for agent_status in status.values():
            assert 'name' in agent_status
            assert 'status' in agent_status
