# COMSOL Automation Skill - Usage Guide

## Overview

The COMSOL Automation Skill, developed by Zhou Tianhang at China University of Petroleum (Beijing), provides a comprehensive solution for automating COMSOL Multiphysics simulations, from parameter definition to result analysis. This guide covers all aspects of using the skill effectively.

## Installation

### Prerequisites

1. **COMSOL Multiphysics 6.0+** installed and properly licensed
2. **Python 3.8+** with required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. **COMSOL Server** configured (for headless operation)

### Quick Setup

```bash
# Clone the repository
git clone <repository-url>
cd comsol-automation-skill

# Install dependencies
pip install -r requirements.txt

# Test the installation
python skills/comsol-automated-modeling/scripts/batch_demo.py
```

## Basic Usage

### 1. Parameter Configuration

Create a JSON configuration file defining your simulation parameters:

```json
{
  "model_name": "my_simulation",
  "template_file": "/path/to/template.mph",
  "output_directory": "/path/to/output",
  "parameters": {
    "length": {"values": [0.01, 0.02, 0.05], "unit": "m"},
    "width": {"values": [0.005, 0.01], "unit": "m"}
  }
}
```

### 2. Running Single Simulations

Use the parameter handler for single simulations:

```python
from skills.comsol_automated_modeling.scripts.parameter_handler import ParameterValidator

validator = ParameterValidator()
result = validator.validate_parameters(config_data)
if result.is_valid:
    # Proceed with simulation
    pass
```

### 3. Batch Simulations

Use the batch generator for multiple simulations:

```bash
python skills/comsol_automated_modeling/scripts/batch_generator_fixed.py examples/interdigitated_flow_batch.json
```

### 4. API Code Generation

Generate COMSOL API code automatically:

```python
from skills.comsol_automated_modeling.scripts.model_creator import COMSOLModelCreator

creator = COMSOLModelCreator()
java_code = creator.generate_java_code(config)
matlab_code = creator.generate_matlab_code(config)
```

## Advanced Features

### Parameter Sweeping

Configure automated parameter sweeps in your JSON config:

```json
{
  "parameter_sweep": {
    "enabled": true,
    "parameters": ["temperature", "pressure"],
    "output_type": "all_combinations",
    "filter_conditions": "temperature > 300 && pressure < 1000"
  }
}
```

### Filtering and Constraints

Apply constraints to parameter combinations:

```json
{
  "filter_conditions": "length * width > 0.0001 && thickness < 0.01"
}
```

### Result Processing

Automatic result extraction and analysis:

```python
from skills.comsol_automated_modeling.scripts.simulation_runner import ResultProcessor

processor = ResultProcessor()
report = processor.generate_summary_report(simulation_results)
```

## Configuration Reference

### Model Configuration

- **model_name**: Unique identifier for the simulation
- **template_file**: Path to COMSOL template (.mph file)
- **output_directory**: Where to save results
- **api_type**: "python", "java", or "matlab"

### Parameter Definition

```json
"parameter_name": {
  "values": [1, 2, 3],
  "min": 0,
  "max": 10,
  "step": 0.5,
  "unit": "m"
}
```

### Physics Configuration

```json
"physics": {
  "modules": ["HeatTransfer", "SolidMechanics"],
  "boundary_conditions": {
    "temperature": {"type": "fixed", "value": 300}
  }
}
```

### Solver Settings

```json
"solver": {
  "type": "stationary",
  "tolerance": 1e-6,
  "max_iterations": 100
}
```

## Examples

### Basic Heat Transfer Simulation

See `examples/interdigitated_flow_batch.json` for a complete example of thermal simulation setup.

### Parameter Sweep Study

See `examples/parameter_sweep_demo.json` for automated parameter variation studies.

### Electro-Thermal Coupling

See `examples/test_batch_config.json` for multi-physics coupling examples.

## Troubleshooting

### Common Issues

1. **COMSOL Connection Failed**: Ensure COMSOL Server is running and accessible
2. **License Error**: Verify COMSOL license is valid and available
3. **Memory Issues**: Reduce batch size or concurrent simulations
4. **File Permissions**: Ensure write access to output directories

### Debug Mode

Enable verbose logging:

```json
"logging": {
  "level": "DEBUG",
  "file": "debug.log",
  "console_output": true
}
```

## Performance Tips

1. **Use Templates**: Pre-configured templates speed up model creation
2. **Batch Processing**: Group simulations to reduce overhead
3. **Parallel Execution**: Use multiple COMSOL instances for large batches
4. **Memory Management**: Close models after processing to free memory
5. **Disk Space**: Monitor output directory size for large parameter studies

## Best Practices

1. **Test Configurations**: Validate JSON configs before running large batches
2. **Incremental Testing**: Start with small parameter sets
3. **Backup Results**: Regularly backup important simulation results
4. **Version Control**: Track configuration changes in version control
5. **Documentation**: Document simulation setups and parameters

## Support

For additional help:

- Check the [API Reference](API_REFERENCE.md)
- Review [Contribution Guidelines](CONTRIBUTING.md)
- Open issues on the project repository
- Consult COMSOL documentation for physics-specific questions