# COMSOL Automation Workflow Guide

This guide explains the end-to-end workflow for automating COMSOL simulations using the provided scripts and tools.

## Overview

The COMSOL automation workflow consists of four main stages:

1. **Parameter Definition** - Define simulation parameters and configuration
2. **Model Generation** - Create COMSOL models programmatically 
3. **Simulation Execution** - Run simulations in batch mode
4. **Results Processing** - Analyze and extract results

## Workflow Decision Tree

```
Start: User Request
    │
    ├── Are simulation parameters needed? ──Yes──→ Use parameter_handler.py
    │       │
    │       └── Create JSON configuration file
    │
    ├── What type of automation? 
    │       │
    │       ├── Single simulation ──→ Use model_creator.py + simulation_runner.py batch
    │       │
    │       ├── Parameter sweep ──→ Use simulation_runner.py sweep
    │       │
    │       ├── Optimization ──→ Use parameter sweep with custom objective function
    │       │
    │       └── Custom workflow ──→ Combine scripts as needed
    │
    └── Run and analyze results
```

## Step-by-Step Workflows

### Workflow 1: Single Simulation

#### Step 1: Define Parameters
Create a JSON configuration file:
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

#### Step 2: Validate Parameters
```bash
python3 scripts/parameter_handler.py config.json
```

#### Step 3: Generate Model Code
```bash
# Generate Java code for COMSOL
python3 scripts/model_creator.py config.json java

# OR generate MATLAB code
python3 scripts/model_creator.py config.json matlab
```

#### Step 4: Run Simulation
```bash
# Using MATLAB
matlab -batch "addpath('path/to/comsol'); mphstart; model = mphload('generated_model.mph'); model.sol('sol1').run(); mphsave(model, 'results/solved_model.mph'); exit;"

# Using batch mode
python3 scripts/simulation_runner.py batch generated_model.mph results
```

#### Step 5: Analyze Results
```bash
python3 scripts/simulation_runner.py summary results
```

### Workflow 2: Parameter Sweep

#### Step 1: Create Base Configuration
Create a base configuration file as in Workflow 1.

#### Step 2: Define Parameter Sweep Values
Create a file `sweep_values.json`:
```json
[100, 200, 300, 400, 500]
```

#### Step 3: Run Parameter Sweep
```bash
python3 scripts/simulation_runner.py sweep config.json heat_flux sweep_values.json parameter_sweep_results
```

#### Step 4: Analyze Results
The sweep will generate:
- Individual result directories for each parameter value
- Summary file: `parameter_sweep_summary.json`
- Individual result files and model files

### Workflow 3: Geometry Variation

#### Step 1: Create Configuration Template
```json
{
  "model_name": "geometry_study",
  "geometry": {
    "type": "cylinder",
    "radius": {"value": 1.0, "unit": "m"},
    "height": {"value": 2.0, "unit": "m"}
  },
  "physics": ["electrostatics"],
  "parameters": {
    "voltage": {"value": 12.0, "unit": "V"}
  }
}
```

#### Step 2: Generate Multiple Configurations
```python
import json

base_config = {...}  # Your base configuration

# Vary geometry parameters
for radius in [0.5, 1.0, 1.5, 2.0]:
    config = base_config.copy()
    config["geometry"]["radius"]["value"] = radius
    config["model_name"] = f"cylinder_r{radius}"
    
    with open(f"config_r{radius}.json", 'w') as f:
        json.dump(config, f, indent=2)
```

#### Step 3: Batch Process
```bash
for config in config_*.json; do
    echo "Processing $config"
    model_file=$(python3 scripts/model_creator.py $config | grep "Generated")
    python3 scripts/simulation_runner.py batch $model_file results_$(basename $config .json)
done
```

### Workflow 4: Multi-Physics Coupling

#### Step 1: Define Coupled Physics
```json
{
  "model_name": "multiphysics_analysis",
  "physics": ["electrostatics", "heat_transfer"],
  "physics_coupling": {
    "electrostatic_heating": true,
    "joule_heating": "es.Qrh"
  },
  "parameters": {
    "voltage": {"value": 12.0, "unit": "V"},
    "thermal_conductivity": {"value": 400, "unit": "W/(m·K"}
  }
}
```

#### Step 2: Configure Coupling in Generated Code
The model creator will automatically set up:
- Electrostatic heat source as input to thermal physics
- Temperature-dependent material properties
- Coupled solver settings

### Workflow 5: Design Optimization

#### Step 1: Define Objective Function
```python
def objective_function(results_dir):
    """Extract objective value from simulation results"""
    # Parse results and return objective value
    # Example: minimize maximum temperature
    with open(f"{results_dir}/solution_data.txt") as f:
        data = f.read()
    # Extract max temperature and return
    return max_temperature
```

