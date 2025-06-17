# ===== app/agents/orchestrator.py =====
from typing import Dict, List, Any
import asyncio
import logging
from datetime import datetime

from .data_collector_agent import DataCollectorAgent
from .liability_analyst_agent import LiabilityAnalystAgent
from .investment_simulation_agent import InvestmentSimulationAgent

class AgentOrchestrator:
    """Orchestrates and coordinates all AI agents"""
    
    def __init__(self):
        self.agents = {
            'data_collector': DataCollectorAgent(),
            'liability_analyst': LiabilityAnalystAgent(),
            'investment_simulation': InvestmentSimulationAgent()
        }
        self.logger = logging.getLogger("orchestrator")
        self.execution_history = []
    
    def get_all_agents_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {name: agent.get_status() for name, agent in self.agents.items()}
    
    def execute_agent(self, agent_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a specific agent"""
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not found")
        
        agent = self.agents[agent_name]
        self.logger.info(f"Executing agent: {agent_name}")
        
        result = agent.execute(**kwargs)
        
        # Log execution
        self.execution_history.append({
            'agent': agent_name,
            'timestamp': datetime.now(),
            'result': result,
            'success': result.get('status') == 'success'
        })
        
        return result
    
    def run_daily_analysis(self) -> Dict[str, Any]:
        """Run comprehensive daily analysis using all agents"""
        self.logger.info("Starting daily analysis workflow")
        
        results = {}
        
        try:
            # Step 1: Collect latest data
            self.logger.info("Step 1: Collecting external data")
            data_result = self.execute_agent('data_collector')
            results['data_collection'] = data_result
            
            if data_result.get('status') != 'success':
                raise Exception("Data collection failed")
            
            # Step 2: Analyze liability with latest parameters
            self.logger.info("Step 2: Analyzing liability")
            
            # Extract parameters from collected data
            exchange_rates = data_result['data'].get('exchange_rates', {})
            economic_indicators = data_result['data'].get('economic_indicators', {})
            
            liability_params = {
                'total_jemaah': 2500000,
                'inflasi_saudi': economic_indicators.get('saudi_inflation', 3.5),
                'kurs_usd': exchange_rates.get('USD', 15500),
                'biaya_awal': 94482028,
                'tingkat_diskonto': economic_indicators.get('bi_rate', 6.5),
                'analysis_type': 'full'
            }
            
            liability_result = self.execute_agent('liability_analyst', **liability_params)
            results['liability_analysis'] = liability_result
            
            # Step 3: Run investment simulation
            self.logger.info("Step 3: Running investment simulation")
            
            investment_params = {
                'simulation_type': 'portfolio_optimization',
                'portfolio_value': 180.5e12
            }
            
            investment_result = self.execute_agent('investment_simulation', **investment_params)
            results['investment_simulation'] = investment_result
            
            # Step 4: Generate summary
            self.logger.info("Step 4: Generating analysis summary")
            summary = self._generate_analysis_summary(results)
            results['summary'] = summary
            
            self.logger.info("Daily analysis completed successfully")
            
            return {
                'status': 'success',
                'timestamp': datetime.now(),
                'results': results
            }
            
        except Exception as e:
            self.logger.error(f"Daily analysis failed: {str(e)}")
            return {
                'status': 'failed',
                'timestamp': datetime.now(),
                'error': str(e),
                'partial_results': results
            }
    
    def _generate_analysis_summary(self, results: Dict) -> Dict[str, Any]:
        """Generate executive summary from all analysis results"""
        summary = {
            'timestamp': datetime.now(),
            'key_metrics': {},
            'alerts': [],
            'recommendations': []
        }
        
        # Extract key metrics
        if 'liability_analysis' in results and results['liability_analysis'].get('status') == 'success':
            liability_data = results['liability_analysis']
            total_liability = liability_data.get('total_liability', 0)
            
            summary['key_metrics']['total_liability_trillions'] = total_liability / 1e12
            summary['key_metrics']['liability_status'] = 'normal' if total_liability < 200e12 else 'high'
        
        if 'investment_simulation' in results and results['investment_simulation'].get('status') == 'success':
            investment_data = results['investment_simulation']
            if 'optimal_expected_return' in investment_data:
                summary['key_metrics']['expected_return'] = investment_data['optimal_expected_return']
                summary['key_metrics']['return_status'] = 'good' if investment_data['optimal_expected_return'] > 0.07 else 'low'
        
        # Generate alerts
        if summary['key_metrics'].get('liability_status') == 'high':
            summary['alerts'].append({
                'level': 'warning',
                'message': 'Total liabilitas melebihi Rp 200 triliun',
                'action_required': True
            })
        
        if summary['key_metrics'].get('return_status') == 'low':
            summary['alerts'].append({
                'level': 'info',
                'message': 'Expected return di bawah target 7%',
                'action_required': False
            })
        
        # Generate recommendations
        summary['recommendations'] = [
            'Review alokasi portofolio untuk optimalisasi return',
            'Monitor perkembangan inflasi Saudi secara berkala',
            'Pertimbangkan hedging currency untuk mitigasi risiko kurs'
        ]
        
        return summary
