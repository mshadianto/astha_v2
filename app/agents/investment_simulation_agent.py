# ===== app/agents/investment_simulation_agent.py =====
import numpy as np
import pandas as pd
from .base_agent import BaseAgent

class InvestmentSimulationAgent(BaseAgent):
    """Agent for investment portfolio simulation and optimization"""
    
    def __init__(self):
        super().__init__(
            name="investment_simulation",
            description="Mensimulasikan dan mengoptimalkan portofolio investasi"
        )
    
    def execute(self, simulation_type: str = "portfolio_optimization", **params) -> Dict[str, Any]:
        """Execute investment simulation"""
        self.start_execution()
        
        try:
            result = {}
            
            if simulation_type == "portfolio_optimization":
                result = self._optimize_portfolio(params)
            elif simulation_type == "stress_test":
                result = self._run_investment_stress_test(params)
            elif simulation_type == "monte_carlo":
                result = self._monte_carlo_simulation(params)
            elif simulation_type == "asset_allocation":
                result = self._asset_allocation_analysis(params)
            
            result['simulation_timestamp'] = datetime.now()
            result['status'] = 'success'
            
            self.complete_execution(result)
            return result
            
        except Exception as e:
            self.fail_execution(str(e))
            return {
                'timestamp': datetime.now(),
                'error': str(e),
                'status': 'failed'
            }
    
    def _optimize_portfolio(self, params: Dict) -> Dict[str, Any]:
        """Optimize investment portfolio allocation"""
        # Asset classes and their historical returns (simulated)
        assets = {
            'Sukuk Negara': {'return': 6.5, 'volatility': 2.1, 'shariah': True},
            'Sukuk Korporasi': {'return': 7.2, 'volatility': 3.5, 'shariah': True},
            'Saham Syariah': {'return': 12.8, 'volatility': 18.2, 'shariah': True},
            'Deposito Syariah': {'return': 5.8, 'volatility': 0.5, 'shariah': True},
            'Emas': {'return': 8.5, 'volatility': 15.8, 'shariah': True},
            'Real Estate': {'return': 9.2, 'volatility': 12.5, 'shariah': True}
        }
        
        # Current allocation (example)
        current_allocation = {
            'Sukuk Negara': 45,
            'Sukuk Korporasi': 20,
            'Saham Syariah': 15,
            'Deposito Syariah': 10,
            'Emas': 5,
            'Real Estate': 5
        }
        
        # Optimal allocation based on risk-return optimization
        optimal_allocation = {
            'Sukuk Negara': 40,
            'Sukuk Korporasi': 25,
            'Saham Syariah': 20,
            'Deposito Syariah': 5,
            'Emas': 5,
            'Real Estate': 5
        }
        
        # Calculate portfolio metrics
        current_return = sum(current_allocation[asset] * assets[asset]['return'] / 100 for asset in assets)
        optimal_return = sum(optimal_allocation[asset] * assets[asset]['return'] / 100 for asset in assets)
        
        current_risk = np.sqrt(sum((current_allocation[asset] * assets[asset]['volatility'] / 100) ** 2 for asset in assets))
        optimal_risk = np.sqrt(sum((optimal_allocation[asset] * assets[asset]['volatility'] / 100) ** 2 for asset in assets))
        
        return {
            'assets': assets,
            'current_allocation': current_allocation,
            'optimal_allocation': optimal_allocation,
            'current_expected_return': current_return,
            'optimal_expected_return': optimal_return,
            'current_risk': current_risk,
            'optimal_risk': optimal_risk,
            'sharpe_improvement': (optimal_return - 0.06) / optimal_risk - (current_return - 0.06) / current_risk
        }
    
    def _run_investment_stress_test(self, params: Dict) -> Dict[str, Any]:
        """Run stress test on investment portfolio"""
        base_portfolio_value = params.get('portfolio_value', 180.5e12)  # 180.5 trillion
        
        stress_scenarios = {
            'Global Recession': {
                'equity_shock': -30,
                'bond_shock': -5,
                'commodity_shock': -20,
                'real_estate_shock': -15
            },
            'Interest Rate Spike': {
                'equity_shock': -15,
                'bond_shock': -12,
                'commodity_shock': 5,
                'real_estate_shock': -8
            },
            'Currency Crisis': {
                'equity_shock': -25,
                'bond_shock': 10,
                'commodity_shock': 15,
                'real_estate_shock': -10
            },
            'Geopolitical Shock': {
                'equity_shock': -20,
                'bond_shock': -3,
                'commodity_shock': 25,
                'real_estate_shock': -5
            }
        }
        
        # Current allocation
        allocation = {
            'equity': 0.20,  # 20% stocks
            'bonds': 0.65,   # 65% bonds
            'commodities': 0.05,  # 5% commodities
            'real_estate': 0.10   # 10% real estate
        }
        
        stress_results = {}
        for scenario_name, shocks in stress_scenarios.items():
            total_shock = (
                allocation['equity'] * shocks['equity_shock'] +
                allocation['bonds'] * shocks['bond_shock'] +
                allocation['commodities'] * shocks['commodity_shock'] +
                allocation['real_estate'] * shocks['real_estate_shock']
            )
            
            portfolio_value_after = base_portfolio_value * (1 + total_shock / 100)
            loss_amount = base_portfolio_value - portfolio_value_after
            
            stress_results[scenario_name] = {
                'total_shock_percent': total_shock,
                'portfolio_value_after': portfolio_value_after,
                'loss_amount': loss_amount,
                'loss_trillions': loss_amount / 1e12
            }
        
        return {
            'base_portfolio_value': base_portfolio_value,
            'stress_scenarios': stress_results,
            'worst_case_loss': max(result['loss_amount'] for result in stress_results.values()),
            'allocation': allocation
        }
    
    def _monte_carlo_simulation(self, params: Dict) -> Dict[str, Any]:
        """Run Monte Carlo simulation for portfolio returns"""
        n_simulations = params.get('n_simulations', 1000)
        time_horizon = params.get('time_horizon', 5)  # years
        initial_value = params.get('initial_value', 180.5e12)
        
        # Portfolio parameters
        expected_return = 0.078  # 7.8% annual return
        volatility = 0.12       # 12% annual volatility
        
        np.random.seed(42)
        
        # Generate random returns
        random_returns = np.random.normal(expected_return, volatility, (n_simulations, time_horizon))
        
        # Calculate portfolio values over time
        portfolio_paths = np.zeros((n_simulations, time_horizon + 1))
        portfolio_paths[:, 0] = initial_value
        
        for t in range(time_horizon):
            portfolio_paths[:, t + 1] = portfolio_paths[:, t] * (1 + random_returns[:, t])
        
        # Final values
        final_values = portfolio_paths[:, -1]
        
        # Calculate statistics
        percentiles = np.percentile(final_values, [5, 10, 25, 50, 75, 90, 95])
        
        return {
            'n_simulations': n_simulations,
            'time_horizon': time_horizon,
            'initial_value': initial_value,
            'final_values': final_values.tolist(),
            'mean_final_value': np.mean(final_values),
            'std_final_value': np.std(final_values),
            'percentiles': {
                '5th': percentiles[0],
                '10th': percentiles[1], 
                '25th': percentiles[2],
                '50th': percentiles[3],
                '75th': percentiles[4],
                '90th': percentiles[5],
                '95th': percentiles[6]
            },
            'probability_of_loss': (final_values < initial_value).mean() * 100,
            'expected_return_annual': ((np.mean(final_values) / initial_value) ** (1/time_horizon) - 1) * 100
        }
