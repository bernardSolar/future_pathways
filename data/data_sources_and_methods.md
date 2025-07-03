# Historical Civilization Dynamics Dataset (1970-2024)

## Overview
Annual time series data for empirical analysis of civilization dynamics using three key variables:
- CO2 emissions (gigatonnes CO2 per year)
- Material extraction/use (gigatonnes per year)  
- Economic growth rate (percent per year)

## Data Sources & Quality

### CO2 Emissions (1970-2024)
- **Source**: Global Carbon Project / Our World in Data
- **Quality**: High - annual observations from authoritative source
- **Scope**: Fossil fuel and industrial emissions only
- **URL**: https://ourworldindata.org/co2-emissions

### Material Extraction (1970-2024)  
- **Sources**: UNEP Global Material Flows Database + Krausmann et al. (2018)
- **Quality**: High for 1970+ (UNEP), moderate for early period (estimates)
- **Categories**: Biomass + Fossil fuels + Metal ores + Non-metallic minerals
- **URL**: https://www.materialflows.net/

### Economic Growth (1970-2024)
- **Sources**: Maddison Project Database + World Bank WDI
- **Quality**: High - well-established national accounting data
- **Measure**: Real GDP growth rates (inflation-adjusted)
- **URL**: https://ourworldindata.org/economic-growth

## Dataset Characteristics
- **Observations**: 55 annual data points
- **Period**: 1970-2024
- **CO2 Range**: 14.8-50.0 GT/yr
- **Materials Range**: 27.1-106.0 GT/yr  
- **Growth Range**: -3.3% to 4.4%

## Usage for Dynamical Systems Analysis
This dataset enables empirical estimation of parameters for Lorenz-like equations:
- dx/dt = σ(y - x)          [CO2 emissions dynamics]
- dy/dt = x(ρ - z) - y      [Material use dynamics] 
- dz/dt = xy*α - βz         [Economic growth dynamics]

Where: x=CO2, y=Materials, z=Growth

## Data Quality Indicators
- **exact**: Data point exists in original source
- **interpolated**: Linear interpolation between known points

## Files
- `civilization_dynamics_1970_2024.csv`: Main dataset
- `data_sources_and_methods.md`: This documentation file

## Key Historical Events Captured
- 1970s Oil Crises
- 1980s Economic Expansion  
- 1990s Post-Cold War Growth
- 2000s China's Rapid Industrialization
- 2008 Global Financial Crisis
- 2020 COVID-19 Pandemic

## References
- Krausmann, F., et al. (2018). "From resource extraction to outflows of wastes and emissions: The socioeconomic metabolism of the global economy, 1900–2015." Global Environmental Change.
- Global Carbon Project (2024). Global Carbon Budget.
- Bolt, J. & van Zanden, J.L. (2024). "Maddison style estimates of the evolution of the world economy: A new 2023 update." Journal of Economic Surveys.
- UNEP (2024). Global Material Flows Database.

## Generated
- **Date**: 2025-07-03
- **Project**: Future Pathways - Empirical Civilization Attractor Analysis
- **Repository**: https://github.com/bernardSolar/future_pathways
- **Contact**: bernard@solarnautics.org

## Previous Analysis Results (1995-2024 subset)
Using a limited 7-point subset, we found empirically-derived parameters:
- σ ≈ 0.021 (emissions response rate)
- ρ ≈ 4.75 (critical growth threshold)  
- β ≈ variable (growth damping - poor fit)

The expanded 55-point dataset should provide much more robust parameter estimates and reveal longer-term dynamics not visible in the smaller sample.
