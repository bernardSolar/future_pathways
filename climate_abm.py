import numpy as np
import matplotlib.pyplot as plt


class Agent:
    def __init__(self, id, type, wealth, environmental_awareness):
        self.id = id
        self.type = type  # 'household' or 'firm'
        self.wealth = wealth
        self.environmental_awareness = environmental_awareness
        self.has_renewables = False
        self.energy_cost = 0

    def decide_adoption(self, renewable_cost, fossil_cost, global_temperature):
        # Economic factor: cost difference between renewable and fossil
        economic_factor = (fossil_cost - renewable_cost) / fossil_cost

        # Environmental factor: increases with temperature rise
        environmental_factor = self.environmental_awareness * (global_temperature - 1)

        # Combined decision factor
        adoption_probability = 0.1 * (economic_factor + environmental_factor)

        # Wealth constraint
        if self.wealth < renewable_cost:
            adoption_probability = 0

        # Make adoption decision
        if not self.has_renewables and np.random.random() < adoption_probability:
            self.has_renewables = True
            self.energy_cost = renewable_cost
            return True
        return False


class ClimateModel:
    def __init__(self, n_households, n_firms):
        self.agents = []
        self.temperature = 1.0  # Starting at 1°C above pre-industrial
        self.year = 2024

        # Initialize agents
        for i in range(n_households):
            wealth = np.random.lognormal(mean=11, sigma=1)  # Random wealth distribution
            awareness = np.random.beta(2, 5)  # Random environmental awareness
            self.agents.append(Agent(i, 'household', wealth, awareness))

        for i in range(n_firms):
            wealth = np.random.lognormal(mean=13, sigma=1.5)  # Firms have more wealth
            awareness = np.random.beta(2, 5)
            self.agents.append(Agent(i + n_households, 'firm', wealth, awareness))

    def step(self, renewable_cost, fossil_cost):
        # Count adoptions in this step
        new_adoptions = 0

        # Update each agent
        for agent in self.agents:
            if agent.decide_adoption(renewable_cost, fossil_cost, self.temperature):
                new_adoptions += 1

        # Update global temperature based on adoption rate
        adoption_rate = sum(1 for a in self.agents if a.has_renewables) / len(self.agents)
        self.temperature += 0.03 * (1 - adoption_rate)  # Simplified climate dynamics
        self.year += 1

        return new_adoptions, adoption_rate, self.temperature


# Run simulation
def run_simulation(years=30):
    model = ClimateModel(n_households=1000, n_firms=100)

    # Initialize tracking variables
    temperatures = [model.temperature]
    adoption_rates = [0]
    years = list(range(model.year, model.year + years))

    # Renewable costs decline over time (learning curve)
    base_renewable_cost = 100
    fossil_cost = 80

    for year in range(len(years) - 1):
        renewable_cost = base_renewable_cost * (0.95 ** year)  # 5% cost reduction per year
        new_adoptions, adoption_rate, temp = model.step(renewable_cost, fossil_cost)

        temperatures.append(temp)
        adoption_rates.append(adoption_rate)

    # Plot results
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.plot(years, temperatures)
    ax1.set_ylabel('Temperature Above Pre-industrial (°C)')
    ax1.set_title('Global Temperature Change')

    ax2.plot(years, adoption_rates)
    ax2.set_ylabel('Renewable Energy Adoption Rate')
    ax2.set_xlabel('Year')

    plt.tight_layout()
    plt.show()


# Run the simulation
run_simulation()