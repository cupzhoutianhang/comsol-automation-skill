---
name: comsol-automated-modeling
description: Complete COMSOL Multiphysics automation solution for end-to-end simulation workflows from parameter definition to result analysis. Developed by Zhou Tianhang, China University of Petroleum (Beijing). Automatically creates models, configures physics, generates code, runs batch simulations, processes results, and supports MATLAB, Java, and Python COMSOL APIs. Use when needing to automate parameter studies, multi-parameter sweeps, design optimization, batch processing, API integration, or post-processing analysis.
---

# COMSOL Automated Modeling

## Overview

This skill provides a complete automation solution for COMSOL Multiphysics simulations, enabling end-to-end workflows from parameter definition to result analysis. It transforms manual COMSOL workflows into scalable, automated processes suitable for design optimization, parameter studies, and batch processing.

## Core Capabilities

### 1. Parameter Management
- **Input Validation**: Comprehensive parameter validation with type checking and constraint verification
- **Configuration Handling**: JSON-based configuration system for all simulation parameters
- **Template System**: Pre-built templates for common simulation types
- **Dynamic Generation**: Programmatic parameter creation and modification

### 2. Automated Model Creation
- **Code Generation**: Automatic generation of Java and MATLAB code for COMSOL API
- **Multi-Physics Support**: Built-in support for electromagnetics, heat transfer, fluid dynamics, structural mechanics, and chemical transport
- **Geometry Automation**: Automated geometry creation with validation
- **Mesh Configuration**: Intelligent mesh generation with size optimization

### 3. Batch Simulation Execution
- **Batch Processing**: Run multiple simulations in automated sequence
- **Parameter Sweeps**: Automated parameter variation studies
- **Error Handling**: Robust error detection and recovery mechanisms
- **Resource Management**: Memory and CPU optimization for large-scale studies

### 4. Result Processing & Analysis
- **Automated Extraction**: Extract key results and metrics automatically
- **Data Analysis**: Statistical analysis and trend identification
- **Report Generation**: Automated summary reports with visualizations
- **Comparative Studies**: Cross-simulation result comparison

### 5. Multi-API Integration
- **Java API**: Direct COMSOL Java API integration
- **MATLAB API**: LiveLink for MATLAB automation
- **Python Integration**: Python wrapper support for COMSOL operations
- **Batch Mode**: Command-line batch processing support

## Quick Start

### Basic Usage Pattern

1. **Define your simulation parameters** in a JSON configuration file:
```json
{
  "model_name": "thermal_analysis",
  "geometry": {
    "type": "rectangle",
    "dimensions": [10, 5, 2]
  },
  "physics": ["heat_transfer"],
  "parameters": {
    "temperature": {
      "value": 293.15,
      "unit": "K",
      "description": "Initial temperature"
    }
  }
}
```

2. **Generate the COMSOL model** using the automation scripts:
```bash
python3 scripts/model_creator.py config.json java
```

3. **Run the simulation** and analyze results:
```bash
python3 scripts/simulation_runner.py batch generated_model.mph results
python3 scripts/simulation_runner.py summary results
```

### Common Workflows

#### Single Simulation
```bash
# Validate parameters → Generate model → Run simulation → Analyze results
python3 scripts/parameter_handler.py config.json
python3 scripts/model_creator.py config.json java
python3 scripts/simulation_runner.py batch model.mph results
python3 scripts/simulation_runner.py summary results
```

#### Parameter Sweep
```bash
# Run parameter sweep over multiple values
python3 scripts/simulation_runner.py sweep config.json temperature temperatures.json sweep_results
```

#### Multi-Physics Analysis
```bash
# Define coupled physics (electrostatic + thermal)
physics": ["electrostatics", "heat_transfer"],
physics_coupling": {
  "electrostatic_heating": true
}
```

## Task Categories

### Category 1: Parameter Studies
For simulations requiring variation of input parameters:

**Triggers:**
- "Run parameter sweep for voltage 5V to 20V"
- "Optimize design by varying geometry parameters"
- "Study temperature effects on material properties"

**Workflow:**
1. Use `parameter_handler.py` to validate sweep parameters
2. Create parameter value arrays in JSON format
3. Execute `simulation_runner.py sweep` for automated variation
4. Analyze results using summary tools

**Example Request:**
```
"Perform a parameter sweep of heat flux from 1000 to 5000 W/m² in steps of 500, analyze the maximum temperature for each case"
```

### Category 2: Multi-Physics Simulations
For coupled physics problems:

**Triggers:**
- "Simulate electro-thermal coupling in power electronics"
- "Analyze fluid-structure interaction"
- "Model thermal-stress coupling"

**Workflow:**
1. Define coupled physics in configuration
2. Use `model_creator.py` to generate coupled model
3. Configure solver for multiphysics convergence
4. Extract coupled field results

