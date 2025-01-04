import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# Base Agent class
class Agent:
    def __init__(self, id, type, wealth, environmental_awareness, location):
        self.id = id
        self.type = type  # 'household' or 'firm'
        self.wealth = wealth
        self.environmental_awareness = environmental_awareness
        self.has_renewables = False
        self.energy_cost = 0
        self.location = location  # (x, y) coordinates
        self.neighbors = []
        self.annual_emissions = 20 if type == 'household' else 200  # tonnes CO2

    def decide_adoption(self, renewable_cost, fossil_cost, global_temperature, policy_incentive):
        if self.has_renewables:
            return False

        base_cost_difference = (fossil_cost - renewable_cost + policy_incentive) / fossil_cost

        neighbor_adoption_rate = sum(1 for n in self.neighbors if n.has_renewables) / max(len(self.neighbors), 1)
        social_influence = 0.3 * neighbor_adoption_rate

        local_temp_impact = global_temperature * (1 + 0.2 * abs(self.location[1]) / 90)
        environmental_factor = self.environmental_awareness * local_temp_impact

        adoption_probability = 0.1 * (base_cost_difference + social_influence + environmental_factor)

        annual_payment = renewable_cost / 10
        if self.wealth < renewable_cost and self.wealth < annual_payment * 2:
            adoption_probability *= 0.1

        if np.random.random() < max(0, min(1, adoption_probability)):
            self.has_renewables = True
            self.energy_cost = renewable_cost / 10
            self.annual_emissions *= 0.1
            return True
        return False


# Base ClimateModel class
class ClimateModel:
    def __init__(self, n_households, n_firms):
        self.agents = []
        self.temperature = 1.0
        self.year = 2024
        self.cumulative_emissions = 0
        self.carbon_price = 0

        city_centers = [(30, 30), (-30, 30), (0, -30)]

        for i in range(n_households):
            city_center = city_centers[np.random.randint(0, len(city_centers))]
            location = (
                city_center[0] + np.random.normal(0, 10),
                city_center[1] + np.random.normal(0, 10)
            )

            wealth = np.random.lognormal(mean=11, sigma=1)
            awareness = np.random.beta(2, 5)
            self.agents.append(Agent(i, 'household', wealth, awareness, location))

        for i in range(n_firms):
            location = (np.random.uniform(-90, 90), np.random.uniform(-90, 90))
            wealth = np.random.lognormal(mean=13, sigma=1.5)
            awareness = np.random.beta(2, 5)
            self.agents.append(Agent(i + n_households, 'firm', wealth, awareness, location))

        self._establish_neighbor_networks()

    def _establish_neighbor_networks(self):
        for agent in self.agents:
            distances = []
            for other in self.agents:
                if other != agent:
                    dist = np.sqrt(
                        (agent.location[0] - other.location[0]) ** 2 +
                        (agent.location[1] - other.location[1]) ** 2
                    )
                    distances.append((dist, other))
            agent.neighbors = [x[1] for x in sorted(distances)[:10]]

    def calculate_carbon_price(self):
        base_price = 30
        temp_multiplier = max(1, self.temperature ** 2)
        emission_multiplier = min(2, self.cumulative_emissions / 1e6)
        self.carbon_price = base_price * temp_multiplier * emission_multiplier

    def step(self, renewable_cost, fossil_cost):
        self.calculate_carbon_price()
        fossil_cost += self.carbon_price

        policy_incentive = max(0, (self.temperature - 1.5) * 20)

        new_adoptions = 0
        total_emissions = 0

        for agent in self.agents:
            if agent.decide_adoption(renewable_cost, fossil_cost, self.temperature, policy_incentive):
                new_adoptions += 1
            total_emissions += agent.annual_emissions

        self.cumulative_emissions += total_emissions
        adoption_rate = sum(1 for a in self.agents if a.has_renewables) / len(self.agents)

        self.temperature = 1.0 + 0.0000015 * self.cumulative_emissions

        self.year += 1

        return new_adoptions, adoption_rate, self.temperature, total_emissions


