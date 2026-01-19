# COMSOL API Reference

This reference provides information about COMSOL Multiphysics API and how to use it with the automation scripts in this skill.

## COMSOL API Overview

COMSOL Multiphysics provides several APIs for automation:

1. **Java API** - Direct programming interface with COMSOL
2. **MATLAB API (LiveLink)** - Integration with MATLAB environment  
3. **Python API** - Available through COMSOL 5.6+
4. **COMSOL Server API** - For COMSOL Server deployments

## Supported Physics Interfaces

### Electromagnetics
- `Electrostatics` - "es"
- `Electric Currents` - "ec" 
- `Magnetic Fields` - "mf"
- `Wave Electromagnetics` - "we"

### Heat Transfer
- `Heat Transfer in Solids` - "ht"
- `Heat Transfer in Fluids` - "ht"
- `Thermal Radiation` - "tr"

### Fluid Dynamics
- `Laminar Flow` - "spf"
- `Turbulent Flow` - "turb"
- `Multiphase Flow` - "tpf"

### Structural Mechanics
- `Solid Mechanics` - "solid"
- `Beam` - "beam"
- `Shell` - "shell"

### Chemical Transport
- `Transport of Diluted Species` - "tds"
- `Reaction Engineering` - "re"

## Java API Reference

### Core Model Methods

```java
// Create a new model
Model model = ModelUtil.create("ModelName");

// Load existing model
Model model = ModelUtil.load("path/to/model.mph");

// Save model
ModelUtil.save(model, "path/to/save.mph");
```

### Geometry Creation

```java
// Create 3D component
model.component().create("comp1", true);
model.component("comp1").geom().create("geom1", 3);

// Add geometry primitives
model.component("comp1").geom("geom1").create("blk1", "Block");
model.component("comp1").geom("geom1").feature("blk1").set("size", new double[]{1.0, 1.0, 1.0});

model.component("comp1").geom("geom1").create("cyl1", "Cylinder");
model.component("comp1").geom("geom1").feature("cyl1").set("r", 0.5);
model.component("comp1").geom("geom1").feature("cyl1").set("h", 2.0);

// Build geometry
model.component("comp1").geom("geom1").run();
```

### Mesh Generation

```java
// Create mesh
model.component("comp1").mesh().create("mesh1");

// Automatic mesh with different sizes
model.component("comp1").mesh("mesh1").automatic(true, "coarse");
model.component("comp1").mesh("mesh1").automatic(true, "normal"); 
model.component("comp1").mesh("mesh1").automatic(true, "fine");

// Manual mesh settings
model.component("comp1").mesh("geom1").feature("size").set("hauto", 3); // 1-9 scale
```

### Physics Setup

```java
// Electrostatics
model.component("comp1").physics().create("es1", "Electrostatics", "geom1");
model.component("comp1").physics("es1").create("pot1", "Pointwise", 2);
model.component("comp1").physics("es1").feature("pot1").selection().all();

// Heat Transfer
model.component("comp1").physics().create("ht1", "HeatTransfer", "geom1");
model.component("comp1").physics("ht1").create("init1", "Init", "geom1");
model.component("comp1").physics("ht1").feature("init1").selection().all();

// Laminar Flow
model.component("comp1").physics().create("spf1", "LaminarFlow", "geom1");
model.component("comp1").physics("spf1").create("init1", "Init", "geom1");
model.component("comp1").physics("spf1").feature("init1").selection().all();
```

### Study Configuration

```java
// Stationary study
model.study().create("std1");
model.study("std1").create("stat", "Stationary");

// Time-dependent study
model.study("std1").create("time", "Time");
model.study("std1").feature("time").set("tlist", "range(0,0.1,10)");

// Eigenfrequency study
model.study("std1").create("eig", "Eigenfrequency");

// Parametric sweep
model.study("std1").create("param", "Parametric");
model.study("std1").feature("param").set("pname", new String[]{"p1"});
model.study("std1").feature("param").set("plistarr", new String[]{"1 2 3"});
```

### Solver Configuration

```java
// Create solver
model.sol().create("sol1");
model.sol("sol1").study("std1");
model.sol("sol1").attach("std1");

// Set solver options
model.sol("sol1").feature("s1").set("rtol", 0.001);
model.sol("sol1").feature("s1").set("atol", 0.001);

// Run solution
model.sol("sol1").run();
```

## MATLAB API Reference

### Basic Setup

```matlab
% Add COMSOL to path
addpath('/path/to/comsol56/multiphysics/matlablive');

% Start COMSOL server
mphstart;

% Load or create model
model = mphload('model.mph');
% OR
model = ModelUtil.create('Model1');
```

### Model Operations

```matlab
% Set parameters
model.param.set('frequency', '1000[Hz]');
model.param.set('voltage', '12[V]');
model.param.set('temperature', '293.15[K]');

% Build geometry
model.component('comp1').geom('geom1').run();

% Build mesh
model.component('comp1').mesh('mesh1').run();

% Solve
model.sol('sol1').run();

% Get results
T = mphglobal(model, 'T'); % Temperature
V = mphglobal(model, 'V'); % Electric potential
```

### Common Workflows

#### Parameter Sweep Example
```matlab
frequencies = [100, 500, 1000, 5000];
results = zeros(size(frequencies));

for i = 1:length(frequencies)
    model.param.set('frequency', [num2str(frequencies(i)) '[Hz]']);
    model.sol('sol1').run();
    results(i) = mphglobal(model, 'T_max');
end
```

## Batch Mode Operations

### Command Line Usage
```bash
# Windows
"C:\Program Files\COMSOL\COMSOL56\Multiphysics\bin\comsol.bat" batch -inputfile script.mph

# Linux/Mac
/usr/local/comsol56/multiphysics/bin/comsol batch -inputfile script.mph
```

### COMSOL Server
```bash
# Start server
comsol server start

# Submit job
comsol batch -server localhost:2036 -inputfile script.mph
```

## Performance Tips

1. **Mesh Optimization** - Use appropriate mesh sizing for accuracy vs performance
2. **Memory Management** - Clear unused models and results regularly
3. **Parallel Processing** - Utilize `mpiexec` for distributed computing
4. **Parameter Studies** - Leverage COMSOL's built-in parametric solver
5. **Batch Processing** - Use batch mode for automated workflows

## Troubleshooting

### Common Issues
- **"No JVM found"**: Set `JAVA_HOME` environment variable
- **"Port already in use"**: Find and kill existing COMSOL processes
- **Memory issues**: Increase Java heap space with `-Xmx` JVM option
- **Geometry errors**: Validate geometry before meshing operations