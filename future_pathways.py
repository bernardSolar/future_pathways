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
current_pos = np.array([0.8, 0.6, 0.7])  # CO2e, Growth, Materials

# Business As Usual path
bau_x = 0.8 + 0.2 * t
bau_y = 0.6 - 0.8 * t
bau_z = 0.7 + 0.3 * t

# Green Growth path
gg_x = 0.8 - 1.2 * t
gg_y = 0.6 + 0.2 * t
gg_z = 0.7 + 0.1 * (1-np.exp(-3*t))

# Managed Descent path
md_x = 0.8 - 0.9 * t
md_y = 0.6 - 0.8 * t
md_z = 0.7 - 0.4 * t

# Star Trek path
st_x = 0.8 - 1.4 * t
st_y = 0.6 + 0.3 * t
st_z = 0.7 + 0.2 * np.sin(2*np.pi*t) - 0.5 * t

# Collapse path
col_x = 0.8 + 0.1 * t
col_y = 0.6 - 1.1 * t
col_z = 0.7 - 0.6 * t

# Plot paths
paths = {
    'Business As Usual': (bau_x, bau_y, bau_z, 'red'),
    'Green Growth': (gg_x, gg_y, gg_z, 'green'),
    'Managed Descent': (md_x, md_y, md_z, 'blue'),
    'Star Trek': (st_x, st_y, st_z, 'purple'),
    'Collapse': (col_x, col_y, col_z, 'brown')
}

lines = {}
for name, (x, y, z, color) in paths.items():
    lines[name] = ax.plot(x, y, z, label=name, color=color, linewidth=2)[0]

# Plot current position
ax.scatter([current_pos[0]], [current_pos[1]], [current_pos[2]], 
          color='red', s=100, label='Current Position')

# Set labels and title
ax.set_xlabel('CO2e Emissions')
ax.set_ylabel('Growth')
ax.set_zlabel('Material Use')
ax.set_title('Future Pathways: Interactive 3D Visualization')

# Set axis limits
ax.set_xlim([-1, 1.5])
ax.set_ylim([-1, 1])
ax.set_zlim([0, 1.5])

# Add grid
ax.grid(True)

# Add legend
ax.legend(loc='upper right')

# Create check buttons for toggling paths
rax = plt.axes([0.02, 0.4, 0.12, 0.2])
check = CheckButtons(rax, list(paths.keys()), [True]*len(paths))

def func(label):
    lines[label].set_visible(not lines[label].get_visible())
    plt.draw()

check.on_clicked(func)

# Add text for controls
fig.text(0.02, 0.95, 'Controls:', fontsize=10)
fig.text(0.02, 0.92, 'Left mouse: Rotate', fontsize=8)
fig.text(0.02, 0.89, 'Right mouse: Zoom', fontsize=8)
fig.text(0.02, 0.86, 'Middle mouse: Pan', fontsize=8)

plt.show()
