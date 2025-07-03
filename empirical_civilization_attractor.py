import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class EmpiricalCivilizationAttractor:
    def __init__(self, sigma=0.021, rho=4.75, beta=0.7):
        """
        Initialize with empirically-derived parameters from historical data analysis
        
        sigma: Emissions response rate (how fast CO2 chases materials)
        rho: Critical growth threshold 
        beta: Growth damping factor (we'll experiment with this)
        """
        self.sigma = sigma  # Empirically derived: 0.021
        self.rho = rho      # Empirically derived: 4.75
        self.beta = beta    # This one didn't fit well empirically, so we'll experiment

        # Current real-world values for scaling (our 2024 starting point)
        self.emissions_scale = 50.0   # GT CO2e/year
        self.materials_scale = 106.0  # GT/year
        self.growth_scale = 2.5       # %/year

    def system_eqs(self, state, t):
        """
        Define the empirically-grounded system of equations
        """
        x, y, z = state  # x: emissions, y: material use, z: growth

        # Use empirically-derived equations in real units
        # Equation 1: dCO2/dt = σ(Materials - CO2) - very good empirical fit
        dx = self.sigma * (y - x)
        
        # Equation 2: dMaterials/dt = CO2*(ρ - Growth) - Materials - decent empirical fit
        dy = x * (self.rho - z) - y
        
        # Equation 3: dGrowth/dt = CO2*Materials*scale_factor - β*Growth 
        # (Experimenting with scaling since empirical fit was poor)
        scale_factor = 1e-4  # Scale down the CO2*Materials product
        dz = x * y * scale_factor - self.beta * z

        return [dx, dy, dz]

    def generate_trajectory(self, initial_state=None, t_span=50, n_points=5000):
        """Generate a trajectory through the phase space"""
        if initial_state is None:
            # Start from our current 2024 position
            initial_state = [
                50.0,   # Current CO2 emissions GT/year
                106.0,  # Current material use GT/year  
                2.5     # Current growth rate %/year
            ]

        t = np.linspace(0, t_span, n_points)
        trajectory = odeint(self.system_eqs, initial_state, t)

        return trajectory, t

    def plot_empirical_attractor(self, trajectory, t):
        """Plot the empirically-derived attractor with historical context"""
        fig = plt.figure(figsize=(16, 12))

        # 3D trajectory plot
        ax1 = fig.add_subplot(221, projection='3d')
        
        # Plot the trajectory with color gradient (blue->red over time)
        n_points = len(trajectory)
        colors = plt.cm.viridis(np.linspace(0, 1, n_points))
        
        for i in range(n_points-1):
            ax1.plot([trajectory[i, 0], trajectory[i+1, 0]], 
                    [trajectory[i, 1], trajectory[i+1, 1]], 
                    [trajectory[i, 2], trajectory[i+1, 2]], 
                    color=colors[i], alpha=0.7, linewidth=0.5)

        # Mark starting point
        ax1.scatter([trajectory[0, 0]], [trajectory[0, 1]], [trajectory[0, 2]], 
                   color='red', s=100, label='Start (2024)')
        
        # Mark end point
        ax1.scatter([trajectory[-1, 0]], [trajectory[-1, 1]], [trajectory[-1, 2]], 
                   color='blue', s=100, label=f'End ({t[-1]:.0f} years)')

        # Add historical data points for reference
        historical_years = [1995, 2000, 2005, 2010, 2015, 2020, 2024]
        historical_co2 = [23.0, 25.5, 30.0, 33.5, 36.5, 43.0, 50.0]
        historical_materials = [45.0, 54.0, 65.0, 78.0, 88.0, 98.0, 106.0]
        historical_growth = [3.3, 4.4, 3.9, 4.3, 2.9, -3.3, 2.5]
        
        ax1.scatter(historical_co2, historical_materials, historical_growth, 
                   color='black', marker='*', s=50, alpha=0.7, label='Historical (1995-2024)')

        ax1.set_xlabel('CO2e Emissions (GT/yr)')
        ax1.set_ylabel('Material Use (GT/yr)')
        ax1.set_zlabel('Growth (%/yr)')
        ax1.set_title('Empirically-Derived Civilization Attractor')
        ax1.legend()

        # Add transition zones for reference
        self._add_transition_zones(ax1)

        # Time series plots
        ax2 = fig.add_subplot(322)
        ax2.plot(t, trajectory[:, 0], 'b-', label='Predicted')
        ax2.axhline(y=50, color='red', linestyle='--', alpha=0.7, label='2024 Start')
        ax2.set_ylabel('CO2e Emissions (GT/yr)')
        ax2.set_title('CO2 Emissions Over Time')
        ax2.legend()
        ax2.grid(True)

        ax3 = fig.add_subplot(324)
        ax3.plot(t, trajectory[:, 1], 'g-', label='Predicted')
        ax3.axhline(y=106, color='red', linestyle='--', alpha=0.7, label='2024 Start')
        ax3.set_ylabel('Material Use (GT/yr)')
        ax3.set_title('Material Use Over Time')
        ax3.legend()
        ax3.grid(True)

        ax4 = fig.add_subplot(326)
        ax4.plot(t, trajectory[:, 2], 'r-', label='Predicted')
        ax4.axhline(y=2.5, color='red', linestyle='--', alpha=0.7, label='2024 Start')
        ax4.axhline(y=self.rho, color='orange', linestyle=':', alpha=0.7, label=f'ρ threshold ({self.rho}%)')
        ax4.set_ylabel('Growth (%/yr)')
        ax4.set_xlabel('Time (years)')
        ax4.set_title('Economic Growth Over Time')
        ax4.legend()
        ax4.grid(True)

        # Phase space plots
        ax5 = fig.add_subplot(223)
        ax5.plot(trajectory[:, 0], trajectory[:, 1], 'purple', alpha=0.7)
        ax5.scatter(historical_co2, historical_materials, color='black', marker='*', s=30)
        ax5.set_xlabel('CO2e Emissions (GT/yr)')
        ax5.set_ylabel('Material Use (GT/yr)')
        ax5.set_title('CO2 vs Materials Phase Space')
        ax5.grid(True)

        # Parameter information
        params_text = (f'Empirical Parameters:\n'
                       f'σ = {self.sigma:.4f} (emissions response)\n'
                       f'ρ = {self.rho:.2f} (growth threshold)\n'
                       f'β = {self.beta:.2f} (growth damping)')
        plt.figtext(0.02, 0.02, params_text, fontsize=9, family='monospace')

        plt.tight_layout()
        plt.show()

    def _add_transition_zones(self, ax):
        """Add reference planes for transition zones"""
        x = np.linspace(-20, 100, 10)
        y = np.linspace(0, 200, 10)
        X, Y = np.meshgrid(x, y)

        # Energy Transition Zone (2.5% to 5%)
        Z_high = np.full_like(X, 5)
        Z_low = np.full_like(X, 2.5)
        ax.plot_surface(X, Y, Z_high, alpha=0.05, color='green')
        ax.plot_surface(X, Y, Z_low, alpha=0.05, color='green')

        # Intermediate Zone (0% to 2.5%)
        Z_high = np.full_like(X, 2.5)
        Z_low = np.full_like(X, 0)
        ax.plot_surface(X, Y, Z_high, alpha=0.05, color='orange')
        ax.plot_surface(X, Y, Z_low, alpha=0.05, color='orange')

        # Descent Zone (-5% to 0%)
        Z_high = np.full_like(X, 0)
        Z_low = np.full_like(X, -5)
        ax.plot_surface(X, Y, Z_high, alpha=0.05, color='red')
        ax.plot_surface(X, Y, Z_low, alpha=0.05, color='red')

    def experiment_with_parameters(self, param_ranges):
        """
        Experiment with different parameter values to find interesting dynamics
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 10), subplot_kw={'projection': '3d'})
        axes = axes.flatten()
        
        for i, (name, sigma, rho, beta) in enumerate(param_ranges):
            # Create temporary system with new parameters
            temp_system = EmpiricalCivilizationAttractor(sigma=sigma, rho=rho, beta=beta)
            trajectory, t = temp_system.generate_trajectory(t_span=30, n_points=3000)
            
            ax = axes[i]
            ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], 
                   lw=0.5, alpha=0.8)
            ax.scatter([50], [106], [2.5], color='red', s=50, label='Start')
            ax.set_xlabel('CO2 (GT/yr)')
            ax.set_ylabel('Materials (GT/yr)')
            ax.set_zlabel('Growth (%/yr)')
            ax.set_title(f'{name}\nσ={sigma}, ρ={rho}, β={beta}')
            
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # Create system with empirically-derived parameters
    print("Creating Empirical Civilization Attractor...")
    print("Using parameters derived from 1995-2024 data analysis:")
    print("σ = 0.021 (emissions response rate)")
    print("ρ = 4.75 (critical growth threshold)")
    print("β = 0.7 (experimental growth damping)")
    
    system = EmpiricalCivilizationAttractor()

    # Generate trajectory starting from current 2024 position
    print("\nGenerating trajectory from 2024 starting point...")
    trajectory, t = system.generate_trajectory(t_span=50, n_points=5000)

    # Plot the empirically-derived attractor
    print("Plotting results...")
    system.plot_empirical_attractor(trajectory, t)
    
    # Experiment with different beta values since that parameter didn't fit well empirically
    print("\nExperimenting with different parameter combinations...")
    param_experiments = [
        ("Empirical Base", 0.021, 4.75, 0.7),
        ("Higher Damping", 0.021, 4.75, 2.0),
        ("Lower Threshold", 0.021, 3.0, 0.7),  
        ("Faster Response", 0.05, 4.75, 0.7)
    ]
    
    system.experiment_with_parameters(param_experiments)