def run_monte_carlo_simulation(n_runs=100, years=30):
    """Run multiple simulations with parameter variations"""

    # Storage for results across all runs
    all_temperatures = []
    all_adoption_rates = []
    all_emissions = []
    all_carbon_prices = []

    # Parameter ranges for uncertainty (mean, std)
    param_distributions = {
        'learning_rate': (0.15, 0.03),  # Learning rate 15% ± 3%
        'environmental_awareness_alpha': (2, 0.4),  # Shape parameters for beta distribution
        'environmental_awareness_beta': (5, 1.0),
        'wealth_mean': (11, 1),  # Parameters for wealth lognormal
        'temperature_sensitivity': (0.0000015, 0.0000003),  # Temperature response to emissions
        'social_influence': (0.3, 0.06),  # Social influence factor
        'base_carbon_price': (30, 6)  # Starting carbon price
    }

    for run in range(n_runs):
        # Sample parameters from their distributions
        params = {
            'learning_rate': np.random.normal(
                param_distributions['learning_rate'][0],
                param_distributions['learning_rate'][1]
            ),
            'env_awareness_alpha': np.random.normal(
                param_distributions['environmental_awareness_alpha'][0],
                param_distributions['environmental_awareness_alpha'][1]
            ),
            'env_awareness_beta': np.random.normal(
                param_distributions['environmental_awareness_beta'][0],
                param_distributions['environmental_awareness_beta'][1]
            ),
            'wealth_mean': np.random.normal(
                param_distributions['wealth_mean'][0],
                param_distributions['wealth_mean'][1]
            ),
            'temp_sensitivity': np.random.normal(
                param_distributions['temperature_sensitivity'][0],
                param_distributions['temperature_sensitivity'][1]
            ),
            'social_influence': np.random.normal(
                param_distributions['social_influence'][0],
                param_distributions['social_influence'][1]
            ),
            'base_carbon_price': np.random.normal(
                param_distributions['base_carbon_price'][0],
                param_distributions['base_carbon_price'][1]
            )
        }

        # Run simulation
        model = ClimateModel(n_households=1000, n_firms=100)

        temperatures = [model.temperature]
        adoption_rates = [0]
        emissions = [0]
        carbon_prices = [model.carbon_price]

        base_renewable_cost = 100
        fossil_cost = 80

        for year in range(years):
            current_adoption = sum(1 for a in model.agents if a.has_renewables)
            learning_rate = params['learning_rate']
            renewable_cost = base_renewable_cost * (2 ** (np.log2(max(current_adoption + 1, 1)) * -learning_rate))

            results = model.step(renewable_cost, fossil_cost)
            temperatures.append(results[2])
            adoption_rates.append(results[1])
            emissions.append(results[3])
            carbon_prices.append(model.carbon_price)

        all_temperatures.append(temperatures)
        all_adoption_rates.append(adoption_rates)
        all_emissions.append(emissions)
        all_carbon_prices.append(carbon_prices)

    # Convert to numpy arrays for easier calculation
    all_temperatures = np.array(all_temperatures)
    all_adoption_rates = np.array(all_adoption_rates)
    all_emissions = np.array(all_emissions)
    all_carbon_prices = np.array(all_carbon_prices)

    # Calculate statistics
    temp_mean = np.mean(all_temperatures, axis=0)
    temp_std = np.std(all_temperatures, axis=0)

    adopt_mean = np.mean(all_adoption_rates, axis=0)
    adopt_std = np.std(all_adoption_rates, axis=0)

    emis_mean = np.mean(all_emissions, axis=0)
    emis_std = np.std(all_emissions, axis=0)

    price_mean = np.mean(all_carbon_prices, axis=0)
    price_std = np.std(all_carbon_prices, axis=0)

    # Plot results with uncertainty bands
    years_list = list(range(2024, 2024 + years + 1))

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

    # Temperature plot
    ax1.fill_between(years_list, temp_mean - 2 * temp_std, temp_mean + 2 * temp_std, alpha=0.2)
    ax1.plot(years_list, temp_mean)
    ax1.set_ylabel('Temperature Above Pre-industrial (°C)')
    ax1.set_title('Global Temperature Change')

    # Adoption plot
    ax2.fill_between(years_list,
                     np.clip(adopt_mean - 2 * adopt_std, 0, 1),
                     np.clip(adopt_mean + 2 * adopt_std, 0, 1),
                     alpha=0.2)
    ax2.plot(years_list, adopt_mean)
    ax2.set_ylabel('Renewable Energy Adoption Rate')
    ax2.set_title('Technology Adoption')

    # Emissions plot
    ax3.fill_between(years_list,
                     np.clip(emis_mean - 2 * emis_std, 0, None),
                     emis_mean + 2 * emis_std,
                     alpha=0.2)
    ax3.plot(years_list, emis_mean)
    ax3.set_ylabel('Annual Emissions (tonnes CO2)')
    ax3.set_xlabel('Year')
    ax3.set_title('Emissions Trajectory')

    # Carbon price plot
    ax4.fill_between(years_list,
                     np.clip(price_mean - 2 * price_std, 0, None),
                     price_mean + 2 * price_std,
                     alpha=0.2)
    ax4.plot(years_list, price_mean)
    ax4.set_ylabel('Carbon Price ($)')
    ax4.set_xlabel('Year')
    ax4.set_title('Carbon Price Evolution')

    plt.tight_layout()
    plt.show()

    return {
        'temperatures': all_temperatures,
        'adoption_rates': all_adoption_rates,
        'emissions': all_emissions,
        'carbon_prices': all_carbon_prices
    }


# Run the Monte Carlo simulation
results = run_monte_carlo_simulation(n_runs=100)