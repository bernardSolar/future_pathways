import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import CheckButtons

# Create figure and 3D axes
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Current position - calibrated to real values
# x: 50 GT CO2e/yr
# y: 2.5% growth (middle of 2-3% range)
# z: 106 billion tonnes/yr (2024 material use)
current_pos = np.array([50, 2.5, 106])  # CO2e, Growth, Materials

# Plot current position
ax.scatter([current_pos[0]], [current_pos[2]], [current_pos[1]],
          color='red', s=100, label='Current Position')

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