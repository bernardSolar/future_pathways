import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


class CarbonRemovalComparison:
    def __init__(self):
        # Natural solution properties
        self.natural_solutions = {
            'Marine': {
                'potential': 2.0,  # GT CO2/year
                'material_intensity': 0.1,  # GT material/GT CO2
                'energy_intensity': 0.15,  # MWh/tCO2 (150 TWh/GT)
                'growth_rate': 0.15,
                'scaling_limit': 5.0  # GT CO2/year
            },
            'Mineral': {
                'potential': 4.0,
                'material_intensity': 0.3,
                'energy_intensity': 0.35,  # MWh/tCO2 (350 TWh/GT)
                'growth_rate': 0.10,
                'scaling_limit': 8.0
            },
            'Soil': {
                'potential': 3.0,
                'material_intensity': 0.05,
                'energy_intensity': 0.1,  # MWh/tCO2 (100 TWh/GT)
                'growth_rate': 0.12,
                'scaling_limit': 6.0
            }
        }

        # Technological solution properties (DAC)
        self.tech_solution = {
            'potential': 5.0,
            'material_intensity': 0.5,
            'energy_intensity': 2.0,  # MWh/tCO2 (2000 TWh/GT)
            'growth_rate': 0.20,
            'scaling_limit': 10.0
        }

    def calculate_removal_potential(self, t):
        """Calculate removal potential for each solution type over time"""
        results = {}

        # Natural solutions
        for name, props in self.natural_solutions.items():
            # S-curve growth with scaling limit
            growth = props['potential'] * (1 - np.exp(-props['growth_rate'] * t))
            limit_factor = 1 - growth / props['scaling_limit']
            results[name] = growth * limit_factor

        # Technological solution
        tech_growth = self.tech_solution['potential'] * \
                      (1 - np.exp(-self.tech_solution['growth_rate'] * t))
        tech_limit = 1 - tech_growth / self.tech_solution['scaling_limit']
        results['Technological'] = tech_growth * tech_limit

        return results

    def calculate_resource_demands(self, removals):
        """Calculate material and energy demands for each solution"""
        demands = {}

        # Natural solutions
        for name, props in self.natural_solutions.items():
            removal = removals[name]
            demands[name] = {
                'materials': removal * props['material_intensity'],
                'energy': removal * props['energy_intensity']
            }

        # Technological solution
        tech_removal = removals['Technological']
        demands['Technological'] = {
            'materials': tech_removal * self.tech_solution['material_intensity'],
            'energy': tech_removal * self.tech_solution['energy_intensity']
        }

        return demands

    def plot_comparison(self, t_span=50):
        """Plot comparison with realistic energy units"""
        t = np.linspace(0, t_span, 1000)

        # Calculate removals and demands over time
        removals_over_time = []
        material_demands = []
        energy_demands = {
            'Marine': [], 'Mineral': [], 'Soil': [], 'Technological': [], 'Total': []
        }

        for time in t:
            removals = self.calculate_removal_potential(time)
            demands = self.calculate_resource_demands(removals)

            removals_over_time.append(removals)

            # Convert GT materials to GT/year
            total_materials = sum(d['materials'] for d in demands.values())
            material_demands.append(total_materials)

            # Calculate energy in TWh/year for each solution
            for solution in ['Marine', 'Mineral', 'Soil', 'Technological']:
                if solution == 'Technological':
                    energy = removals['Technological'] * self.tech_solution['energy_intensity'] * 1000
                else:
                    energy = removals[solution] * self.natural_solutions[solution]['energy_intensity'] * 1000
                energy_demands[solution].append(energy)

            # Calculate total energy demand
            energy_demands['Total'].append(sum(
                energy_demands[s][-1] for s in ['Marine', 'Mineral', 'Soil', 'Technological']
            ))

        # Create plots
        fig = plt.figure(figsize=(15, 10))

        # Carbon removal potential
        ax1 = fig.add_subplot(221)
        for solution in ['Marine', 'Mineral', 'Soil', 'Technological']:
            values = [r[solution] for r in removals_over_time]
            ax1.plot(t, values, label=solution)
        ax1.set_ylabel('GT CO2/year')
        ax1.set_title('Carbon Removal Potential')
        ax1.legend()
        ax1.grid(True)

        # Cumulative removal
        ax2 = fig.add_subplot(222)
        cumulative = {s: np.cumsum([r[s] for r in removals_over_time]) / len(t) * t_span
                      for s in ['Marine', 'Mineral', 'Soil', 'Technological']}
        for solution, values in cumulative.items():
            ax2.plot(t, values, label=solution)
        ax2.set_ylabel('GT CO2 (cumulative)')
        ax2.set_title('Cumulative Carbon Removal')
        ax2.legend()
        ax2.grid(True)

        # Material demand
        ax3 = fig.add_subplot(223)
        ax3.plot(t, material_demands, 'b-', label='Material Demand')
        ax3.set_ylabel('GT materials/year')
        ax3.set_xlabel('Years from 2024')
        ax3.set_title('Total Material Demand')
        ax3.grid(True)

        # Energy demand
        ax4 = fig.add_subplot(224)
        for solution in ['Marine', 'Mineral', 'Soil', 'Technological']:
            ax4.plot(t, energy_demands[solution], label=solution)
        ax4.plot(t, energy_demands['Total'], 'k--', label='Total')
        ax4.set_ylabel('TWh/year')
        ax4.set_xlabel('Years from 2024')
        ax4.set_title('Energy Demand by Solution')
        ax4.legend()
        ax4.grid(True)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    model = CarbonRemovalComparison()
    model.plot_comparison()