#### Step 2: Set Up Optimization Loop
```python
import json
from simulation_runner import COMSOLSimulationRunner

runner = COMSOLSimulationRunner()
current_best = float('inf')
best_design = None

for design_param in design_space:
    # Update configuration
    config["parameters"]["design_variable"] = design_param
    
    # Generate and run simulation
    model_file = generate_model_from_config(config)
    results = runner.run_batch_simulation(model_file, f"results_{design_param}")
    
    # Evaluate objective
    objective_value = objective_function(f"results_{design_param}")
    
    if objective_value < current_best:
        current_best = objective_value
        best_design = design_param
```

## Workflow Templates

### Template 1: Thermal Analysis
```json
{
  "$template": "thermal_analysis",
  "geometry": {
    "type": "rectangle",
    "dimensions": "{{dimensions}}"
  },
  "physics": ["heat_transfer"],
  "boundary_conditions": {
    "heating_power": "{{heating_power}}",
    "ambient_temperature": "{{ambient_temp}}"
  }
}
```

### Template 2: Structural Analysis
```json
{
  "$template": "structural_analysis",
  "geometry": {
    "type": "beam",
    "length": "{{length}}",
    "cross_section": "{{cross_section}}"
  },
  "physics": ["structural_mechanics"],
  "boundary_conditions": {
    "load": "{{applied_load}}",
    "constraints": "{{constraints}}"
  }
}
```

### Template 3: Electromagnetic Analysis
```json
{
  "$template": "electromagnetic_analysis",
  "geometry": {
    "type": "rectangle",
    "dimensions": "{{coil_dimensions}}"
  },
  "physics": ["electric_currents"],
  "parameters": {
    "frequency": "{{frequency}}",
    "current": "{{current}}"
  }
}
```

## Error Handling and Debugging

### Common Issues

1. **Parameter Validation Errors**
   - Check parameter types and units
   - Verify required parameters are present
   - Ensure numerical values are within valid ranges

2. **Geometry Creation Failures**
   - Validate geometry parameters (positive dimensions)
   - Check geometry topology
   - Verify mesh compatibility

3. **Solver Convergence Issues**
   ```bash
   # Check solver logs
   cat results/solver.log
   
   # Adjust tolerances if needed
   "solver": {
     "relative_tolerance": 0.01,  # Increase for faster convergence
     "absolute_tolerance": 0.001
   }
   ```

4. **Memory Issues**
   ```bash
   # Increase Java heap space for COMSOL
   export JVM_ARGS="-Xmx8g"
   ```

### Debugging Commands

```bash
# Validate configuration
python3 scripts/parameter_handler.py config.json

# Generate model with verbose output
python3 scripts/model_creator.py config.json --verbose

# Run simulation with debug logging
python3 scripts/simulation_runner.py batch model.mph --debug

# Check COMSOL installation
which comsol
comsol --version
```

## Performance Optimization

### Parallel Execution
```bash
# Run multiple simulations in parallel
gnu_parallel -j 4 'python3 scripts/simulation_runner.py batch {} results_{/}' ::: models/*.mph
```

### Resource Management
```bash
# Limit memory usage
ulimit -v 8000000  # 8GB virtual memory

# Set number of cores
export COMSOL_NUM_THREADS=4
```

### Result Caching
```python
# Store and retrieve previous results
import pickle
import hashlib

def get_config_hash(config):
    return hashlib.md5(json.dumps(config, sort_keys=True).encode()).hexdigest()

config_hash = get_config_hash(config)
cache_file = f"cache/{config_hash}.pkl"

if os.path.exists(cache_file):
    with open(cache_file, 'rb') as f:
        results = pickle.load(f)
else:
    results = run_simulation(config)
    with open(cache_file, 'wb') as f:
        pickle.dump(results, f)
```

## Integration with Other Tools

### MATLAB Integration
```matlab
% Call COMSOL automation from MATLAB
system('python3 scripts/parameter_handler.py config.json');
system('python3 scripts/model_creator.py config.json matlab');

% Load and post-process results
results = load('results/solution_data.txt');
```

### Python Integration
```python
from subprocess import run
import json

# Run automation scripts
result = run(['python3', 'scripts/parameter_handler.py', 'config.json'], 
            capture_output=True, text=True)

# Process results
with open('results/output.json') as f:
    simulation_results = json.load(f)
```

## Best Practices

1. **Configuration Management**
   - Use version control for configuration files
   - Document parameter meanings and units
   - Include validation ranges in comments

2. **Error Handling**
   - Always validate inputs before running simulations
   - Implement timeout mechanisms for long-running jobs
   - Log errors and warnings systematically

3. **Resource Efficiency**
   - Use appropriate mesh refinement levels
   - Implement result caching for repeated studies
   - Clean up temporary files and models

4. **Reproducibility**
   - Store complete configuration with results
   - Document version numbers of tools and COMSOL
   - Keep log files for debugging

5. **Scalability**
   - Use batch processing for large studies
   - Implement parallel execution where possible
   - Monitor resource usage during execution