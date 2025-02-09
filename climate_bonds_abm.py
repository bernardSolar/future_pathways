import numpy as np
import matplotlib.pyplot as plt

# Parameters
initial_bonds = 1_000_000  # Bonds issued
coupon_rate = 0.07         # Annual interest rate
bond_duration = 10         # Years
renewable_cost_per_mw = 1_000_000  # Cost per MW of renewable capacity
annual_savings_per_mw = 200_000    # Annual savings per MW deployed

# Initial conditions
renewable_capacity = 0
total_savings = 0
annual_revenue = []
capacity_over_time = []
savings_over_time = []
repayments_over_time = []

# Simulate over bond duration
for year in range(1, bond_duration + 1):
    # Deploy renewable capacity
    deployed_capacity = initial_bonds / renewable_cost_per_mw
    renewable_capacity += deployed_capacity

    # Calculate annual savings
    annual_savings = renewable_capacity * annual_savings_per_mw
    total_savings += annual_savings

    # Calculate bond repayment
    bond_repayment = initial_bonds * coupon_rate
    net_revenue = annual_savings - bond_repayment

    # Store results
    capacity_over_time.append(renewable_capacity)
    savings_over_time.append(annual_savings)
    repayments_over_time.append(bond_repayment)
    annual_revenue.append(net_revenue)

# Plot the results
plt.figure(figsize=(12, 6))

# Renewable capacity over time
plt.subplot(2, 2, 1)
plt.plot(range(1, bond_duration + 1), capacity_over_time, marker='o')
plt.title('Renewable Capacity Over Time')
plt.xlabel('Year')
plt.ylabel('Capacity (MW)')
plt.grid(True)

# Annual savings over time
plt.subplot(2, 2, 2)
plt.plot(range(1, bond_duration + 1), savings_over_time, marker='o', color='green')
plt.title('Annual Savings Over Time')
plt.xlabel('Year')
plt.ylabel('Savings ($)')
plt.grid(True)

# Bond repayments over time
plt.subplot(2, 2, 3)
plt.plot(range(1, bond_duration + 1), repayments_over_time, marker='o', color='red')
plt.title('Annual Bond Repayments Over Time')
plt.xlabel('Year')
plt.ylabel('Repayments ($)')
plt.grid(True)

# Net revenue over time
plt.subplot(2, 2, 4)
plt.plot(range(1, bond_duration + 1), annual_revenue, marker='o', color='purple')
plt.title('Net Revenue Over Time')
plt.xlabel('Year')
plt.ylabel('Net Revenue ($)')
plt.grid(True)

plt.tight_layout()
plt.show()