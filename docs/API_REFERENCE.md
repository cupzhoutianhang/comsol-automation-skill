# COMSOL Automation API Reference

## Overview

This document provides detailed API reference for all classes and functions in the COMSOL Automation Skill developed by Zhou Tianhang at China University of Petroleum (Beijing).

## Core Classes

### COMSOLParameter

Data class representing a COMSOL simulation parameter.

```python
class COMSOLParameter:
    """Represents a single COMSOL simulation parameter."""
    
    name: str                    # Parameter name
    value: Union[float, int, str] # Parameter value
    unit: Optional[str]          # Physical unit
    parameter_type: str          # Variable type (float, int, string)
    description: Optional[str]   # Parameter description
    constraints: Optional[Dict]  # Parameter constraints
```

### ParameterValidator

Handles validation and processing of COMSOL parameters.

#### Methods

**validate_parameters(parameters: Dict) -> ValidationResult**

Validates a dictionary of parameters against COMSOL requirements.

Parameters:
- `parameters`: Dictionary of parameter definitions

Returns:
- `ValidationResult` object with validation status and messages

**generate_sample_inputs() -> List[Dict]**

Generates sample parameter configurations for testing.

Returns:
- List of sample parameter dictionaries

**apply_constraints(parameters: Dict, constraints: Dict) -> Dict**

Applies constraints to parameter values.

Parameters:
- `parameters`: Parameter dictionary
- `constraints`: Constraint definitions

Returns:
- Filtered parameter dictionary

### COMSOLModelCreator

Generates COMSOL API code for model creation.

#### Methods

**generate_java_code(config: Dict) -> str**

Generates Java code for COMSOL API.

Parameters:
- `config`: Model configuration dictionary

Returns:
- Java code as string

**generate_matlab_code(config: Dict) -> str**

Generates MATLAB code for COMSOL API.

Parameters:
- `config`: Model configuration dictionary

Returns:
- MATLAB code as string

**generate_python_code(config: Dict) -> str**

Generates Python code for COMSOL API.

Parameters:
- `config`: Model configuration dictionary  

Returns:
- Python code as string

### COMSOLSimulationRunner

Handles simulation execution and result processing.

#### Methods

**run_batch_simulation(config: Dict, parameters_list: List[Dict]) -> SimulationResult**

Runs multiple simulations in batch mode.

Parameters:
- `config`: Simulation configuration
- `parameters_list`: List of parameter dictionaries

Returns:
- `SimulationResult` containing all simulation results

**run_parameter_sweep(config: Dict) -> SimulationResult**

Runs automated parameter sweep study.

Parameters:
- `config`: Parameter sweep configuration

Returns:
- `SimulationResult` with sweep results

**export_results(results: SimulationResult, format: str) -> str**

Exports results in specified format.

Parameters:
- `results`: Simulation results
- `format`: Export format (csv, json, hdf5)

Returns:
- Path to exported file

### COMSOLBatchGenerator

Specialized class for batch model generation.

#### Methods

**load_config(config_file: str) -> Dict**

Loads configuration from JSON file.

Parameters:
- `config_file`: Path to configuration file

Returns:
- Configuration dictionary

**generate_parameter_combinations(parameters: Dict) -> List[Dict]**

Generates all parameter combinations.

Parameters:
- `parameters`: Parameter definitions

Returns:
- List of parameter combination dictionaries

**_apply_filtering(combinations: List[Dict], conditions: str) -> List[Dict]**

Applies filtering conditions to parameter combinations.

Parameters:
- `combinations`: List of parameter combinations
- `conditions`: Filter condition string

Returns:
- Filtered list of combinations

**setup_parameters_in_model(model, parameters: Dict) -> bool**

Sets parameters in COMSOL model.

Parameters:
- `model`: COMSOL model object
- `parameters`: Parameter dictionary

Returns:
- Success status boolean

**generate_all_models() -> List[str]**

Generates all models according to configuration.

Returns:
- List of generated model file paths

### ResultProcessor

Processes and analyzes simulation results.

#### Methods

**generate_summary_report(results: SimulationResult) -> str**

Generates comprehensive summary report.

Parameters:
- `results`: Simulation results

Returns:
- Report content as string

