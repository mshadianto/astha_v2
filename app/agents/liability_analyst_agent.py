# ===== app/agents/liability_analyst_agent.py =====
import numpy as np
import pandas as pd
from .base_agent import BaseAgent
from utils.calculations import LiabilityCalculator

class LiabilityAnalystAgent(BaseAgent):
    """Agent specialized in liability analysis and calculation"""
    
    def __init__(self):
        super().__init__(
            name="liability_analyst", 
            description="Menganalisis dan menghitung liabilitas keuangan haji"
        )
        self.calculator = LiabilityCalculator()
    
    def execute(self, analysis_type: str = "full", **params) -> Dict[str, Any]:
        """Execute liability analysis"""
        self.start_execution()
        
        try:
            result = {}
            
            if analysis_type in ["full", "basic"]:
                # Basic liability calculation
                total_liability, projections = self.calculator.calculate_total_liability(
                    total_jemaah=params.get('total_jemaah', 2500000),
                    inflasi_saudi=params.get('inflasi_saudi', 3.5),
                    kurs_usd=params.get('kurs_usd', 15500),
                    biaya_awal=params.get('biaya_awal', 94482028),
                    tingkat_diskonto=params.get('tingkat_diskonto', 6.5),
                    tahun_proyeksi=params.get('tahun_proyeksi', 20)
                )
                
                result['total_liability'] = total_liability
                result['projections'] = projections
            
            if analysis_type in ["full", "sensitivity"]:
                # Sensitivity analysis
                base_params = {
                    'total_jemaah': params.get('total_jemaah', 2500000),
                    'inflasi_saudi': params.get('inflasi_saudi', 3.5),
                    'kurs_usd': params.get('kurs_usd', 15500),
                    'biaya_awal': params.get('biaya_awal', 94482028),
                    'tingkat_diskonto': params.get('tingkat_diskonto', 6.5),
                    'tahun_proyeksi': params.get('tahun_proyeksi', 20)
                }
                
                sensitivity_params = {
                    'inflasi_saudi': [2.0, 3.5, 5.0, 6.5, 8.0],
                    'kurs_usd': [14000, 15500, 17000, 18500, 20000],
                    'tingkat_diskonto': [4.5, 6.5, 8.5, 10.5, 12.5]
                }
                
                sensitivity_results = self.calculator.sensitivity_analysis(
                    base_params, sensitivity_params
                )
                result['sensitivity_analysis'] = sensitivity_results
            
            if analysis_type in ["full", "scenarios"]:
                # Scenario analysis
                scenarios = self._run_scenario_analysis(params)
                result['scenarios'] = scenarios
            
            result['analysis_timestamp'] = datetime.now()
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
    
    def _run_scenario_analysis(self, base_params: Dict) -> List[Dict]:
        """Run various liability scenarios"""
        scenarios = [
            {
                'name': 'Base Case',
                'params': base_params,
                'description': 'Skenario dasar dengan parameter standar'
            },
            {
                'name': 'Optimistic',
                'params': {**base_params, 'inflasi_saudi': 2.0, 'kurs_usd': 14000},
                'description': 'Skenario optimis dengan inflasi rendah'
            },
            {
                'name': 'Pessimistic',
                'params': {**base_params, 'inflasi_saudi': 6.0, 'kurs_usd': 18000},
                'description': 'Skenario pesimis dengan inflasi tinggi'
            },
            {
                'name': 'Stress Test',
                'params': {**base_params, 'inflasi_saudi': 8.0, 'kurs_usd': 20000},
                'description': 'Skenario stress dengan kondisi ekstrem'
            }
        ]
        
        results = []
        for scenario in scenarios:
            liability, projections = self.calculator.calculate_total_liability(
                **scenario['params']
            )
            
            results.append({
                'name': scenario['name'],
                'description': scenario['description'],
                'total_liability': liability,
                'liability_trillions': liability / 1e12,
                'projections': projections[:5]  # First 5 years only
            })
        
        return results
