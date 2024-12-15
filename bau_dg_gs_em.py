import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import CheckButtons

# Create figure and 3D axes
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Generate paths data
t = np.linspace(0, 1, 100)

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

# Eco-modernist path - ensuring it starts at current position
em_x = current_pos[0] - 65 * t - 5 * t**2  # Start at 50 GT/yr
em_y = current_pos[1] + 2 * t**2  # Start at 2.5% growth
em_z = current_pos[2] + 40 * t * np.exp(-3*t) - 40 * t  # Start at 106 billion tonnes

# Verify all paths start at current position
print(f"Start positions:")
print(f"BAU: ({bau_x[0]:.1f}, {bau_y[0]:.1f}, {bau_z[0]:.1f})")
print(f"Degrowth: ({dg_x[0]:.1f}, {dg_y[0]:.1f}, {dg_z[0]:.1f})")
print(f"Great Simplification: ({gs_x[0]:.1f}, {gs_y[0]:.1f}, {gs_z[0]:.1f})")
print(f"Eco-modernist: ({em_x[0]:.1f}, {em_y[0]:.1f}, {em_z[0]:.1f})")

# Plot paths
ax.plot([current_pos[0]], [current_pos[2]], [current_pos[1]], 'ro', label='Current Position')
ax.plot(bau_x, bau_z, bau_y, 'r-', label='Business As Usual', linewidth=2)
ax.plot(dg_x, dg_z, dg_y, 'b-', label='Degrowth (Hickel)', linewidth=2)
ax.plot(gs_x, gs_z, gs_y, 'g-', label='Great Simplification (Hagens)', linewidth=2)
ax.plot(em_x, em_z, em_y, 'c-', label='Eco-modernist Utopia', linewidth=2)

# Set labels and title
ax.set_xlabel('CO2e Emissions (GT/yr)')
ax.set_zlabel('Growth (%/yr)')
ax.set_ylabel('Material Use (billion tonnes/yr)')
ax.set_title('Future Pathways: Interactive 3D Visualization')

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