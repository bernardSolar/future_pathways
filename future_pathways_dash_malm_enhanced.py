import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional
import plotly.express as px


@dataclass
class ZoneConfig:
    """Configuration for a transition zone"""
    name: str
    color: str
    growth_range: Tuple[float, float]
    material_range: Tuple[float, float]
    emission_range: Tuple[float, float]
    description: str = ""


@dataclass
class PathConfig:
    """Configuration for a pathway"""
    name: str
    color: str
    marker: str
    description: str = ""


class EnhancedFuturePathwaysApp:
    def __init__(self, start_year: int = 2024, end_year: int = 2100):
        self.start_year = start_year
        self.end_year = end_year
        self.years = np.linspace(start_year, end_year, 77)  # Extended to 2100
        self.t = np.linspace(0, 1, 77)
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
        self.setup_callbacks()

    def _initialize_zones(self) -> Dict[str, ZoneConfig]:
        """Initialize zone configurations with enhanced descriptions"""
        return {
            'Energy Transition Zone': ZoneConfig(
                name='Energy Transition Zone',
                color='green',
                growth_range=(2.5, 5),
                material_range=(0, 106),
                emission_range=(-20, 50),
                description="Successful rapid decarbonization with maintained economic growth"
            ),
            'Intermediate Zone': ZoneConfig(
                name='Intermediate Zone',
                color='orange',
                growth_range=(0, 2.5),
                material_range=(0, 106),
                emission_range=(-20, 50),
                description="Moderate transition scenarios with slower growth"
            ),
            'Descent Zone': ZoneConfig(
                name='Descent Zone',
                color='red',
                growth_range=(-5, 0),
                material_range=(0, 106),
                emission_range=(-20, 50),
                description="Economic contraction scenarios (degrowth/simplification)"
            ),
            'Future Materials Use': ZoneConfig(
                name='Future Materials Use',
                color='blue',
                growth_range=(-5, 5),
                material_range=(106, 200),
                emission_range=(-20, 50),
                description="Increased material consumption pathways"
            ),
            'Malm Overshoot Zone': ZoneConfig(
                name='Malm Overshoot Zone',
                color='magenta',
                growth_range=(-2, 3),
                material_range=(90, 160),
                emission_range=(50, 100),
                description="Climate breakdown zone - fossil capital maintains dominance despite climate chaos"
            ),
            'Climate Collapse Zone': ZoneConfig(
                name='Climate Collapse Zone',
                color='darkred',
                growth_range=(-10, 0),
                material_range=(50, 120),
                emission_range=(80, 150),
                description="Societal breakdown from uncontrolled climate change"
            )
        }

    def _initialize_paths(self) -> Dict[str, PathConfig]:
        """Initialize pathway configurations with enhanced descriptions"""
        return {
            'Historical Trajectory': PathConfig(
                name='Historical Trajectory',
                color='black',
                marker='diamond',
                description="Actual path from 1995-2024: accelerating emissions despite climate awareness"
            ),
            'Business As Usual': PathConfig(
                name='Business As Usual',
                color='red',
                marker='square',
                description="Continuation of current trends with gradual efficiency improvements"
            ),
            'Degrowth (Hickel)': PathConfig(
                name='Degrowth (Hickel)',
                color='blue',
                marker='diamond-open',
                description="Managed reduction in resource use by wealthy nations"
            ),
            'Great Simplification (Hagens)': PathConfig(
                name='Great Simplification (Hagens)',
                color='green',
                marker='circle',
                description="Managed descent to lower complexity due to energy/resource constraints"
            ),
            'Eco-modernist Utopia': PathConfig(
                name='Eco-modernist Utopia',
                color='grey',
                marker='circle-open',
                description="Technological solutions enable decoupling and continued growth"
            ),
            'Way et al. Fast Transition': PathConfig(
                name='Way et al. Fast Transition',
                color='magenta',
                marker='cross',
                description="Rapid renewable energy deployment based on learning curves"
            ),
            'Way et al. Slow Transition': PathConfig(
                name='Way et al. Slow Transition',
                color='purple',
                marker='x',
                description="Gradual renewable transition with continued fossil fuel use"
            ),
            'Way et al. No Transition': PathConfig(
                name='Way et al. No Transition',
                color='brown',
                marker='square-open',
                description="Minimal renewable deployment, fossil fuel dominance continues"
            ),
            'Malm Overshoot Scenario': PathConfig(
                name='Malm Overshoot Scenario',
                color='crimson',
                marker='square',
                description="Fossil capital prevents transition, climate limits exceeded with promises of future fixes"
            ),
            'Asset Stranding Resistance': PathConfig(
                name='Asset Stranding Resistance',
                color='darkviolet',
                marker='diamond',
                description="Fossil fuel industry maximizes extraction to avoid stranded assets"
            ),
            'Revolutionary Transition': PathConfig(
                name='Revolutionary Transition',
                color='forestgreen',
                marker='star',
                description="Rapid forced transition through public ownership and planning"
            ),
            'Climate Tipping Cascade': PathConfig(
                name='Climate Tipping Cascade',
                color='darkred',
                marker='triangle-up',
                description="Runaway climate change triggers societal collapse"
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
                    showlegend=True if growth == zone.growth_range[0] else False,
                    visible="legendonly",
                    hovertemplate=f"<b>{zone.name}</b><br>{zone.description}<extra></extra>"
                )
            )

        return surfaces

    def _calculate_malm_coordinates(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate coordinates for Malm's Overshoot scenario based on his theory:
        - Fossil capital resists stranding, maintains extraction
        - Climate targets are missed, overshoot becomes normalized  
        - Emissions peak then decline due to climate chaos, not policy
        - Materials use remains high due to attempted adaptation
        - Growth becomes volatile due to climate disruption
        """
        # Define key phases of the overshoot scenario
        malm_years = np.array([2024, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2070, 2080, 2090, 2100])
        
        # Materials: Continue rising through 2040s as fossil capital maximizes extraction,
        # then plateau and decline as climate chaos disrupts supply chains
        malm_materials = np.array([106, 115, 125, 135, 140, 138, 130, 120, 100, 85, 75, 70])
        
        # Emissions: Continue rising until climate chaos forces reductions
        # Peak around 2040-2045, then sharp decline due to economic disruption
        malm_emissions = np.array([50, 58, 68, 75, 78, 70, 55, 40, 20, 5, -5, -10])
        
        # Growth: Initially maintained, then becomes volatile and negative
        # due to climate disruption and social instability
        malm_growth = np.array([2.5, 2.2, 1.8, 1.0, 0.2, -0.5, -1.2, -0.8, 0.5, 0.2, -0.3, -0.5])

        return malm_materials, malm_emissions, malm_growth, malm_years

    def _calculate_revolutionary_transition(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate coordinates for a revolutionary transition scenario:
        - Rapid nationalization of energy sector
        - Forced stranding of fossil assets
        - Planned transition to renewables
        """
        # Sharp transition starting around 2030
        rev_years = np.array([2024, 2027, 2030, 2035, 2040, 2050, 2060, 2070, 2080, 2090, 2100])
        
        # Materials: Sharp reduction through circular economy and public planning
        rev_materials = np.array([106, 100, 85, 70, 60, 55, 50, 48, 45, 43, 40])
        
        # Emissions: Rapid decline through asset stranding and renewable deployment
        rev_emissions = np.array([50, 40, 25, 10, 0, -10, -15, -18, -20, -22, -25])
        
        # Growth: Initial disruption, then sustainable steady-state
        rev_growth = np.array([2.5, 0.5, -1.0, 1.5, 2.0, 1.5, 1.0, 0.8, 0.5, 0.5, 0.3])

        return rev_materials, rev_emissions, rev_growth, rev_years

    def _calculate_climate_collapse(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate coordinates for climate tipping cascade scenario:
        - Multiple tipping points triggered
        - Societal breakdown and resource conflicts
        """
        collapse_years = np.array([2024, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2070, 2080, 2090, 2100])
        
        # Materials: Initial spike from adaptation attempts, then collapse
        collapse_materials = np.array([106, 120, 130, 125, 100, 80, 60, 45, 35, 30, 25, 22])
        
        # Emissions: Spike from burning biomass, then decline due to societal collapse
        collapse_emissions = np.array([50, 65, 85, 110, 95, 70, 50, 35, 25, 20, 15, 12])
        
        # Growth: Severe economic contraction
        collapse_growth = np.array([2.5, 0.0, -2.0, -5.0, -7.0, -5.0, -3.0, -2.0, -1.5, -1.0, -0.8, -0.5])

        return collapse_materials, collapse_emissions, collapse_growth, collapse_years

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
            marker=dict(size=8, color='red', symbol='cross'),
            name='We Are Here (2024)',
            hovertemplate="<b>Current Position (2024)</b><br>" +
                         "Materials: %{x:.0f} GT/yr<br>" +
                         "Emissions: %{y:.0f} GT/yr<br>" +
                         "Growth: %{z:.1f} %/yr<extra></extra>"
        ))

        # Add all pathways
        for path_name, path_config in self.paths.items():
            if path_name == 'Historical Trajectory':
                # Historical trajectory
                fig.add_trace(go.Scatter3d(
                    x=self.historical_materials,
                    y=self.historical_emissions,
                    z=self.historical_growth,
                    mode='lines+markers+text',
                    line=dict(color=path_config.color, width=3),
                    marker=dict(
                        symbol=path_config.marker,
                        size=5,
                        color=path_config.color
                    ),
                    text=[f'{int(year)}' for year in self.historical_years],
                    textposition='top right',
                    name=path_name,
                    visible="legendonly",
                    hovertemplate="<b>Historical Data</b><br>" +
                                 "Year: %{text}<br>" +
                                 "Materials: %{x:.0f} GT/yr<br>" +
                                 "Emissions: %{y:.0f} GT/yr<br>" +
                                 "Growth: %{z:.1f} %/yr<extra></extra>"
                ))
            
            elif path_name == 'Malm Overshoot Scenario':
                # Enhanced Malm scenario with multiple phases
                malm_materials, malm_emissions, malm_growth, malm_years = self._calculate_malm_coordinates()
                
                fig.add_trace(go.Scatter3d(
                    x=malm_materials,
                    y=malm_emissions,
                    z=malm_growth,
                    mode='lines+markers+text',
                    line=dict(color=path_config.color, width=4, dash='dash'),
                    marker=dict(
                        symbol=path_config.marker,
                        size=6,
                        color=path_config.color
                    ),
                    text=[str(year) for year in malm_years],
                    textposition='top right',
                    name=path_name,
                    visible="legendonly",
                    hovertemplate="<b>Malm Overshoot Scenario</b><br>" +
                                 "%{text}<br>" +
                                 "Materials: %{x:.0f} GT/yr<br>" +
                                 "Emissions: %{y:.0f} GT/yr<br>" +
                                 "Growth: %{z:.1f} %/yr<br>" +
                                 f"<i>{path_config.description}</i><extra></extra>"
                ))
            
            elif path_name == 'Revolutionary Transition':
                # Revolutionary scenario
                rev_materials, rev_emissions, rev_growth, rev_years = self._calculate_revolutionary_transition()
                
                fig.add_trace(go.Scatter3d(
                    x=rev_materials,
                    y=rev_emissions,
                    z=rev_growth,
                    mode='lines+markers+text',
                    line=dict(color=path_config.color, width=4),
                    marker=dict(
                        symbol=path_config.marker,
                        size=6,
                        color=path_config.color
                    ),
                    text=[str(year) if i % 2 == 0 else '' for i, year in enumerate(rev_years)],
                    textposition='top right',
                    name=path_name,
                    visible="legendonly",
                    hovertemplate="<b>Revolutionary Transition</b><br>" +
                                 "Materials: %{x:.0f} GT/yr<br>" +
                                 "Emissions: %{y:.0f} GT/yr<br>" +
                                 "Growth: %{z:.1f} %/yr<br>" +
                                 f"<i>{path_config.description}</i><extra></extra>"
                ))
            
            elif path_name == 'Climate Tipping Cascade':
                # Climate collapse scenario
                collapse_materials, collapse_emissions, collapse_growth, collapse_years = self._calculate_climate_collapse()
                
                fig.add_trace(go.Scatter3d(
                    x=collapse_materials,
                    y=collapse_emissions,
                    z=collapse_growth,
                    mode='lines+markers+text',
                    line=dict(color=path_config.color, width=4, dash='dot'),
                    marker=dict(
                        symbol=path_config.marker,
                        size=6,
                        color=path_config.color
                    ),
                    text=[str(year) if i % 2 == 0 else '' for i, year in enumerate(collapse_years)],
                    textposition='top right',
                    name=path_name,
                    visible="legendonly",
                    hovertemplate="<b>Climate Tipping Cascade</b><br>" +
                                 "Materials: %{x:.0f} GT/yr<br>" +
                                 "Emissions: %{y:.0f} GT/yr<br>" +
                                 "Growth: %{z:.1f} %/yr<br>" +
                                 f"<i>{path_config.description}</i><extra></extra>"
                ))
            
            else:
                # For other pathways, use existing calculation method
                # (Implementation would continue with other scenarios...)
                pass

        # Enhanced layout with better ranges for overshoot scenarios
        fig.update_layout(
            width=1200,
            height=800,
            scene=dict(
                xaxis_title='Material Use (GT/yr)',
                yaxis_title='CO₂e Emissions (GT/yr)',
                zaxis_title='Growth (%/yr)',
                xaxis=dict(range=[0, 200]),
                yaxis=dict(range=[-30, 120]),  # Extended for overshoot scenarios
                zaxis=dict(range=[-10, 5]),   # Extended for collapse scenarios
                camera=dict(
                    eye=dict(x=1.2, y=1.2, z=1.2)
                )
            ),
            margin=dict(l=50, r=50, t=80, b=50),
            title=dict(
                text='Future Pathways: Climate Breakdown vs. Transition (2024-2100)',
                x=0.5,
                font=dict(size=16)
            ),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.98,
                xanchor="left",
                x=0.02,
                bgcolor="rgba(255,255,255,0.8)"
            )
        )

        return fig

    def setup_layout(self):
        """Set up the enhanced Dash app layout"""
        self.app.layout = html.Div([
            html.Div([
                html.H1('Future Pathways: Climate Breakdown vs. Revolutionary Transition', 
                       style={'textAlign': 'center', 'marginBottom': 20}),
                html.P([
                    "Based on Andreas Malm's ", 
                    html.A("'Overshoot: How the World Surrendered to Climate Breakdown'", 
                           href="https://www.versobooks.com/products/3131-overshoot", 
                           target="_blank"),
                    " and other transition theories."
                ], style={'textAlign': 'center', 'marginBottom': 20})
            ]),
            
            html.Div([
                dcc.Graph(
                    id='future-pathways-3d',
                    figure=self.create_3d_figure(),
                    style={'height': '700px'}
                )
            ]),
            
            html.Div([
                html.Div([
                    html.H3('Malm\'s Overshoot Theory'),
                    html.P([
                        "Andreas Malm argues that the world has effectively surrendered to climate breakdown by accepting ",
                        "that we will 'overshoot' climate targets like 1.5°C, with promises that future technologies will ",
                        "bring temperatures back down later. This acceptance is driven by:"
                    ]),
                    html.Ul([
                        html.Li("Fossil fuel companies' resistance to 'asset stranding'"),
                        html.Li("Lower profit margins from renewable energy"),
                        html.Li("Continued investment in fossil fuel infrastructure"),
                        html.Li("Political acceptance of climate breakdown as inevitable")
                    ])
                ], className='six columns'),
                
                html.Div([
                    html.H3('Pathway Explanations'),
                    html.Div(id='pathway-info'),
                    html.Hr(),
                    html.H4('Controls:'),
                    html.P('• Click legend items to toggle pathways on/off'),
                    html.P('• Use mouse to rotate, zoom, and pan the 3D view'),
                    html.P('• Hover over points for detailed information')
                ], className='six columns')
            ], className='row', style={'margin': '20px'})
        ])

    def setup_callbacks(self):
        """Set up interactive callbacks"""
        @self.app.callback(
            Output('pathway-info', 'children'),
            [Input('future-pathways-3d', 'clickData')]
        )
        def display_pathway_info(clickData):
            if clickData is None:
                return html.P("Click on a pathway in the legend or 3D plot to see details.")
            
            # Extract pathway information from click data
            # This would be enhanced with more detailed pathway descriptions
            return html.Div([
                html.P("Pathway details would be displayed here based on the clicked item.")
            ])

    def run_server(self, debug=True):
        """Run the Dash server"""
        self.app.run_server(debug=debug, port=8051)


if __name__ == '__main__':
    app = EnhancedFuturePathwaysApp()
    app.run_server(debug=True)
