import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import CheckButtons
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional


@dataclass
class ZoneConfig:
    """Configuration for a transition zone"""
    name: str
    color: str
    growth_range: Tuple[float, float]
    material_range: Tuple[float, float]
    emission_range: Tuple[float, float]
    text_position: Tuple[float, float, float]
    surfaces: List = None
    text_handle: Optional[object] = None

    def __post_init__(self):
        self.surfaces = [] if self.surfaces is None else self.surfaces


@dataclass
class PathConfig:
    """Configuration for a pathway"""
    name: str
    color: str
    marker: str
    artists: List = None

    def __post_init__(self):
        self.artists = [] if self.artists is None else self.artists


class PathwayVisualizer:
    """
    A class for visualizing future energy transition pathways in 3D space.

    This visualization shows different possible trajectories for society's energy transition,
    plotting paths through zones representing different states of growth, material use, and
    CO2 emissions.
    """

    def __init__(self, start_year: int = 2024, end_year: int = 2060):
        """
        Initialize the visualization with time range and starting parameters.

        Args:
            start_year: Starting year for the visualization
            end_year: Ending year for the visualization
        """
        self.start_year = start_year
        self.end_year = end_year
        self.years = np.linspace(start_year, end_year, 37)
        self.t = np.linspace(0, 1, 37)
        self.current_pos = np.array([50, 2.5, 106])  # CO2e, Growth, Materials

        # Initialize zones configuration
        self.zones = {
            'Energy Transition Zone': ZoneConfig(
                name='Energy Transition Zone',
                color='green',
                growth_range=(2.5, 5),
                material_range=(0, 106),
                emission_range=(-20, 50),
                text_position=(0, 50, 3.75)
            ),
            'Intermediate Zone': ZoneConfig(
                name='Intermediate Zone',
                color='orange',
                growth_range=(0, 2.5),
                material_range=(0, 106),
                emission_range=(-20, 50),
                text_position=(0, 50, 1.25)
            ),
            'Descent Zone': ZoneConfig(
                name='Descent Zone',
                color='red',
                growth_range=(-5, 0),
                material_range=(0, 106),
                emission_range=(-20, 50),
                text_position=(0, 50, -2.5)
            ),
            'Future Materials Use': ZoneConfig(
                name='Future Materials Use',
                color='blue',
                growth_range=(-5, 5),
                material_range=(106, 160),
                emission_range=(-20, 50),
                text_position=(0, 130, 0)
            )
        }

        # Initialize paths configuration
        self.paths = self._initialize_paths()

        # Setup visualization
        self.setup_figure()
        self.create_transition_zones()
        self.plot_paths()
        self.setup_controls()
        self.finalize_plot()

    def _initialize_paths(self) -> Dict[str, PathConfig]:
        """Initialize pathway configurations"""
        return {
            'Business As Usual': PathConfig(
                name='Business As Usual',
                color='red',
                marker='s'  # square
            ),
            'Degrowth (Hickel)': PathConfig(
                name='Degrowth (Hickel)',
                color='blue',
                marker='^'  # triangle up
            ),
            'Great Simplification (Hagens)': PathConfig(
                name='Great Simplification (Hagens)',
                color='green',
                marker='v'  # triangle down
            ),
            'Eco-modernist Utopia': PathConfig(
                name='Eco-modernist Utopia',
                color='grey',
                marker='D'  # diamond
            ),
            'Way et al. Fast Transition': PathConfig(
                name='Way et al. Fast Transition',
                color='magenta',
                marker='o'  # circle
            ),
            'Way et al. Slow Transition': PathConfig(
                name='Way et al. Slow Transition',
                color='purple',
                marker='p'  # pentagon
            ),
            'Way et al. No Transition': PathConfig(
                name='Way et al. No Transition',
                color='brown',
                marker='h'  # hexagon
            )
        }

    def setup_figure(self):
        """Initialize the figure and 3D axes"""
        self.fig = plt.figure(figsize=(15, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')

    def _calculate_path_coordinates(self, path_name: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate the coordinates for a given pathway.

        Args:
            path_name: Name of the pathway to calculate coordinates for

        Returns:
            Tuple of (x, y, z) coordinates arrays
        """
        if path_name == 'Business As Usual':
            x = self.current_pos[0] + 10 * self.t
            y = self.current_pos[1] - 3.5 * self.t
            z = self.current_pos[2] + 54 * self.t
        elif path_name == 'Degrowth (Hickel)':
            x = self.current_pos[0] - 60 * self.t
            y = self.current_pos[1] - 4 * self.t + 1.5 * self.t ** 2
            z = self.current_pos[2] - 56 * self.t
        elif path_name == 'Great Simplification (Hagens)':
            x = self.current_pos[0] * np.exp(-2 * self.t)
            y = self.current_pos[1] - 3 * self.t - 1.5 * self.t ** 2
            z = self.current_pos[2] * np.exp(-1.5 * self.t)
        elif path_name == 'Eco-modernist Utopia':
            x = self.current_pos[0] - 65 * self.t - 5 * self.t ** 2
            y = self.current_pos[1] + 2 * self.t ** 2
            z = self.current_pos[2] + 40 * self.t * np.exp(-3 * self.t) - 40 * self.t
        elif path_name == 'Way et al. Fast Transition':
            x = self.current_pos[0] * np.exp(-0.15 * (self.t * 36)) - 5 * self.t ** 2
            y = self.current_pos[1] + 0.3 * self.t + 0.7 * self.t ** 2
            z = self.current_pos[2] + 30 * self.t * np.exp(-self.t) - 20 * self.t ** 2
        elif path_name == 'Way et al. Slow Transition':
            x = self.current_pos[0] * np.exp(-0.06 * (self.t * 36))
            y = self.current_pos[1] + 0.25 * self.t - 0.5 * self.t ** 2
            z = self.current_pos[2] + 15 * self.t + 10 * self.t ** 2
        else:  # Way et al. No Transition
            x = self.current_pos[0] + 10 * self.t + 5 * self.t ** 2
            y = self.current_pos[1] - self.t - 0.5 * self.t ** 2
            z = self.current_pos[2] + 25 * self.t + 15 * self.t ** 2

        return x, y, z

    def create_transition_zones(self):
        """Create all transition zone surfaces"""
        x = np.linspace(-20, 50, 20)
        y = np.linspace(0, 160, 20)  # Extended to accommodate Future Materials Use zone
        X, Y = np.meshgrid(x, y)

        for zone in self.zones.values():
            # Create horizontal surfaces
            z_range = np.linspace(zone.growth_range[0], zone.growth_range[1], 20)
            for growth in z_range:
                # Only create surfaces within the zone's material range
                mask = (Y >= zone.material_range[0]) & (Y <= zone.material_range[1])
                Z = np.full_like(X, growth)
                Z[~mask] = np.nan  # Make surfaces outside material range invisible
                surface = self.ax.plot_surface(X, Y, Z, alpha=0.02, color=zone.color)
                zone.surfaces.append(surface)

        self._create_vertical_surfaces()

    def _create_vertical_surfaces(self):
        """Create vertical surfaces for all zones"""
        for zone in self.zones.values():
            # Create vertical surfaces at material range boundaries
            x_wall = np.linspace(-20, 50, 20)
            z_wall = np.linspace(zone.growth_range[0], zone.growth_range[1], 20)
            X_wall, Z_wall = np.meshgrid(x_wall, z_wall)

            # Front wall at maximum material value
            Y_wall_max = np.full_like(X_wall, zone.material_range[1])
            surface = self.ax.plot_surface(X_wall, Y_wall_max, Z_wall,
                                           alpha=0.02, color=zone.color)
            zone.surfaces.append(surface)

            # Back wall at minimum material value
            Y_wall_min = np.full_like(X_wall, zone.material_range[0])
            surface = self.ax.plot_surface(X_wall, Y_wall_min, Z_wall,
                                           alpha=0.02, color=zone.color)
            zone.surfaces.append(surface)

            # Side walls
            y_wall = np.linspace(zone.material_range[0], zone.material_range[1], 20)
            Y_wall, Z_wall = np.meshgrid(y_wall, z_wall)

            # Right side wall at maximum emissions
            X_wall_max = np.full_like(Y_wall, zone.emission_range[1])
            surface = self.ax.plot_surface(X_wall_max, Y_wall, Z_wall,
                                           alpha=0.02, color=zone.color)
            zone.surfaces.append(surface)

            # Left side wall at minimum emissions
            X_wall_min = np.full_like(Y_wall, zone.emission_range[0])
            surface = self.ax.plot_surface(X_wall_min, Y_wall, Z_wall,
                                           alpha=0.02, color=zone.color)
            zone.surfaces.append(surface)

    def plot_paths(self):
        """Plot all pathways and current position"""
        # Plot current position
        self.ax.scatter([self.current_pos[0]], [self.current_pos[2]], [self.current_pos[1]],
                        color='red', s=100, label='We Are Here (2024)')

        # Plot all paths
        for path_name, path_config in self.paths.items():
            x, y, z = self._calculate_path_coordinates(path_name)
            path_config.artists = self._plot_path_with_years(
                x, z, y, path_config.color, path_name, path_config.marker
            )

    def _plot_path_with_years(self, x, z, y, color, label, marker):
        """Plot a single path with year markers"""
        line, = self.ax.plot(x, z, y, color=color, label=label, linewidth=2)
        artists = [line]

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

        # Modify the appearance of each pathway label
        for i, label in enumerate(self.check.labels):
            self.check.labels[i].set_color(self.paths[label.get_text()].color)

        self.check.on_clicked(self._toggle_path)

        # Create separate axes for transition zone controls
        tax = plt.axes([0.02, 0.25, 0.12, 0.1])  # Adjusted height to accommodate new zone
        tax.set_frame_on(False)

        # Create checkbuttons for zones
        self.zone_check = CheckButtons(tax, list(self.zones.keys()), [True] * len(self.zones))

        # Set colors for zone labels
        for i, zone_name in enumerate(self.zones.keys()):
            self.zone_check.labels[i].set_color(self.zones[zone_name].color)

        self.zone_check.on_clicked(self._toggle_zones)

    def _toggle_path(self, label):
        """Callback for toggling path visibility"""
        for artist in self.paths[label].artists:
            artist.set_visible(not artist.get_visible())
        plt.draw()

    def _toggle_zones(self, label):
        """Callback for toggling zone visibility"""
        zone = self.zones[label]
        for surface in zone.surfaces:
            surface.set_visible(not surface.get_visible())
        zone.text_handle.set_visible(not zone.text_handle.get_visible())
        plt.draw()

    def finalize_plot(self):
        """Set up final plot parameters and styling"""
        # Set labels and title
        self.ax.set_xlabel('CO2e Emissions (GT/yr)')
        self.ax.set_zlabel('Growth (%/yr)')
        self.ax.set_ylabel('Material Use (GT/yr)')
        self.ax.set_title('Future Pathways: 2024-2060')

        # Add zone labels
        for zone in self.zones.values():
            zone.text_handle = self.ax.text(*zone.text_position,
                                                f"{zone.name}",
                                                color=zone.color,
                                                fontsize=10)

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

if __name__ == "__main__":
    viz = PathwayVisualizer()
    viz.show()