**Example Request:**
```
"Create a coupled electrostatic-thermal simulation for a power resistor, with Joule heating feedback"
```

### Category 3: Design Optimization
For automated design improvement:

**Triggers:**
- "Find optimal geometry for minimum weight"
- "Optimize cooling channel layout for best thermal performance"
- "Design antenna for maximum radiation efficiency"

**Workflow:**
1. Define objective function in configuration
2. Set up parameter bounds and constraints
3. Use parameter sweep with result filtering
4. Extract optimal design parameters

**Example Request:**
```
"Optimize the thickness of a heat sink fin to minimize maximum temperature while constraining total mass"
```

### Category 4: Batch Processing & Scalability
For large-scale simulation studies:

**Triggers:**
- "Run 100 simulations with different random material properties"
- "Process simulation library results"
- "Automated quality checking of design space"

**Workflow:**
1. Create batch configuration files
2. Use parallel execution capabilities
3. Aggregate results across simulations
4. Generate comprehensive reports

**Example Request:**
```
"Process all simulation files in the design_library directory and create a performance comparison report"
```

### Category 5: API Integration & Code Generation
For programmatic COMSOL access:

**Triggers:**
- "Generate Java code for COMSOL automation"
- "Create MATLAB script for parameter study"
- "Export COMSOL model to different API format"

**Workflow:**
1. Provide configuration parameters
2. Use `model_creator.py` to generate desired API code
3. Customize generated code as needed
4. Integrate with existing workflows

**Example Request:**
```
"Generate MATLAB code for a thermal-structural coupling analysis with parameters for frequency sweep"
```

## Physics Support

### Electromagnetics
- **Electrostatics**: Electric field and potential analysis
- **Electric Currents**: Conduction and resistive heating
- **Magnetic Fields**: Static and time-varying magnetic field analysis
- **Wave Electromagnetics**: RF and microwave frequency analysis

### Heat Transfer
- **Conduction**: Steady-state and transient heat conduction
- **Convection**: Forced and natural convection cooling
- **Radiation**: Surface-to-surface radiation
- **Phase Change**: Melting and solidification

### Fluid Dynamics
- **Laminar Flow**: Low Reynolds number flows
- **Turbulent Flow**: High Reynolds number flows
- **Multiphase Flow**: Two-phase and multi-fluid systems
- **Heat Transfer in Fluids**: Conjugate heat transfer

### Structural Mechanics
- **Linear Elasticity**: Small deformation analysis
- **Nonlinear Materials**: Plasticity and hyperelasticity
- **Contact Analysis**: Surface interaction problems
- **Dynamic Analysis**: Modal and transient structural response

### Chemical Transport
- **Diffusion**: Mass transport in solids and fluids
- **Reaction Engineering**: Chemical kinetics
- **Electrochemistry**: Battery and fuel cell modeling
- **Multicomponent Transport**: Multi-species systems

## Scripts Overview

### parameter_handler.py
**Purpose**: Validate and process simulation parameters from JSON configuration files.

**Key Features**:
- Parameter validation with physics-specific checks
- Type conversion and unit handling
- Sample configuration generation
- Error reporting and suggestion system

**Usage**:
```bash
python3 parameter_handler.py config.json
python3 parameter_handler.py  # Creates sample config
```

### model_creator.py
**Purpose**: Generate COMSOL-compatible code (Java/MATLAB) from configuration.

**Key Features**:
- Multi-format code generation (Java, MATLAB)
- Automatic geometry and mesh setup
- Physics interface configuration
- Solver and study setup

**Usage**:
```bash
python3 model_creator.py config.json java
python3 model_creator.py config.json matlab
```

### simulation_runner.py
**Purpose**: Execute simulations and process results automatically.

**Key Features**:
- Batch simulation execution
- Parameter sweep automation
- Result extraction and analysis
- Summary report generation

**Usage**:
```bash
python3 simulation_runner.py batch model.mph results
python3 simulation_runner.py sweep config.json param values.json output
python3 simulation_runner.py summary results_dir
```

## Configuration Reference

### Required Fields
```json
{
  "model_name": "unique_model_identifier",
  "geometry": {
    "type": "rectangle|cylinder|sphere",
    "dimensions": [length, width, height]
  },
  "physics": ["physics_interface_1", "physics_interface_2"]
}
```

### Optional Fields
```json
{
  "mesh": {
    "element_size": "coarse|normal|fine",
    "refinement_level": 1-5
  },
  "solver": {
    "solver_type": "stationary|time_dependent|eigenfrequency",
    "relative_tolerance": 0.001,
    "absolute_tolerance": 0.001
  },
  "materials": {
    "domain": "material_name",
    "boundary": "material_name"
  },
  "boundary_conditions": {
    "type": "value",
    "selection": "boundary_tags"
  }
}
```

