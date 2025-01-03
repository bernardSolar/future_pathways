import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


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

        # Economic factors
        base_cost_difference = (fossil_cost - renewable_cost + policy_incentive) / fossil_cost

        # Social influence from neighbors
        neighbor_adoption_rate = sum(1 for n in self.neighbors if n.has_renewables) / max(len(self.neighbors), 1)
        social_influence = 0.3 * neighbor_adoption_rate

        # Environmental factor with regional climate impacts
        local_temp_impact = global_temperature * (1 + 0.2 * abs(self.location[1]) / 90)  # Higher impact near poles
        environmental_factor = self.environmental_awareness * local_temp_impact

        # Combined decision factor
        adoption_probability = 0.1 * (base_cost_difference + social_influence + environmental_factor)

        # Wealth constraint with financing option
        annual_payment = renewable_cost / 10  # 10-year financing
        if self.wealth < renewable_cost and self.wealth < annual_payment * 2:
            adoption_probability *= 0.1

        # Make adoption decision
        if np.random.random() < max(0, min(1, adoption_probability)):
            self.has_renewables = True
            self.energy_cost = renewable_cost / 10  # Annual payment
            self.annual_emissions *= 0.1  # 90% reduction in emissions
            return True
        return False


class ClimateModel:
    def __init__(self, n_households, n_firms):
        self.agents = []
        self.temperature = 1.0
        self.year = 2024
        self.cumulative_emissions = 0
        self.carbon_price = 0

        # Define city centers
        city_centers = [(30, 30), (-30, 30), (0, -30)]

        # Initialize agents with spatial distribution
        for i in range(n_households):
            # Randomly select a city center
            city_center = city_centers[np.random.randint(0, len(city_centers))]
            # Add random noise to create clustering
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

        # Set up neighbor networks
        self._establish_neighbor_networks()

    def _establish_neighbor_networks(self):
        # Create neighbor networks based on spatial proximity
        for agent in self.agents:
            distances = []
            for other in self.agents:
                if other != agent:
                    dist = np.sqrt(
                        (agent.location[0] - other.location[0]) ** 2 +
                        (agent.location[1] - other.location[1]) ** 2
                    )
                    distances.append((dist, other))
            # Connect to 10 nearest neighbors
            agent.neighbors = [x[1] for x in sorted(distances)[:10]]

    def calculate_carbon_price(self):
        # Carbon price increases with temperature and cumulative emissions
        base_price = 30  # Starting carbon price
        temp_multiplier = max(1, self.temperature ** 2)
        emission_multiplier = min(2, self.cumulative_emissions / 1e6)
        self.carbon_price = base_price * temp_multiplier * emission_multiplier

    def step(self, renewable_cost, fossil_cost):
        # Update carbon price
        self.calculate_carbon_price()
        fossil_cost += self.carbon_price

        # Calculate policy incentive based on temperature
        policy_incentive = max(0, (self.temperature - 1.5) * 20)

        new_adoptions = 0
        total_emissions = 0

        # Update each agent
        for agent in self.agents:
            if agent.decide_adoption(renewable_cost, fossil_cost, self.temperature, policy_incentive):
                new_adoptions += 1
            total_emissions += agent.annual_emissions

        # Update global state
        self.cumulative_emissions += total_emissions
        adoption_rate = sum(1 for a in self.agents if a.has_renewables) / len(self.agents)

        # More sophisticated temperature model based on cumulative emissions
        self.temperature = 1.0 + 0.0000015 * self.cumulative_emissions

        self.year += 1

        return new_adoptions, adoption_rate, self.temperature, total_emissions


def run_enhanced_simulation(years=30):
    model = ClimateModel(n_households=1000, n_firms=100)

    # Initialize tracking variables
    temperatures = [model.temperature]
    adoption_rates = [0]
    emissions = [0]
    carbon_prices = [model.carbon_price]
    years = list(range(model.year, model.year + years))

    # Enhanced cost model
    base_renewable_cost = 100
    fossil_cost = 80

    for year in range(len(years) - 1):
        # More sophisticated learning curve
        current_adoption = sum(1 for a in model.agents if a.has_renewables)
        learning_rate = 0.15  # 15% cost reduction for each doubling
        renewable_cost = base_renewable_cost * (2 ** (np.log2(max(current_adoption + 1, 1)) * -learning_rate))

        results = model.step(renewable_cost, fossil_cost)
        temperatures.append(results[2])
        adoption_rates.append(results[1])
        emissions.append(results[3])
        carbon_prices.append(model.carbon_price)

    # Enhanced visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

    ax1.plot(years, temperatures)
    ax1.set_ylabel('Temperature Above Pre-industrial (°C)')
    ax1.set_title('Global Temperature Change')

    ax2.plot(years, adoption_rates)
    ax2.set_ylabel('Renewable Energy Adoption Rate')
    ax2.set_title('Technology Adoption')

    ax3.plot(years, emissions)
    ax3.set_ylabel('Annual Emissions (tonnes CO2)')
    ax3.set_xlabel('Year')
    ax3.set_title('Emissions Trajectory')

    ax4.plot(years, carbon_prices)
    ax4.set_ylabel('Carbon Price ($)')
    ax4.set_xlabel('Year')
    ax4.set_title('Carbon Price Evolution')

    plt.tight_layout()
    plt.show()


# Run the enhanced simulation
run_enhanced_simulation()