**extract_numerical_data(results: SimulationResult, variables: List[str]) -> pd.DataFrame**

Extracts numerical data for specified variables.

Parameters:
- `results`: Simulation results
- `variables`: List of variable names

Returns:
- Pandas DataFrame with extracted data

**create_visualization(results: SimulationResult, plot_type: str) -> str**

Creates visualization of results.

Parameters:
- `results`: Simulation results
- `plot_type`: Type of plot to generate

Returns:
- Path to generated plot file

## Configuration Schemas

### Main Configuration Schema

```json
{
  "type": "object",
  "properties": {
    "model_name": {"type": "string"},
    "template_file": {"type": "string"},
    "output_directory": {"type": "string"},
    "api_type": {"type": "string", "enum": ["python", "java", "matlab"]},
    "geometry": {"$ref": "#/definitions/geometry"},
    "physics": {"$ref": "#/definitions/physics"},
    "mesh": {"$ref": "#/definitions/mesh"},
    "solver": {"$ref": "#/definitions/solver"},
    "parameter_sweep": {"$ref": "#/definitions/parameter_sweep"},
    "results": {"$ref": "#/definitions/results"},
    "batch_settings": {"$ref": "#/definitions/batch_settings"}
  },
  "required": ["model_name", "output_directory"]
}
```

### Parameter Definition Schema

```json
{
  "type": "object",
  "properties": {
    "values": {"type": "array"},
    "min": {"type": "number"},
    "max": {"type": "number"},
    "step": {"type": "number"},
    "unit": {"type": "string"}
  }
}
```

## Error Handling

### ValidationResult

```python
class ValidationResult:
    """Result of parameter validation."""
    
    is_valid: bool              # Whether validation passed
    errors: List[str]           # List of error messages
    warnings: List[str]         # List of warning messages
    validated_parameters: Dict  # Cleaned parameter dictionary
```

### SimulationResult

```python
class SimulationResult:
    """Container for simulation results."""
    
    success: bool               # Overall success status
    model_files: List[str]      # Generated model file paths
    execution_time: float       # Total execution time
    results_data: Dict          # Numerical results
    error_log: List[str]        # Error messages
    metadata: Dict              # Additional metadata
```

## Exception Classes

### COMSOLError

Base exception for all COMSOL-related errors.

### ValidationError

Raised when parameter validation fails.

### ModelCreationError

Raised when model creation fails.

### SimulationError

Raised when simulation execution fails.

### ConfigurationError

Raised when configuration is invalid.

## Utility Functions

### File Operations

**save_json_config(config: Dict, filepath: str) -> bool**

Saves configuration to JSON file.

**load_json_config(filepath: str) -> Dict**

Loads configuration from JSON file.

**validate_config_schema(config: Dict) -> bool**

Validates configuration against schema.

### Code Generation Helpers

**format_java_string(text: str) -> str**

Formats string for Java code generation.

**format_matlab_string(text: str) -> str**

Formats string for MATLAB code generation.

**indent_code(code: str, levels: int) -> str**

Indents code by specified number of levels.

## Example Usage

### Basic Parameter Validation

```python
from skills.comsol_automated_modeling.scripts.parameter_handler import ParameterValidator

validator = ParameterValidator()
config = {
    "length": {"values": [0.01, 0.02], "unit": "m"},
    "temperature": {"values": [300, 350], "unit": "K"}
}

result = validator.validate_parameters(config)
if result.is_valid:
    print("Parameters validated successfully")
else:
    print(f"Validation errors: {result.errors}")
```

### Batch Simulation

```python
from skills.comsol_automated_modeling.scripts.batch_generator_fixed import COMSOLBatchGenerator

generator = COMSOLBatchGenerator("config.json")
generator.generate_all_models()
```

### Result Processing

```python
from skills.comsol_automated_modeling.scripts.simulation_runner import ResultProcessor

processor = ResultProcessor()
report = processor.generate_summary_report(simulation_results)
with open("report.txt", "w") as f:
    f.write(report)
```

## Version Compatibility

- **COMSOL 6.0+**: Full feature support
- **COMSOL 5.6**: Limited Python API support
- **Python 3.8+**: Required
- **mph 1.0+**: Required for Python API