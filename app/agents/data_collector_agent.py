# ===== app/agents/data_collector_agent.py =====
import requests
import pandas as pd
from datetime import datetime, timedelta
from .base_agent import BaseAgent
from services.api_service import APIService

class DataCollectorAgent(BaseAgent):
    """Agent responsible for collecting external data"""
    
    def __init__(self):
        super().__init__(
            name="data_collector",
            description="Mengumpulkan data real-time dari sumber eksternal"
        )
        self.api_service = APIService()
        
    def execute(self, data_sources: List[str] = None) -> Dict[str, Any]:
        """Collect data from various external sources"""
        self.start_execution()
        
        try:
            collected_data = {}
            
            # Collect exchange rates
            if not data_sources or 'exchange_rates' in data_sources:
                exchange_rates = self.api_service.get_exchange_rates()
                collected_data['exchange_rates'] = exchange_rates
            
            # Collect economic indicators  
            if not data_sources or 'economic_indicators' in data_sources:
                economic_data = self.api_service.get_economic_indicators()
                collected_data['economic_indicators'] = economic_data
            
            # Collect market data (simulated)
            if not data_sources or 'market_data' in data_sources:
                market_data = self._collect_market_data()
                collected_data['market_data'] = market_data
            
            # Collect BI data (simulated)
            if not data_sources or 'bi_data' in data_sources:
                bi_data = self._collect_bi_data()
                collected_data['bi_data'] = bi_data
            
            result = {
                'timestamp': datetime.now(),
                'data': collected_data,
                'sources_count': len(collected_data),
                'status': 'success'
            }
            
            self.complete_execution(result)
            return result
            
        except Exception as e:
            self.fail_execution(str(e))
            return {
                'timestamp': datetime.now(),
                'error': str(e),
                'status': 'failed'
            }
    
    def _collect_market_data(self) -> Dict[str, Any]:
        """Collect financial market data"""
        # Simulated market data - replace with real API calls
        return {
            'sukuk_yield_10y': 6.85,
            'corporate_bond_yield': 7.25,
            'equity_index': 7245.82,
            'gold_price_usd': 2065.50,
            'oil_price_brent': 82.15,
            'timestamp': datetime.now()
        }
    
    def _collect_bi_data(self) -> Dict[str, Any]:
        """Collect Bank Indonesia data"""
        # Simulated BI data - replace with real API calls
        return {
            'bi_rate': 6.00,
            'inflation_mom': 0.15,
            'inflation_yoy': 2.75,
            'money_supply_growth': 8.5,
            'timestamp': datetime.now()
        }
