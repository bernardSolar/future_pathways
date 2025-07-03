"""
Enhanced Empirical Analysis using Comprehensive Historical Dataset (1970-2024)

This script performs empirical parameter estimation for civilization dynamics
using the expanded 55-year dataset, significantly improving on our initial
7-point analysis.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize
from mpl_toolkits.mplot3d import Axes3D
import os


class EnhancedEmpiricalAnalysis:
    def __init__(self, data_file="data/civilization_dynamics_1970_2024.csv"):
        """Load and prepare the comprehensive historical dataset"""
        self.data_file = data_file
        self.load_data()
        self.calculate_derivatives()
        
    def load_data(self):
        """Load the CSV dataset"""
        if os.path.exists(self.data_file):
            self.df = pd.read_csv(self.data_file)
        else:
            # Fallback to embedded data if file not found
            print(f"Warning: {self.data_file} not found, using embedded data")
            self.create_embedded_data()
            
        print(f"Loaded dataset: {len(self.df)} observations from {self.df['year'].min()} to {self.df['year'].max()}")
        print(f"Variables: CO2 ({self.df['co2_emissions_gt'].min():.1f}-{self.df['co2_emissions_gt'].max():.1f} GT), "
              f"Materials ({self.df['material_use_gt'].min():.1f}-{self.df['material_use_gt'].max():.1f} GT), "
              f"Growth ({self.df['gdp_growth_percent'].min():.1f}-{self.df['gdp_growth_percent'].max():.1f}%)")
    
    def create_embedded_data(self):
        """Fallback embedded dataset"""
        years = list(range(1970, 2025))
        co2_base = np.linspace(14.836, 50.0, len(years))
        materials_base = np.linspace(27.1, 106.0, len(years))
        growth_base = [3.4, 3.3, 3.2, 3.1, 3.0, 2.9, 2.8, 2.8, 2.8, 2.8,
                      2.8, 2.8, 2.9, 3.0, 3.1, 3.1, 3.1, 3.1, 3.1, 3.1,
                      3.1, 3.2, 3.3, 3.3, 3.3, 3.3, 4.4, 3.9, 4.0, 4.1,
                      4.2, 4.3, 4.2, 4.1, 4.0, 3.9, 3.8, 3.7, 3.6, 3.5,
                      3.4, 3.3, 3.2, 3.1, 3.0, 2.9, -3.3, -1.0, 0.5, 1.5,
                      2.0, 2.2, 2.3, 2.4, 2.5]
        
        self.df = pd.DataFrame({
            'year': years,
            'co2_emissions_gt': co2_base,
            'material_use_gt': materials_base, 
            'gdp_growth_percent': growth_base[:len(years)],
            'data_quality': ['interpolated'] * len(years)
        })
    
    def calculate_derivatives(self):
        """Calculate time derivatives for all variables"""
        self.df = self.df.sort_values('year').reset_index(drop=True)
        
        # Calculate derivatives using central differences (more accurate than forward/backward)
        self.df['dCO2_dt'] = np.gradient(self.df['co2_emissions_gt'], self.df['year'])
        self.df['dMaterials_dt'] = np.gradient(self.df['material_use_gt'], self.df['year'])
        self.df['dGrowth_dt'] = np.gradient(self.df['gdp_growth_percent'], self.df['year'])
        
        print("Calculated derivatives using central difference method")
        print(f"dCO2/dt range: {self.df['dCO2_dt'].min():.3f} to {self.df['dCO2_dt'].max():.3f}")
        print(f"dMaterials/dt range: {self.df['dMaterials_dt'].min():.3f} to {self.df['dMaterials_dt'].max():.3f}")
        print(f"dGrowth/dt range: {self.df['dGrowth_dt'].min():.3f} to {self.df['dGrowth_dt'].max():.3f}")
    
    def analyze_lorenz_relationships(self):
        """Test Lorenz-like relationships with the full dataset"""
        print("\\n=== Testing Lorenz-like Relationships (1970-2024) ===")
        
        # Extract variables
        co2 = self.df['co2_emissions_gt'].values
        materials = self.df['material_use_gt'].values
        growth = self.df['gdp_growth_percent'].values
        dco2_dt = self.df['dCO2_dt'].values
        dmaterials_dt = self.df['dMaterials_dt'].values
        dgrowth_dt = self.df['dGrowth_dt'].values
        
        # Test Equation 1: dCO2/dt = σ(Materials - CO2)
        materials_co2_diff = materials - co2
        mask1 = np.abs(materials_co2_diff) > 0.1  # Avoid division by near-zero
        sigma_estimates = dco2_dt[mask1] / materials_co2_diff[mask1]
        sigma_mean = np.mean(sigma_estimates)
        sigma_std = np.std(sigma_estimates)
        
        print(f"\\nEquation 1: dCO2/dt = σ(Materials - CO2)")
        print(f"σ = {sigma_mean:.4f} ± {sigma_std:.4f}")
        print(f"R² = {self.calculate_r_squared(dco2_dt[mask1], sigma_mean * materials_co2_diff[mask1]):.3f}")
        
        # Test Equation 2: dMaterials/dt = CO2*(ρ - Growth) - Materials  
        # Rearranged: ρ = (dMat/dt + Materials)/CO2 + Growth
        mask2 = co2 > 1.0  # Avoid division by small CO2 values
        rho_estimates = (dmaterials_dt[mask2] + materials[mask2]) / co2[mask2] + growth[mask2]
        rho_mean = np.mean(rho_estimates)
        rho_std = np.std(rho_estimates)
        
        print(f"\\nEquation 2: dMaterials/dt = CO2*(ρ - Growth) - Materials")
        print(f"ρ = {rho_mean:.2f} ± {rho_std:.2f}")
        predicted_dmaterials = co2[mask2] * (rho_mean - growth[mask2]) - materials[mask2]
        print(f"R² = {self.calculate_r_squared(dmaterials_dt[mask2], predicted_dmaterials):.3f}")
        
        # Test Equation 3: dGrowth/dt = CO2*Materials*α - β*Growth
        # This is more complex, let's use least squares fitting
        mask3 = np.abs(growth) > 0.1
        X = np.column_stack([co2[mask3] * materials[mask3], -growth[mask3]])
        y = dgrowth_dt[mask3]
        
        # Solve least squares: [α, β] = (X^T X)^(-1) X^T y
        try:
            params = np.linalg.lstsq(X, y, rcond=None)[0]
            alpha, beta = params
            predicted_dgrowth = X @ params
            r2_growth = self.calculate_r_squared(y, predicted_dgrowth)
            
            print(f"\\nEquation 3: dGrowth/dt = α*CO2*Materials - β*Growth")
            print(f"α = {alpha:.6f}")
            print(f"β = {beta:.3f}")
            print(f"R² = {r2_growth:.3f}")
        except np.linalg.LinAlgError:
            print(f"\\nEquation 3: Could not fit - matrix singular")
            alpha, beta = 0, 1
        
        return {
            'sigma': sigma_mean,
            'rho': rho_mean, 
            'alpha': alpha,
            'beta': beta,
            'sigma_std': sigma_std,
            'rho_std': rho_std
        }
    
    def calculate_r_squared(self, y_true, y_pred):
        """Calculate R-squared coefficient"""
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        return 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
    
    def plot_comprehensive_analysis(self, params):
        """Create comprehensive visualization of the analysis"""
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Time series of all variables
        ax1 = plt.subplot(3, 4, 1)
        ax1.plot(self.df['year'], self.df['co2_emissions_gt'], 'b-', linewidth=2, label='CO2 Emissions')
        ax1.set_ylabel('CO2 Emissions (GT/yr)')
        ax1.set_title('Historical CO2 Emissions')
        ax1.grid(True)
        
        ax2 = plt.subplot(3, 4, 2)
        ax2.plot(self.df['year'], self.df['material_use_gt'], 'g-', linewidth=2)
        ax2.set_ylabel('Material Use (GT/yr)')
        ax2.set_title('Historical Material Use')
        ax2.grid(True)
        
        ax3 = plt.subplot(3, 4, 3)
        ax3.plot(self.df['year'], self.df['gdp_growth_percent'], 'r-', linewidth=2)
        ax3.set_ylabel('GDP Growth (%/yr)')
        ax3.set_title('Historical Economic Growth')
        ax3.grid(True)
        
        # 2. Derivatives
        ax4 = plt.subplot(3, 4, 4)
        ax4.plot(self.df['year'], self.df['dCO2_dt'], 'b-', alpha=0.7)
        ax4.plot(self.df['year'], self.df['dMaterials_dt'], 'g-', alpha=0.7)
        ax4.plot(self.df['year'], self.df['dGrowth_dt'], 'r-', alpha=0.7)
        ax4.set_ylabel('Rate of Change')
        ax4.set_title('Time Derivatives')
        ax4.legend(['dCO2/dt', 'dMat/dt', 'dGrowth/dt'])
        ax4.grid(True)
        
        # 3. Phase space plots
        ax5 = plt.subplot(3, 4, 5)
        scatter = ax5.scatter(self.df['co2_emissions_gt'], self.df['material_use_gt'], 
                             c=self.df['year'], cmap='viridis', alpha=0.7)
        ax5.set_xlabel('CO2 Emissions (GT/yr)')
        ax5.set_ylabel('Material Use (GT/yr)')
        ax5.set_title('CO2 vs Materials Phase Space')
        plt.colorbar(scatter, ax=ax5, label='Year')
        
        ax6 = plt.subplot(3, 4, 6)
        ax6.scatter(self.df['co2_emissions_gt'], self.df['gdp_growth_percent'], 
                   c=self.df['year'], cmap='plasma', alpha=0.7)
        ax6.set_xlabel('CO2 Emissions (GT/yr)')
        ax6.set_ylabel('GDP Growth (%/yr)')
        ax6.set_title('CO2 vs Growth Phase Space')
        
        ax7 = plt.subplot(3, 4, 7)
        ax7.scatter(self.df['material_use_gt'], self.df['gdp_growth_percent'], 
                   c=self.df['year'], cmap='coolwarm', alpha=0.7)
        ax7.set_xlabel('Material Use (GT/yr)')
        ax7.set_ylabel('GDP Growth (%/yr)')
        ax7.set_title('Materials vs Growth Phase Space')
        
        # 4. 3D trajectory
        ax8 = plt.subplot(3, 4, 8, projection='3d')
        ax8.plot(self.df['co2_emissions_gt'], self.df['material_use_gt'], 
                self.df['gdp_growth_percent'], 'k-', alpha=0.6, linewidth=1)
        ax8.scatter(self.df['co2_emissions_gt'].iloc[0], self.df['material_use_gt'].iloc[0], 
                   self.df['gdp_growth_percent'].iloc[0], color='green', s=100, label='1970')
        ax8.scatter(self.df['co2_emissions_gt'].iloc[-1], self.df['material_use_gt'].iloc[-1], 
                   self.df['gdp_growth_percent'].iloc[-1], color='red', s=100, label='2024')
        ax8.set_xlabel('CO2 (GT/yr)')
        ax8.set_ylabel('Materials (GT/yr)')
        ax8.set_zlabel('Growth (%/yr)')
        ax8.set_title('Full Historical Trajectory')
        ax8.legend()
        
        # 5. Equation fits
        co2 = self.df['co2_emissions_gt'].values
        materials = self.df['material_use_gt'].values
        growth = self.df['gdp_growth_percent'].values
        
        ax9 = plt.subplot(3, 4, 9)
        predicted_dco2 = params['sigma'] * (materials - co2)
        ax9.scatter(self.df['dCO2_dt'], predicted_dco2, alpha=0.6)
        ax9.plot([self.df['dCO2_dt'].min(), self.df['dCO2_dt'].max()], 
                [self.df['dCO2_dt'].min(), self.df['dCO2_dt'].max()], 'r--')
        ax9.set_xlabel('Observed dCO2/dt')
        ax9.set_ylabel('Predicted dCO2/dt')
        ax9.set_title(f'Equation 1 Fit (σ={params["sigma"]:.4f})')
        ax9.grid(True)
        
        ax10 = plt.subplot(3, 4, 10)
        predicted_dmaterials = co2 * (params['rho'] - growth) - materials
        ax10.scatter(self.df['dMaterials_dt'], predicted_dmaterials, alpha=0.6)
        ax10.plot([self.df['dMaterials_dt'].min(), self.df['dMaterials_dt'].max()], 
                 [self.df['dMaterials_dt'].min(), self.df['dMaterials_dt'].max()], 'r--')
        ax10.set_xlabel('Observed dMaterials/dt')
        ax10.set_ylabel('Predicted dMaterials/dt')
        ax10.set_title(f'Equation 2 Fit (ρ={params["rho"]:.2f})')
        ax10.grid(True)
        
        # 6. Parameter evolution over time
        ax11 = plt.subplot(3, 4, 11)
        # Calculate rolling window parameter estimates
        window = 10
        rolling_sigma = []
        rolling_years = []
        for i in range(window, len(self.df)):
            subset = self.df.iloc[i-window:i]
            if len(subset) >= window:
                mat_co2_diff = subset['material_use_gt'] - subset['co2_emissions_gt']
                if np.any(np.abs(mat_co2_diff) > 0.1):
                    mask = np.abs(mat_co2_diff) > 0.1
                    sigma_est = np.mean(subset['dCO2_dt'].iloc[mask] / mat_co2_diff.iloc[mask])
                    rolling_sigma.append(sigma_est)
                    rolling_years.append(subset['year'].iloc[-1])
        
        ax11.plot(rolling_years, rolling_sigma, 'b-', linewidth=2)
        ax11.set_xlabel('Year')
        ax11.set_ylabel('σ estimate')
        ax11.set_title('Parameter Evolution (10-yr window)')
        ax11.grid(True)
        
        # 7. Data quality indicators
        ax12 = plt.subplot(3, 4, 12)
        quality_counts = self.df['data_quality'].value_counts()
        ax12.pie(quality_counts.values, labels=quality_counts.index, autopct='%1.1f%%')
        ax12.set_title('Data Quality Distribution')
        
        # Add parameter summary
        param_text = (f'Empirically Derived Parameters (1970-2024):\\n'
                     f'σ = {params["sigma"]:.4f} ± {params["sigma_std"]:.4f}\\n'
                     f'ρ = {params["rho"]:.2f} ± {params["rho_std"]:.2f}\\n'
                     f'α = {params["alpha"]:.6f}\\n'
                     f'β = {params["beta"]:.3f}\\n'
                     f'Dataset: {len(self.df)} annual observations')
        plt.figtext(0.02, 0.02, param_text, fontsize=10, family='monospace')
        
        plt.tight_layout()
        plt.savefig('comprehensive_empirical_analysis_1970_2024.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def run_complete_analysis(self):
        """Run the complete empirical analysis"""
        print("\\n" + "="*60)
        print("COMPREHENSIVE EMPIRICAL ANALYSIS (1970-2024)")
        print("="*60)
        
        # Analyze Lorenz relationships
        params = self.analyze_lorenz_relationships()
        
        # Create comprehensive plots
        fig = self.plot_comprehensive_analysis(params)
        
        # Summary
        print("\\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Dataset: {len(self.df)} annual observations ({self.df['year'].min()}-{self.df['year'].max()})")
        print(f"Empirically derived parameters:")
        print(f"  σ = {params['sigma']:.4f} ± {params['sigma_std']:.4f} (emissions response)")
        print(f"  ρ = {params['rho']:.2f} ± {params['rho_std']:.2f} (critical growth threshold)")
        print(f"  α = {params['alpha']:.6f} (growth-emissions-materials coupling)")
        print(f"  β = {params['beta']:.3f} (growth damping)")
        print("\\nNext steps: Use these parameters in attractor analysis to explore dynamics")
        
        return params, fig


if __name__ == "__main__":
    # Run the comprehensive analysis
    analyzer = EnhancedEmpiricalAnalysis()
    params, fig = analyzer.run_complete_analysis()
