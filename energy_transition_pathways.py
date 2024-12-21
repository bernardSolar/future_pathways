import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import CheckButtons


class PathwayVisualizer:
    def __init__(self, start_year=2024, end_year=2060):
        self.start_year = start_year
        self.end_year = end_year
        self.years = np.linspace(start_year, end_year, 37)
        self.t = np.linspace(0, 1, 37)
        self.current_pos = np.array([50, 2.5, 106])  # CO2e, Growth, Materials
        self.path_artists = {}
        self.transition_zone_surfaces = []  # New list to store transition zone surfaces
        self.transition_zone_text = None
        self.setup_figure()
        self.define_paths()
        self.create_transition_zone()
        self.plot_paths()
        self.setup_controls()
        self.finalize_plot()

    def setup_figure(self):
        """Initialize the figure and 3D axes"""
        self.fig = plt.figure(figsize=(15, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')

    def define_paths(self):
        """Define all pathway trajectories"""
        self.paths = {
            'Business As Usual': {
                'x': self.current_pos[0] + 10 * self.t,
                'y': self.current_pos[1] - 3.5 * self.t,
                'z': self.current_pos[2] + 54 * self.t,
                'color': 'red',
                'marker': 's'  # square
            },
            'Degrowth (Hickel)': {
                'x': self.current_pos[0] - 60 * self.t,
                'y': self.current_pos[1] - 4 * self.t + 1.5 * self.t ** 2,
                'z': self.current_pos[2] - 56 * self.t,
                'color': 'blue',
                'marker': '^'  # triangle up
            },
            'Great Simplification (Hagens)': {
                'x': self.current_pos[0] * np.exp(-2 * self.t),
                'y': self.current_pos[1] - 3 * self.t - 1.5 * self.t ** 2,
                'z': self.current_pos[2] * np.exp(-1.5 * self.t),
                'color': 'green',
                'marker': 'v'  # triangle down
            },
            'Eco-modernist Utopia': {
                'x': self.current_pos[0] - 65 * self.t - 5 * self.t ** 2,
                'y': self.current_pos[1] + 2 * self.t ** 2,
                'z': self.current_pos[2] + 40 * self.t * np.exp(-3 * self.t) - 40 * self.t,
                'color': 'grey',
                'marker': 'D'  # diamond
            },
            'Way et al. Fast Transition': {
                'x': self.current_pos[0] * np.exp(-0.15 * (self.t * 36)) - 5 * self.t ** 2,
                'y': self.current_pos[1] + 0.3 * self.t + 0.7 * self.t ** 2,
                'z': self.current_pos[2] + 30 * self.t * np.exp(-self.t) - 20 * self.t ** 2,
                'color': 'magenta',
                'marker': 'o'  # circle
            },
            'Way et al. Slow Transition': {
                'x': self.current_pos[0] * np.exp(-0.06 * (self.t * 36)),
                'y': self.current_pos[1] + 0.25 * self.t - 0.5 * self.t ** 2,
                'z': self.current_pos[2] + 15 * self.t + 10 * self.t ** 2,
                'color': 'purple',
                'marker': 'p'  # pentagon
            },
            'Way et al. No Transition': {
                'x': self.current_pos[0] + 10 * self.t + 5 * self.t ** 2,
                'y': self.current_pos[1] - self.t - 0.5 * self.t ** 2,
                'z': self.current_pos[2] + 25 * self.t + 15 * self.t ** 2,
                'color': 'brown',
                'marker': 'h'  # hexagon
            }
        }

    def create_transition_zone(self):
        """Create the green transition zone surfaces"""
        # Create meshgrid for transition zone
        x = np.linspace(-20, 50, 20)
        y = np.linspace(0, 106, 20)
        z = np.linspace(2.5, 5, 20)
        X, Y = np.meshgrid(x, y)

        # Create horizontal surfaces
        for growth in z:
            Z = np.full_like(X, growth)
            surface = self.ax.plot_surface(X, Y, Z, alpha=0.02, color='green')
            self.transition_zone_surfaces.append(surface)

        # Create vertical surfaces
        self._create_vertical_surfaces()

    def _create_vertical_surfaces(self):
        """Helper method to create vertical surfaces of transition zone"""
        # Front wall
        y_wall = np.linspace(0, 106, 20)
        z_wall = np.linspace(2.5, 5, 20)
        Y_wall, Z_wall = np.meshgrid(y_wall, z_wall)
        X_wall = np.full_like(Y_wall, 50)
        surface = self.ax.plot_surface(X_wall, Y_wall, Z_wall, alpha=0.02, color='green')
        self.transition_zone_surfaces.append(surface)

        # Material use wall
        X_wall = np.linspace(-20, 50, 20)
        Z_wall = np.linspace(2.5, 5, 20)
        X_wall, Z_wall = np.meshgrid(X_wall, Z_wall)
        Y_wall = np.full_like(X_wall, 106)
        surface = self.ax.plot_surface(X_wall, Y_wall, Z_wall, alpha=0.02, color='green')
        self.transition_zone_surfaces.append(surface)

    def plot_paths(self):
        """Plot all pathways and current position"""
        # Plot current position
        self.ax.scatter([self.current_pos[0]], [self.current_pos[2]], [self.current_pos[1]],
                        color='red', s=100, label='Current Position (2024)')

        # Plot all paths
        for name, path in self.paths.items():
            self.path_artists[name] = self._plot_path_with_years(
                path['x'], path['y'], path['z'], path['color'], name
            )

    def _plot_path_with_years(self, x, y, z, color, label):
        """Helper method to plot a single path with year markers"""
        line, = self.ax.plot(x, z, y, color=color, label=label, linewidth=2)
        artists = [line]

        # Get marker style from paths dictionary
        marker = self.paths[label]['marker']

        # Add year markers every 10 years
        for i in range(0, len(self.years), 10):
            if i > 0:  # Skip 2024 as it's marked by the red dot
                point = self.ax.scatter(x[i], z[i], y[i], color=color, marker=marker, s=25)
                text = self.ax.text(x[i], z[i], y[i], f'{int(self.years[i])}', color=color)
                artists.extend([point, text])
        return artists

    def setup_controls(self):
        """Set up the interactive controls with colored labels"""
        # Create axes for pathway controls
        rax = plt.axes([0.02, 0.4, 0.12, 0.2])
        rax.set_frame_on(False)

        # Create checkbuttons for pathways
        self.check = CheckButtons(rax, list(self.paths.keys()), [True] * len(self.paths))

        # Modify the appearance of each label
        for i, label in enumerate(self.check.labels):
            path_props = self.paths[label.get_text()]
            label.set_color(path_props['color'])

        self.check.on_clicked(self._toggle_path)

        # Create separate axes for transition zone control
        tax = plt.axes([0.02, 0.35, 0.12, 0.04])  # Position below pathway controls
        tax.set_frame_on(False)

        # Create checkbutton for transition zone
        self.zone_check = CheckButtons(tax, ['Energy Transition Zone'], [True])
        self.zone_check.labels[0].set_color('green')
        self.zone_check.on_clicked(self._toggle_transition_zone)

    def _toggle_path(self, label):
        """Callback for toggling path visibility"""
        for artist in self.path_artists[label]:
            artist.set_visible(not artist.get_visible())
        plt.draw()

    def _toggle_transition_zone(self, label):
        """Callback for toggling transition zone visibility"""
        for surface in self.transition_zone_surfaces:
            surface.set_visible(not surface.get_visible())
        self.transition_zone_text.set_visible(not self.transition_zone_text.get_visible())
        plt.draw()

    def finalize_plot(self):
        """Set up final plot parameters and styling"""
        # Set labels and title
        self.ax.set_xlabel('CO2e Emissions (GT/yr)')
        self.ax.set_zlabel('Growth (%/yr)')
        self.ax.set_ylabel('Material Use (GT/yr)')
        self.ax.set_title('Future Pathways: 2024-2060')

        # Add transition zone label and store the handle
        self.transition_zone_text = self.ax.text(0, 50, 4, "Energy\nTransition\nZone",
                                                 color='green', fontsize=10)

        # Set axis limits and view
        self.ax.set_xlim([-20, 60])
        self.ax.set_ylim([0, 200])
        self.ax.set_zlim([-5, 5])
        self.ax.invert_xaxis()
        self.ax.view_init(elev=20, azim=45)
        self.ax.grid(True)

        # Add legend and controls text
        self.ax.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=3)
        self._add_control_text()

        # Adjust layout
        plt.subplots_adjust(bottom=0.2)

    def _add_control_text(self):
        """Add text explaining controls"""
        self.fig.text(0.02, 0.95, 'Controls:', fontsize=10)
        self.fig.text(0.02, 0.92, 'Left mouse: Rotate', fontsize=8)
        self.fig.text(0.02, 0.89, 'Right mouse: Zoom', fontsize=8)
        self.fig.text(0.02, 0.86, 'Middle mouse: Pan', fontsize=8)

    def show(self):
        """Display the visualization"""
        plt.show()


# Create and display visualization
if __name__ == "__main__":
    viz = PathwayVisualizer()
    viz.show()