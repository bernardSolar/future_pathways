import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import CheckButtons

# Create figure and 3D axes
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Generate paths data - now using 36 points for 36 years (2024-2060)
years = np.linspace(2024, 2060, 37)
t = np.linspace(0, 1, 37)

# Current position
current_pos = np.array([50, 2.5, 106])  # CO2e, Growth, Materials

# Business As Usual path
bau_x = 50 + 10 * t  # CO2e increases
bau_y = 2.5 - 3.5 * t  # Growth decreases
bau_z = 106 + 54 * t  # Materials increase

# Degrowth path (Hickel)
dg_x = 50 - 60 * t  # Rapid emissions reduction
dg_y = 2.5 - 4 * t + 1.5 * t**2  # Controlled descent then stabilization
dg_z = 106 - 56 * t  # Material reduction

# Great Simplification path (Hagens)
gs_x = 50 * np.exp(-2 * t)  # Natural emissions decline with energy descent
gs_y = 2.5 - 3 * t - 1.5 * t**2  # Steepening descent as constraints bind
gs_z = 106 * np.exp(-1.5 * t)  # Material use decline following energy

# Eco-modernist path
em_x = current_pos[0] - 65 * t - 5 * t**2  # Start at 50 GT/yr
em_y = current_pos[1] + 2 * t**2  # Start at 2.5% growth
em_z = current_pos[2] + 40 * t * np.exp(-3*t) - 40 * t  # Start at 106 billion tonnes

# Plot paths with year markers
def plot_path_with_years(x, y, z, color, label):
    ax.plot(x, z, y, color=color, label=label, linewidth=2)
    # Add year markers every 10 years
    for i in range(0, len(years), 10):
        if i > 0:  # Skip 2024 as it's marked by the red dot
            ax.scatter(x[i], z[i], y[i], color=color, s=30)
            ax.text(x[i], z[i], y[i], f'{int(years[i])}', color=color)

# Plot current position
ax.scatter([current_pos[0]], [current_pos[2]], [current_pos[1]],
          color='red', s=100, label='Current Position (2024)')

# Plot paths with year markers
plot_path_with_years(bau_x, bau_y, bau_z, 'red', 'Business As Usual')
plot_path_with_years(dg_x, dg_y, dg_z, 'blue', 'Degrowth (Hickel)')
plot_path_with_years(gs_x, gs_y, gs_z, 'green', 'Great Simplification (Hagens)')
plot_path_with_years(em_x, em_y, em_z, 'cyan', 'Eco-modernist Utopia')

# Set labels and title
ax.set_xlabel('CO2e Emissions (GT/yr)')
ax.set_zlabel('Growth (%/yr)')
ax.set_ylabel('Material Use (billion tonnes/yr)')
ax.set_title('Future Pathways: Interactive 3D Visualization (2024-2060)')

# Set axis limits with calibrated scales
ax.set_xlim([-20, 60])     # CO2e: from -20 GT/yr to 60 GT/yr
ax.set_ylim([0, 200])      # Material use: 0 to 200 billion tonnes/yr
ax.set_zlim([-5, 5])       # Growth: -5% to +5% per year

# Important: Reverse the direction of x-axis ticks
ax.invert_xaxis()

# Set initial view angle
ax.view_init(elev=20, azim=45)

# Add grid
ax.grid(True)

# Add legend
ax.legend(loc='upper right')

# Adjust the aspect ratio to make the plot more readable
ax.set_box_aspect([2, 1, 1])

plt.show()