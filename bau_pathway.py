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
# CO2e: Increase from 50 to 60 GT/yr
# Growth: Decline from 2.5% to -1%
# Materials: Increase from 106 to 160 billion tonnes/yr
bau_x = 50 + 10 * t  # CO2e increases
bau_y = 2.5 - 3.5 * t  # Growth decreases
bau_z = 106 + 54 * t  # Materials increase

# Plot BAU path
ax.plot([bau_x[0]], [bau_z[0]], [bau_y[0]], 'ro', label='Current Position')
ax.plot(bau_x, bau_z, bau_y, 'r-', label='Business As Usual', linewidth=2)

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