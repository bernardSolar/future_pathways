import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class RealisticTransitionAttractor:
    def __init__(self, sigma=1.0, rho=4.0, beta=0.7):
        self.sigma = sigma  # Speed of emissions response
        self.rho = rho  # Critical growth threshold
        self.beta = beta  # Growth damping factor

        # Current real-world values for scaling
        self.emissions_scale = 50.0  # GT CO2e/year
        self.materials_scale = 106.0  # GT/year
        self.growth_scale = 2.5  # %/year

    def system_eqs(self, state, t):
        """Define the system of equations with realistic scaling"""
        x, y, z = state  # x: emissions, y: material use, z: growth

        # Scale variables to normalized form
        x_norm = x / self.emissions_scale
        y_norm = y / self.materials_scale
        z_norm = z / self.growth_scale

        # Core dynamics
        dx = self.sigma * (y_norm - x_norm)
        dy = x_norm * (self.rho - z_norm) - y_norm
        dz = x_norm * y_norm - self.beta * z_norm

        # Scale back to real units
        dx *= self.emissions_scale
        dy *= self.materials_scale
        dz *= self.growth_scale

        return [dx, dy, dz]

    def generate_trajectory(self, initial_state=None, t_span=50, n_points=5000):
        """Generate a trajectory through the phase space"""
        if initial_state is None:
            initial_state = [
                50.0,  # Current emissions GT CO2e/year
                106.0,  # Current material use GT/year
                2.5  # Current growth rate %/year
            ]

        t = np.linspace(0, t_span, n_points)
        trajectory = odeint(self.system_eqs, initial_state, t)

        return trajectory, t

    def plot_attractor(self, trajectory, t):
        """Plot the attractor in 3D space with realistic units"""
        fig = plt.figure(figsize=(15, 10))

        # 3D trajectory plot
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2],
                 lw=0.5, alpha=0.8)

        # Label axes with units
        ax1.set_xlabel('CO2e Emissions (GT/yr)')
        ax1.set_ylabel('Material Use (GT/yr)')
        ax1.set_zlabel('Growth (%/yr)')
        ax1.set_title('Energy Transition Attractor')

        # Add transition zones for reference
        self._add_transition_zones(ax1)

        # Time series plots
        ax2 = fig.add_subplot(322)
        ax2.plot(t, trajectory[:, 0])
        ax2.set_ylabel('CO2e Emissions (GT/yr)')

        ax3 = fig.add_subplot(324)
        ax3.plot(t, trajectory[:, 1])
        ax3.set_ylabel('Material Use (GT/yr)')

        ax4 = fig.add_subplot(326)
        ax4.plot(t, trajectory[:, 2])
        ax4.set_ylabel('Growth (%/yr)')
        ax4.set_xlabel('Time (years)')

        # Add parameter information
        params_text = (f'Parameters:\n'
                       f'σ={self.sigma:.2f} (emissions response)\n'
                       f'ρ={self.rho:.2f} (growth threshold)\n'
                       f'β={self.beta:.2f} (growth damping)')
        plt.figtext(0.02, 0.02, params_text)

        plt.tight_layout()
        plt.show()

    def _add_transition_zones(self, ax):
        """Add reference planes for transition zones"""
        x = np.linspace(-20, 60, 10)
        y = np.linspace(0, 200, 10)
        X, Y = np.meshgrid(x, y)

        # Energy Transition Zone (2.5% to 5%)
        Z = np.full_like(X, 4)
        ax.plot_surface(X, Y, Z, alpha=0.1, color='green')
        Z = np.full_like(X, 2.5)
        ax.plot_surface(X, Y, Z, alpha=0.1, color='green')

        # Intermediate Zone (0% to 2.5%)
        Z = np.full_like(X, 2.5)
        ax.plot_surface(X, Y, Z, alpha=0.1, color='orange')
        Z = np.full_like(X, 0)
        ax.plot_surface(X, Y, Z, alpha=0.1, color='orange')

        # Descent Zone (-5% to 0%)
        Z = np.full_like(X, 0)
        ax.plot_surface(X, Y, Z, alpha=0.1, color='red')
        Z = np.full_like(X, -5)
        ax.plot_surface(X, Y, Z, alpha=0.1, color='red')


# Create and display with realistic parameters
if __name__ == "__main__":
    # Create system with estimated realistic parameters
    system = RealisticTransitionAttractor()

    # Generate trajectory
    trajectory, t = system.generate_trajectory()

    # Plot the attractor with transition zones
    system.plot_attractor(trajectory, t)