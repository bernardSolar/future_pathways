# Using Future Pathways

This is a quick start guide, for full details about the visualization see [Future Pathways](docs/future_pathways.md).

## Introduction
The Future Pathways visualization presents a three-dimensional analysis of possible trajectories for human civilization, focusing on the interrelationships between economic growth, environmental impact, and resource consumption. This document explains how to install and run the visualization.

## The Three Axes

### X-Axis: CO2e Emissions (GT/yr)
This axis represents annual greenhouse gas emissions in gigatonnes of CO2 equivalent. It ranges from negative values (-20 GT/yr) on the left, representing net carbon removal from the atmosphere, to positive values (60 GT/yr) on the right, indicating net emissions. Our current position is approximately 50 GT/yr.

### Y-Axis: Growth (%/yr)
This vertical axis represents annual economic growth, measured as a percentage change in GDP/energy use/civilization complexity. It ranges from -5% (significant decline) to +5% (rapid growth). Our current position shows approximately 2.5% growth, typical of modern industrial economies.

### Z-Axis: Material Use (GT/yr)
This axis represents annual material consumption, including all extracted resources, from minerals to biomass. Current global material consumption is approximately 106 billion tonnes annually, with projections suggesting potential increases to 160 billion tonnes by 2060 under business-as-usual scenarios.

## Future Pathways Installation Guide

This guide will help you set up and run the Future Pathways energy transition application.

### Prerequisites

- Python 3.x installed on your system
- Git installed on your system
- pip (Python package installer)

### Installation Steps

1. Clone the repository:
   ```console
   git clone https://github.com/bernardSolar/future_pathways.git
   cd future_pathways
   ```

2. Install required Python packages:
   ```console
   pip install numpy matplotlib
   ```
   
   If using Python 3 explicitly:
   ```console
   pip3 install numpy matplotlib
   ```

### Running the Application

You can run the application in one of two ways:

#### Command Line
From the project directory, run:
```console
python3 future_pathways.py
```

#### IDE
Alternatively, you can open the project in an IDE like PyCharm and run `energy_transition_pathways.py` directly.

### Support

If you encounter any issues, please open an issue on the [GitHub repository](https://github.com/bernardSolar/future_pathways).

## Controls
Here are the key controls for interacting with the matplotlib 3D visualization:

Mouse Controls:
1. Left mouse button: Rotate the view by clicking and dragging
2. Right mouse button: Zoom in/out by clicking and dragging up/down
3. Middle mouse button (or scroll wheel): Pan the view by clicking and dragging
4. Scroll wheel: Zoom in/out

The toolbar at the bottom of the window also provides additional controls:
- 🏠 (Home): Reset view to original position
- ⬅️ (Back): Go to previous view
- ➡️ (Forward): Go to next view
- ✛ (Pan): Toggle pan mode (drag view with left mouse)
- 🔍 (Zoom): Toggle zoom mode (draw rectangle to zoom)
- ⚒️ (Configure): Adjust plot parameters
- 💾 (Save): Save the current view as an image

Additional Tips:
- Hold Ctrl + Left mouse zooms into or out of the view while rotating/dragging
- The checkbox panel on the left lets you toggle different pathways on/off

## Further Reading
For full details about the visualization see [Future Pathways](docs/future_pathways.md).

