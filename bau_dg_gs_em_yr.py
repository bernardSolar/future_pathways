import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import CheckButtons

# Create figure with adjusted size
fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111, projection='3d')

# Generate paths data - using 37 points for 2024-2060
years = np.linspace(2024, 2060, 37)
t = np.linspace(0, 1, 37)

# Current position
current_pos = np.array([50, 2.5, 106])  # CO2e, Growth, Materials

# Define all paths
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

# Create dictionary to store all artists (lines, points, and texts) for each path
path_artists = {}

# Plot paths with year markers function
def plot_path_with_years(x, y, z, color, label):
    line, = ax.plot(x, z, y, color=color, label=label, linewidth=2)
    artists = [line]
    # Add year markers every 10 years
    for i in range(0, len(years), 10):
        if i > 0:  # Skip 2024 as it's marked by the red dot
            point = ax.scatter(x[i], z[i], y[i], color=color, s=30)
            text = ax.text(x[i], z[i], y[i], f'{int(years[i])}', color=color)
            artists.extend([point, text])
    return artists

# Plot current position
ax.scatter([current_pos[0]], [current_pos[2]], [current_pos[1]],
          color='red', s=100, label='Current Position (2024)')

# Create dictionary of paths with their properties
paths = {
    'Business As Usual': {'x': bau_x, 'y': bau_y, 'z': bau_z, 'color': 'red'},
    'Degrowth (Hickel)': {'x': dg_x, 'y': dg_y, 'z': dg_z, 'color': 'blue'},
    'Great Simplification (Hagens)': {'x': gs_x, 'y': gs_y, 'z': gs_z, 'color': 'green'},
    'Eco-modernist Utopia': {'x': em_x, 'y': em_y, 'z': em_z, 'color': 'cyan'}
}

# Plot paths and store all artists
for name, path in paths.items():
    path_artists[name] = plot_path_with_years(path['x'], path['y'], path['z'], path['color'], name)

# Create checkbuttons with no frame
rax = plt.axes([0.02, 0.4, 0.12, 0.2])
rax.set_frame_on(False)
check = CheckButtons(rax, list(paths.keys()), [True] * len(paths))

def func(label):
    # Toggle visibility for all artists associated with the path
    for artist in path_artists[label]:
        artist.set_visible(not artist.get_visible())
    plt.draw()

check.on_clicked(func)

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

# Add legend below the chart
ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=3)

# Add text for controls
fig.text(0.02, 0.95, 'Controls:', fontsize=10)
fig.text(0.02, 0.92, 'Left mouse: Rotate', fontsize=8)
fig.text(0.02, 0.89, 'Right mouse: Zoom', fontsize=8)
fig.text(0.02, 0.86, 'Middle mouse: Pan', fontsize=8)

# Adjust layout to prevent legend cutoff
plt.subplots_adjust(bottom=0.2)

plt.show()