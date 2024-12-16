'''
Key features of each pathway:

1. High-Tech Enclaves (Cyan)
* Rapid emissions reduction through technology
* Maintained or increasing growth
* Initial high material use then efficiency gains

2. Sustainable Adaptation Zones (Green)
* Fastest emissions reduction
* Controlled descent to steady state
* Steady material reduction

3. Managed Descent Areas (Blue)
* Moderate emissions reduction
* Accelerating negative growth
* Moderate material reduction

4. Industrial Holdouts (Red)
* Increasing emissions
* Initial growth then crash
* High material use

5. Collapse Zones (Brown)
* Chaotic emissions pattern
* Rapid decline in growth
* Rapid material reduction

6. Mixed-Trajectory Regions (Purple)
* Oscillating patterns in all dimensions
* Shows internal variation
* Reflects complex regional dynamics
'''
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

# Define paths for each region type
# For each path, ensure first point matches current_pos exactly

# High-Tech Enclaves
ht_x = current_pos[0] + t * (-60)  # Starts at 50, goes to -10
ht_y = current_pos[1] + t * 3  # Starts at 2.5, goes to 5.5
ht_z = current_pos[2] + t * (-30)  # Starts at 106, goes to 76

# Sustainable Adaptation Zones
sa_x = current_pos[0] + t * (-65)  # Starts at 50, goes to -15
sa_y = current_pos[1] + t * (-2) + (t**2) * 0.5  # Controlled descent
sa_z = current_pos[2] + t * (-56)  # Steady reduction

# Managed Descent Areas
md_x = current_pos[0] + t * (-40)  # Starts at 50, goes to 10
md_y = current_pos[1] + t * (-3) - t**2  # Accelerating decline
md_z = current_pos[2] + t * (-40)  # Moderate reduction

# Industrial Holdouts
ih_x = current_pos[0] + t * 15  # Starts at 50, goes to 65
ih_y = current_pos[1] + t - 5 * t**2  # Growth then crash
ih_z = current_pos[2] + t * 54  # Increasing use

# Collapse Zones
cz_x = current_pos[0] + t * (-30)  # Starts at 50, sharp decline
cz_y = current_pos[1] - 6 * t  # Sharp decline
cz_z = current_pos[2] - 80 * t  # Sharp reduction

# Mixed-Trajectory Regions
mt_x = current_pos[0] + t * (-30) + 10 * np.sin(4 * np.pi * t)  # Oscillating
mt_y = current_pos[1] + t * (-2) + np.sin(3 * np.pi * t)  # Oscillating
mt_z = current_pos[2] + t * (-20) + 15 * np.sin(2 * np.pi * t)  # Oscillating

# Verify all paths start at current position
print("Starting points verification:")
paths_data = {
    'High-Tech Enclaves': (ht_x[0], ht_y[0], ht_z[0]),
    'Sustainable Adaptation': (sa_x[0], sa_y[0], sa_z[0]),
    'Managed Descent': (md_x[0], md_y[0], md_z[0]),
    'Industrial Holdouts': (ih_x[0], ih_y[0], ih_z[0]),
    'Collapse Zones': (cz_x[0], cz_y[0], cz_z[0]),
    'Mixed-Trajectory': (mt_x[0], mt_y[0], mt_z[0])
}

for name, coords in paths_data.items():
    print(f"{name}: {coords}")

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
    'High-Tech Enclaves': {'x': ht_x, 'y': ht_y, 'z': ht_z, 'color': 'cyan'},
    'Sustainable Adaptation': {'x': sa_x, 'y': sa_y, 'z': sa_z, 'color': 'green'},
    'Managed Descent': {'x': md_x, 'y': md_y, 'z': md_z, 'color': 'blue'},
    'Industrial Holdouts': {'x': ih_x, 'y': ih_y, 'z': ih_z, 'color': 'red'},
    'Collapse Zones': {'x': cz_x, 'y': cz_y, 'z': cz_z, 'color': 'brown'},
    'Mixed-Trajectory': {'x': mt_x, 'y': mt_y, 'z': mt_z, 'color': 'purple'}
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
ax.set_title('Regional Pathways in a Fragmented Future (2024-2060)')

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