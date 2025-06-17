# ===== utils/calculations.py =====
import numpy as np
import pandas as pd

class LiabilityCalculator:
    """Actuarial liability calculation engine"""
    
    @staticmethod
    def calculate_total_liability(
        total_jemaah: int,
        inflasi_saudi: float,
        kurs_usd: float,
        biaya_awal: float,
        tingkat_diskonto: float,
        tahun_proyeksi: int = 20,
        depresiasi_rupiah: float = 3.0
    ):
        """
        Calculate total present value of hajj liability
        
        Formula: L_total = Σ (C_t × J_t) / (1+r)^t
        """
        total_liability = 0
        jemaah_per_tahun = total_jemaah / tahun_proyeksi
        projections = []
        
        for t in range(1, tahun_proyeksi + 1):
            # C_t = C_0 × (1 + inflasi_saudi)^t × (1 + depresiasi_rupiah)^t
            biaya_tahun_t = biaya_awal * \
                           (1 + inflasi_saudi/100)**t * \
                           (1 + depresiasi_rupiah/100)**t
            
            # Present Value = Future Value / (1 + discount_rate)^t
            present_value = (biaya_tahun_t * jemaah_per_tahun) / \
                           (1 + tingkat_diskonto/100)**t
            
            total_liability += present_value
            
            projections.append({
                'tahun': 2025 + t,
                'biaya_per_jemaah': biaya_tahun_t,
                'jemaah': jemaah_per_tahun,
                'total_biaya': biaya_tahun_t * jemaah_per_tahun,
                'present_value': present_value
            })
        
        return total_liability, projections
    
    @staticmethod
    def sensitivity_analysis(
        base_params: dict,
        sensitivity_params: dict
    ):
        """Perform sensitivity analysis on key parameters"""
        results = []
        
        for param_name, param_values in sensitivity_params.items():
            for value in param_values:
                params = base_params.copy()
                params[param_name] = value
                
                liability, _ = LiabilityCalculator.calculate_total_liability(**params)
                base_liability, _ = LiabilityCalculator.calculate_total_liability(**base_params)
                
                change_pct = ((liability - base_liability) / base_liability) * 100
                
                results.append({
                    'parameter': param_name,
                    'value': value,
                    'liability': liability,
                    'change_percent': change_pct
                })
        
        return results

class StressTestEngine:
    """Stress testing and scenario analysis"""
    
    @staticmethod
    def run_stress_scenarios(base_assets: float, base_liability: float):
        """Run predefined stress test scenarios"""
        scenarios = {
            "Skenario Dasar": {
                "liability_mult": 1.0,
                "asset_mult": 1.0,
                "description": "Kondisi normal tanpa shock eksternal"
            },
            "Resesi Global": {
                "liability_mult": 1.15,
                "asset_mult": 0.85,
                "description": "Imbal hasil investasi turun, biaya naik"
            },
            "Depresiasi Rupiah Ekstrem": {
                "liability_mult": 1.45,
                "asset_mult": 0.95,
                "description": "Rupiah melemah 30% dalam 2 tahun"
            },
            "Inflasi Saudi Tinggi": {
                "liability_mult": 1.25,
                "asset_mult": 1.02,
                "description": "Inflasi Saudi mencapai 8% per tahun"
            },
            "Shock Ganda": {
                "liability_mult": 1.60,
                "asset_mult": 0.80,
                "description": "Kombinasi resesi + depresiasi + inflasi"
            }
        }
        
        results = []
        for scenario_name, params in scenarios.items():
            scenario_liability = base_liability * params["liability_mult"]
            scenario_assets = base_assets * params["asset_mult"]
            solvency_ratio = scenario_assets / scenario_liability
            
            status = "Aman" if solvency_ratio >= 1.2 else \
                    "Waspada" if solvency_ratio >= 1.0 else "Risiko Tinggi"
            
            results.append({
                'scenario': scenario_name,
                'description': params['description'],
                'assets': scenario_assets,
                'liability': scenario_liability,
                'solvency_ratio': solvency_ratio,
                'status': status
            })
        
        return results
    
    @staticmethod
    def monte_carlo_simulation(
        base_assets: float, 
        base_liability: float, 
        n_simulations: int = 1000
    ):
        """Run Monte Carlo simulation for risk assessment"""
        np.random.seed(42)
        
        # Random factors with normal distribution
        liability_factors = np.random.normal(1.0, 0.15, n_simulations)
        asset_factors = np.random.normal(1.0, 0.10, n_simulations)
        
        # Ensure factors are positive
        liability_factors = np.abs(liability_factors)
        asset_factors = np.abs(asset_factors)
        
        simulated_solvency = (base_assets * asset_factors) / (base_liability * liability_factors)
        
        results = {
            'solvency_ratios': simulated_solvency,
            'mean_solvency': np.mean(simulated_solvency),
            'std_solvency': np.std(simulated_solvency),
            'safe_probability': (simulated_solvency >= 1.0).mean() * 100,
            'worst_case': np.min(simulated_solvency),
            'best_case': np.max(simulated_solvency)
        }
        
        return results
