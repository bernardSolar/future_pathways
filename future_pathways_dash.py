import dash
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional


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

        # Initialize paths configuration
        self.paths = self._initialize_paths()

        # Initialize app
        self.app = dash.Dash(__name__)
        self.setup_layout()

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
            )
        }

    def _calculate_future_coordinates(self, path_name: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Calculate future coordinates for a given pathway"""
        if path_name == 'Business As Usual':
            x = self.current_pos[2] + 54 * self.t  # Materials
            y = self.current_pos[0] + 10 * self.t  # Emissions
            z = self.current_pos[1] - 3.5 * self.t  # Growth
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
        else:  # Way et al. No Transition
            x = self.current_pos[2] + 25 * self.t + 15 * self.t ** 2
            y = self.current_pos[0] + 10 * self.t + 5 * self.t ** 2
            z = self.current_pos[1] - self.t - 0.5 * self.t ** 2

        return x, y, z

    def create_3d_figure(self):
        """Create the main 3D scatter plot"""
        fig = go.Figure()

        # Add current position marker
        fig.add_trace(go.Scatter3d(
            x=[self.current_pos[2]],  # Material Use
            y=[self.current_pos[0]],  # CO2e Emissions
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
            else:
                # Calculate future coordinates
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

        # Set up the layout
        fig.update_layout(
            scene=dict(
                xaxis_title='Material Use (GT/yr)',
                yaxis_title='CO2e Emissions (GT/yr)',
                zaxis_title='Growth (%/yr)',
                xaxis=dict(range=[0, 200]),
                yaxis=dict(range=[-20, 60]),
                zaxis=dict(range=[-5, 5]),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            title='Future Pathways: 2024-2060',
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
            html.H1('Future Pathways: 2024-2060'),
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