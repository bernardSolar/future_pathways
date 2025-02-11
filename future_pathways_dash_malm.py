import dash
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np
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


@dataclass
class PathConfig:
    """Configuration for a pathway"""
    name: str
    color: str
    marker: str


class FuturePathwaysApp:
    def __init__(self, start_year: int = 2024, end_year: int = 2060):
        self.start_year = start_year
        self.end_year = end_year
        self.years = np.linspace(start_year, end_year, 37)
        self.t = np.linspace(0, 1, 37)
        self.current_pos = np.array([50, 2.5, 106])  # CO2e, Growth, Materials

        # Historical data
        self.historical_years = np.array([1995, 2000, 2005, 2010, 2015, 2020, 2024])
        self.historical_emissions = np.array([23.0, 25.5, 30.0, 33.5, 36.5, 43.0, 50.0])
        self.historical_growth = np.array([3.3, 4.4, 3.9, 4.3, 2.9, -3.3, 2.5])
        self.historical_materials = np.array([45.0, 54.0, 65.0, 78.0, 88.0, 98.0, 106.0])

        # Initialize zones and paths configurations
        self.zones = self._initialize_zones()
        self.paths = self._initialize_paths()

        # Initialize app
        self.app = dash.Dash(__name__)
        self.setup_layout()

    def _initialize_zones(self) -> Dict[str, ZoneConfig]:
        """Initialize zone configurations"""
        return {
            'Energy Transition Zone': ZoneConfig(
                name='Energy Transition Zone',
                color='green',
                growth_range=(2.5, 5),
                material_range=(0, 106),
                emission_range=(-20, 50)
            ),
            'Intermediate Zone': ZoneConfig(
                name='Intermediate Zone',
                color='orange',
                growth_range=(0, 2.5),
                material_range=(0, 106),
                emission_range=(-20, 50)
            ),
            'Descent Zone': ZoneConfig(
                name='Descent Zone',
                color='red',
                growth_range=(-5, 0),
                material_range=(0, 106),
                emission_range=(-20, 50)
            ),
            'Future Materials Use': ZoneConfig(
                name='Future Materials Use',
                color='blue',
                growth_range=(-5, 5),
                material_range=(106, 160),
                emission_range=(-20, 50)
            )
        }

    def _initialize_paths(self) -> Dict[str, PathConfig]:
        """Initialize pathway configurations"""
        return {
            'Historical Trajectory': PathConfig(
                name='Historical Trajectory',
                color='black',
                marker='diamond'
            ),
            'Business As Usual': PathConfig(
                name='Business As Usual',
                color='red',
                marker='square'
            ),
            'Degrowth (Hickel)': PathConfig(
                name='Degrowth (Hickel)',
                color='blue',
                marker='diamond-open'
            ),
            'Great Simplification (Hagens)': PathConfig(
                name='Great Simplification (Hagens)',
                color='green',
                marker='circle'
            ),
            'Eco-modernist Utopia': PathConfig(
                name='Eco-modernist Utopia',
                color='grey',
                marker='circle-open'
            ),
            'Way et al. Fast Transition': PathConfig(
                name='Way et al. Fast Transition',
                color='magenta',
                marker='cross'
            ),
            'Way et al. Slow Transition': PathConfig(
                name='Way et al. Slow Transition',
                color='purple',
                marker='x'
            ),
            'Way et al. No Transition': PathConfig(
                name='Way et al. No Transition',
                color='brown',
                marker='square-open'
            ),
            'Malm Overshoot Scenario': PathConfig(
                name='Malm Overshoot Scenario',
                color='teal',
                marker='square'
            ),
            'Economic and Infrastructural Inertia': PathConfig(
                name='Economic and Infrastructural Inertia',
                color='olive',  # Chosen color for this pathway
                marker='diamond'  # Using an allowed symbol; note it may duplicate another marker style
            )
        }

    def _create_zone_surface(self, zone: ZoneConfig) -> List[go.Surface]:
        """Create surface traces for a transition zone"""
        surfaces = []

        # Create meshgrid for the zone
        emissions = np.linspace(zone.emission_range[0], zone.emission_range[1], 20)
        materials = np.linspace(zone.material_range[0], zone.material_range[1], 20)
        emissions_grid, materials_grid = np.meshgrid(emissions, materials)

        # Create horizontal surfaces at zone boundaries
        for growth in zone.growth_range:
            growth_grid = np.full_like(emissions_grid, growth)
            surfaces.append(
                go.Surface(
                    x=materials_grid,
                    y=emissions_grid,
                    z=growth_grid,
                    showscale=False,
                    opacity=0.1,
                    colorscale=[[0, zone.color], [1, zone.color]],
                    name=zone.name,
                    legendgroup=f"zone_{zone.name}",
                    showlegend=True if growth == zone.growth_range[0] else False
                )
            )

        # Create vertical surfaces at material boundaries
        growth_values = np.linspace(zone.growth_range[0], zone.growth_range[1], 20)
        for material in [zone.material_range[0], zone.material_range[1]]:
            material_grid = np.full((20, 20), material)
            emissions_grid, growth_grid = np.meshgrid(emissions, growth_values)
            surfaces.append(
                go.Surface(
                    x=material_grid,
                    y=emissions_grid,
                    z=growth_grid,
                    showscale=False,
                    opacity=0.1,
                    colorscale=[[0, zone.color], [1, zone.color]],
                    name=zone.name,
                    legendgroup=f"zone_{zone.name}",
                    showlegend=False
                )
            )

        # Create vertical surfaces at emission boundaries
        for emission in [zone.emission_range[0], zone.emission_range[1]]:
            emission_grid = np.full((20, 20), emission)
            materials_grid, growth_grid = np.meshgrid(materials, growth_values)
            surfaces.append(
                go.Surface(
                    x=materials_grid,
                    y=emission_grid,
                    z=growth_grid,
                    showscale=False,
                    opacity=0.1,
                    colorscale=[[0, zone.color], [1, zone.color]],
                    name=zone.name,
                    legendgroup=f"zone_{zone.name}",
                    showlegend=False
                )
            )

        return surfaces

    def _calculate_future_coordinates(self, path_name: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Calculate future coordinates for a given pathway"""
        if path_name == 'Business As Usual':
            x = self.current_pos[2] + 54 * self.t  # Materials
            y = self.current_pos[0] + 10 * self.t   # Emissions
            z = self.current_pos[1] - 3.5 * self.t   # Growth
        elif path_name == 'Degrowth (Hickel)':
            x = self.current_pos[2] - 56 * self.t
            y = self.current_pos[0] - 60 * self.t
            z = self.current_pos[1] - 4 * self.t + 1.5 * self.t ** 2
        elif path_name == 'Great Simplification (Hagens)':
            x = self.current_pos[2] * np.exp(-1.5 * self.t)
            y = self.current_pos[0] * np.exp(-2 * self.t)
            z = self.current_pos[1] - 3 * self.t - 1.5 * self.t ** 2
        elif path_name == 'Eco-modernist Utopia':
            x = self.current_pos[2] + 40 * self.t * np.exp(-3 * self.t) - 40 * self.t
            y = self.current_pos[0] - 65 * self.t - 5 * self.t ** 2
            z = self.current_pos[1] + 2 * self.t ** 2
        elif path_name == 'Way et al. Fast Transition':
            x = self.current_pos[2] + 30 * self.t * np.exp(-self.t) - 20 * self.t ** 2
            y = self.current_pos[0] * np.exp(-0.15 * (self.t * 36)) - 5 * self.t ** 2
            z = self.current_pos[1] + 0.3 * self.t + 0.7 * self.t ** 2
        elif path_name == 'Way et al. Slow Transition':
            x = self.current_pos[2] + 15 * self.t + 10 * self.t ** 2
            y = self.current_pos[0] * np.exp(-0.06 * (self.t * 36))
            z = self.current_pos[1] + 0.25 * self.t - 0.5 * self.t ** 2
        else:  # Way et al. No Transition (and any others computed continuously)
            x = self.current_pos[2] + 25 * self.t + 15 * self.t ** 2
            y = self.current_pos[0] + 10 * self.t + 5 * self.t ** 2
            z = self.current_pos[1] - self.t - 0.5 * self.t ** 2

        return x, y, z

    def create_3d_figure(self):
        """Create the main 3D scatter plot"""
        fig = go.Figure()

        # Add all zone surfaces
        for zone_name, zone_config in self.zones.items():
            surfaces = self._create_zone_surface(zone_config)
            for surface in surfaces:
                fig.add_trace(surface)

        # Add current position marker
        fig.add_trace(go.Scatter3d(
            x=[self.current_pos[2]],  # Material Use
            y=[self.current_pos[0]],  # CO₂e Emissions
            z=[self.current_pos[1]],  # Growth
            mode='markers',
            marker=dict(size=6, color='red'),
            name='We Are Here (2024)'
        ))

        # Add all pathways
        for path_name, path_config in self.paths.items():
            if path_name == 'Historical Trajectory':
                # Historical trajectory in a single trace
                fig.add_trace(go.Scatter3d(
                    x=self.historical_materials,
                    y=self.historical_emissions,
                    z=self.historical_growth,
                    mode='lines+markers+text',
                    line=dict(color=path_config.color, width=2),
                    marker=dict(
                        symbol=path_config.marker,
                        size=4,
                        color=path_config.color
                    ),
                    text=[f'{int(year)}' for year in self.historical_years],
                    textposition='top right',
                    name=path_name
                ))
            elif path_name == 'Malm Overshoot Scenario':
                # Define the discrete data points for the Malm scenario
                malm_years = np.array([2024, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100])
                malm_materials = np.array([106, 110, 115, 120, 100, 90, 85, 80, 75])
                malm_emissions = np.array([50, 55, 65, 65, 30, 0, -10, -15, -20])
                malm_growth   = np.array([2.5, 2.0, 1.8, 1.5, 0.5, 0.0, 0.5, 1.0, 1.0])

                # Add continuous line trace for the Malm scenario (dashed style)
                fig.add_trace(go.Scatter3d(
                    x=malm_materials,
                    y=malm_emissions,
                    z=malm_growth,
                    mode='lines',
                    line=dict(color=path_config.color, width=4, dash='dash'),
                    name=path_name,
                    legendgroup=path_name
                ))
                # Add markers and text for the Malm scenario
                fig.add_trace(go.Scatter3d(
                    x=malm_materials,
                    y=malm_emissions,
                    z=malm_growth,
                    mode='markers+text',
                    marker=dict(
                        symbol=path_config.marker,
                        size=4,
                        color=path_config.color
                    ),
                    text=[str(year) for year in malm_years],
                    textposition='top right',
                    legendgroup=path_name,
                    showlegend=False
                ))
            elif path_name == 'Economic and Infrastructural Inertia':
                # Define the discrete data points for the inertia pathway
                inertia_years = np.array([2024, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100])
                inertia_materials = np.array([106, 110, 115, 118, 120, 118, 115, 112, 110])
                inertia_emissions = np.array([50, 55, 60, 65, 70, 68, 65, 62, 60])
                inertia_growth   = np.array([2.5, 2.3, 2.0, 1.8, 1.5, 1.2, 1.0, 0.8, 0.8])

                # Add continuous line trace for the inertia pathway (solid line)
                fig.add_trace(go.Scatter3d(
                    x=inertia_materials,
                    y=inertia_emissions,
                    z=inertia_growth,
                    mode='lines',
                    line=dict(color=path_config.color, width=2),
                    name=path_name,
                    legendgroup=path_name
                ))
                # Add markers and text for the inertia pathway
                fig.add_trace(go.Scatter3d(
                    x=inertia_materials,
                    y=inertia_emissions,
                    z=inertia_growth,
                    mode='markers+text',
                    marker=dict(
                        symbol=path_config.marker,
                        size=4,
                        color=path_config.color
                    ),
                    text=[str(year) for year in inertia_years],
                    textposition='top right',
                    legendgroup=path_name,
                    showlegend=False
                ))
            else:
                # For all other pathways, calculate future coordinates continuously
                x, y, z = self._calculate_future_coordinates(path_name)

                # Add continuous line trace
                fig.add_trace(go.Scatter3d(
                    x=x, y=y, z=z,
                    mode='lines',
                    line=dict(color=path_config.color, width=2),
                    name=path_name,
                    legendgroup=path_name
                ))

                # Add decade markers
                decade_indices = range(0, len(self.years), 10)
                fig.add_trace(go.Scatter3d(
                    x=x[decade_indices],
                    y=y[decade_indices],
                    z=z[decade_indices],
                    mode='markers+text',
                    marker=dict(
                        symbol=path_config.marker,
                        size=4,
                        color=path_config.color
                    ),
                    text=[f'{int(self.years[i])}' for i in decade_indices],
                    textposition='top right',
                    legendgroup=path_name,
                    showlegend=False
                ))

        # Set up the layout; note that the CO₂e axis is extended to 80 Gt
        fig.update_layout(
            scene=dict(
                xaxis_title='Material Use (GT)',
                yaxis_title='CO₂e Emissions (GT)',
                zaxis_title='Growth (%)',
                xaxis=dict(range=[0, 200]),
                yaxis=dict(range=[-20, 80]),
                zaxis=dict(range=[-5, 5]),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            title='Future Pathways: 2024-2100',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        return fig

    def setup_layout(self):
        """Set up the Dash app layout"""
        self.app.layout = html.Div([
            html.H1('Future Pathways: 2024-2100'),
            html.Div([
                dcc.Graph(
                    id='future-pathways-3d',
                    figure=self.create_3d_figure(),
                    style={'height': '800px'}
                )
            ]),
            html.Div([
                html.H3('Controls:'),
                html.P('Use mouse to rotate, zoom, and pan the 3D view'),
                html.P('Click on legend items to toggle pathways')
            ])
        ])

    def run_server(self, debug=True):
        """Run the Dash server"""
        self.app.run_server(debug=debug)


if __name__ == '__main__':
    app = FuturePathwaysApp()
    app.run_server(debug=True)