### Parameter Definition Format
```json
"parameters": {
  "parameter_name": {
    "value": number_or_string,
    "unit": "SI_unit_notation",
    "type": "float|int|string|boolean",
    "description": "human_readable_description"
  }
}
```

## Best Practices

### Performance Optimization
1. **Mesh Management**: Use appropriate mesh density - finer meshes increase accuracy but computation time
2. **Solver Selection**: Choose solver type based on problem physics (stationary vs time-dependent)
3. **Parameter Organization**: Group related parameters for easier management
4. **Result Storage**: Use structured output directories for easy result tracking

### Error Prevention
1. **Input Validation**: Always validate parameters before running simulations
2. **Geometry Checks**: Verify geometry topology before meshing
3. **Resource Monitoring**: Monitor memory and CPU usage during batch runs
4. **Backup Strategy**: Save intermediate results during long parameter sweeps

### Scalability Guidelines
1. **Small Studies** (<10 simulations): Use direct sequential execution
2. **Medium Studies** (10-100 simulations): Implement result caching
3. **Large Studies** (>100 simulations): Use parallel execution and distributed computing

## Integration Examples

### With MATLAB
```matlab
% Automated parameter study in MATLAB
config = loadjson('config.json');
results = struct();

for voltage = 5:5:25
    config.parameters.voltage.value = voltage;
    savejson('', config, 'temp_config.json');
    
    system('python3 ../scripts/model_creator.py temp_config.json matlab');
    system('python3 ../scripts/simulation_runner.py batch temp_model.mph temp_results');
    
    results.(['V', num2str(voltage)]) = load_results('temp_results');
end
```

### With Python Scientific Stack
```python
import pandas as pd
import matplotlib.pyplot as plt
from simulation_runner import COMSOLSimulationRunner

# Automated design space exploration
design_points = []
runner = COMSOLSimulationRunner()

for thickness in [0.001, 0.002, 0.005]:
    for conductivity in [100, 200, 400]:
        config = create_config(thickness, conductivity)
        results = runner.run_batch_simulation(generate_model(config))
        design_points.append({
            'thickness': thickness,
            'conductivity': conductivity,
            'max_temperature': results['max_temp']
        })

df = pd.DataFrame(design_points)
df.plot.scatter(x='thickness', y='conductivity', c='max_temperature')
plt.show()
```

### With Jupyter Notebooks
```python
# Interactive parameter study
from ipywidgets import interact
import matplotlib.pyplot as plt

def study_parameter(frequency=1e6, voltage=12):
    config = create_frequency_domain_config(frequency, voltage)
    results = run_automated_simulation(config)
    
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(results['electric_field'])
    plt.title('Electric Field Distribution')
    
    plt.subplot(1, 2, 2)
    plt.imshow(results['power_density'])
    plt.title('Power Density')
    plt.show()

interact(study_parameter, frequency=(1e3, 1e9, 1e6), voltage=(1, 50, 1))
```

## Workflow Organization

### Basic Directory Structure
```
project_directory/
├── config/                    # Configuration files
│   ├── base_config.json      # Base simulation parameters
│   ├── parameter_sweeps/     # Parameter sweep definitions
│   └── templates/           # Reusable config templates
├── models/                   # Generated COMSOL models
│   ├── java/                # Java API code
│   ├── matlab/              # MATLAB API code
│   └── mph/                 # COMSOL model files
├── results/                  # Simulation outputs
│   ├── single_runs/         # Individual simulation results
│   ├── parameter_sweeps/    # Sweep study results
│   └── summaries/           # Analysis and reports
├── scripts/                  # Automation scripts (from skill)
└── analysis/                 # Post-processing scripts
```

### Resource Management

1. **Temporary Files**: Clean up intermediate files after successful runs
2. **Cache Management**: Use hash-based caching for repeated studies
3. **Log Rotation**: Implement log file rotation for long-running processes
4. **Backup Strategy**: Version control for configuration files

## References and Extended Documentation

### API Documentation
See [comsol_api_reference.md](references/comsol_api_reference.md) for comprehensive COMSOL API reference including:
- Java API examples and syntax
- MATLAB API integration patterns
- Python API usage guidelines
- Batch mode configuration options
- Performance optimization tips

### Workflow Guide
See [workflow_guide.md](references/workflow_guide.md) for detailed workflows including:
- Step-by-step implementation guides
- Decision trees for workflow selection
- Template configurations for common problems
- Error handling and debugging strategies
- Integration patterns with external tools

### Common Issues and Solutions
- **COMSOL Installation**: Ensure COMSOL is installed and COMSOL_PATH environment variable is set
- **Java/MATLAB Configuration**: Verify API compatibility and license availability
- **Memory Management**: Adjust JVM heap size for large models
- **Solver Convergence**: Use appropriate tolerances and solver settings for problem physics