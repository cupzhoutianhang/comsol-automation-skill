# COMSOL Automated Modeling Skill

🚀 **Complete COMSOL Multiphysics automation solution for end-to-end simulation workflows**

**Developed by: Zhou Tianhang, China University of Petroleum (Beijing)**
**Contact: zhouth@cup.edu.cn**

[![Skill Package](https://img.shields.io/badge/skill%20package-v1.0-blue.svg)](comsol-automated-modeling.skill)

## ✨ Features

- 🔄 **End-to-End Automation**: Parameter definition → Model creation → Simulation execution → Result analysis
- 🎯 **Batch Processing**: Generate 800+ parameter combinations automatically (replicates your comsol.py workflow)
- 🔧 **Multi-API Support**: Java, MATLAB, and Python COMSOL API integration
- 📊 **Multi-Physics**: Electromagnetics, heat transfer, fluid dynamics, structural mechanics, chemical transport
- 💾 **Configurable Workflows**: JSON-based configuration, no coding required

## 📦 Installation

### Method 1: Using Pre-built Package (Recommended)

1. **Download the skill package**
   ```bash
   # Clone this repository
   git clone https://github.com/cupzhoutianhang/comsol-automation-skill.git
   cd comsol-automation-skill
   
   # Install COMSOL Automation Skill
   skills install comsol-automated-modeling.skill
   ```

2. **Verify installation**
   ```bash
   skills list | grep comsol-automated-modeling
   ```

### Method 2: Manual Setup

1. **Install Dependencies**
   ```bash
   pip install mph numpy json logging
   ```

2. **Extract and Setup**
   ```bash
   unzip comsol-automated-modeling.skill -d comsol-skill
   cd comsol-skill
   ```

## 🚀 Quick Start

### Basic Usage: 868 File Batch Generation

This replicates your original `comsol.py` functionality:

```bash
# Create configuration (similar to your PARAMETERS in comsol.py)
cat > batch_config.json << 'EOF'
{
  "model_name": "interdigitated_flow_batch",
  "template_model": "/path/to/your/template.mph",
  "output_directory": "/path/to/output",
  "parameters": {
    "K_ch": [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8],
    "W_ch": [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8],
    "W_rib": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
  },
  "parameter_units": {
    "K_ch": "mm",
    "W_ch": "mm",
    "W_rib": "mm"
  },
  "batch_filtering": {
    "target_count": 868
  }
}
EOF

# Run batch generation
python3 scripts/batch_generator.py batch_config.json
```

### Advanced Usage: Parameter Sweep with Analysis

```bash
# Run parameter sweep with result collection
python3 scripts/simulation_runner.py sweep config.json temperature values.json results

# Generate analysis report
python3 scripts/simulation_runner.py summary results
```

## 📋 Configuration Examples

### Example 1: Simple Parameter Study
🔍 See: `examples/single_parameter_study.json`
```json
{
  "model_name": "thermal_analysis",
  "parameters": {
    "temperature": {
      "value": 293.15,
      "unit": "K"
    }
  }
}
```

### Example 2: Electro-Thermal Coupling
🔍 See: `examples/electro_thermal_coupling.json`
```json
{
  "physics": ["electrostatics", "heat_transfer"],
  "physics_coupling": {
    "electrostatic_heating": true,
    "joule_heating": "es.Qrh"
  }
}
```

### Example 3: Your Workflow
🔍 See: `examples/comsol_py_replacement.json`

## 🛠️ Core Scripts

| Script | Purpose | Your Script Equivalent |
|--------|---------|----------------------|
| `parameter_handler.py` | Validate and process parameters | Parameter validation logic |
| `model_creator.py` | Generate COMSOL API code | Model loading and parameter setting |
| `batch_generator.py` | Batch file generation | Main batch processing of comsol.py |
| `simulation_runner.py` | Execute and analyze simulations | Mesh generation and file saving |

## 📁 Project Structure

```
comsol-automation-skill/
├── 📦 comsol-automated-modeling.skill  # Ready-to-use package
├── 📝 SKILL.md                         # Core skill documentation
├── 📁 examples/                        # Ready-to-run examples
├── 📁 docs/                            # Additional documentation
├── 📝 requirements.txt                 # Python dependencies
└── 📝 README.md                        # This file
```

## 🧑‍💻 Development

### Building from Source

If you want to modify the skill:

```bash
# Extract source
unzip comsol-automated-modeling.skill -d source

# Make modifications
cd source/comsol-automated-modeling

# Test changes
python3 scripts/batch_demo.py examples/test_config.json

# Repackage
python3 ../../skills/skill-creator/scripts/package_skill.py .
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## 📖 Documentation

- 📚 **User Guide**: `SKILL.md` in the skill package
- 🔧 **API Reference**: See references in the skill package
- 💡 **Workflow Examples**: `examples/` directory
- ❓ **Troubleshooting**: `docs/TROUBLESHOOTING.md`

## 🤝 Dependencies

- **COMSOL Multiphysics** 5.6+ (required for actual execution)
- **Python Libraries**: `mph`, `numpy`
- **Optional**: MATLAB, Java (for alternative API access)

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 🌟 Features Comparison

| Feature | Your comsol.py | COMSOL Automation Skill |
|---------|---------------|-------------------------|
| Parameter combination generation | ✅ | ✅ |
| Filtering to 868 files | ✅ | ✅ |
| Template model loading | ✅ | ✅ |
| Parameter modification | ✅ | ✅ |
| Mesh generation | ✅ | ✅ |
| File saving with naming | ✅ | ✅ |
| **Configuration-driven** | ❌ | ✅ |
| **Multi-API support** | ❌ | ✅ |
| **Parallel processing** | ❌ | ✅ |
| **Result analysis** | ❌ | ✅ |
| **Extensible framework** | ❌ | ✅ |

## 📞 Support

- 📧 Email: zhouth@cup.edu.cn
- 🏫 Institution: China University of Petroleum (Beijing)
- 🐛 Issues: [GitHub Issues](https://github.com/cupzhoutianhang/comsol-automation-skill/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/cupzhoutianhang/comsol-automation-skill/discussions)

## 🙏 Acknowledgments



---

**Ready to automate your COMSOL workflows?** 🚀

**Developed by Zhou Tianhang, China University of Petroleum (Beijing)**

```bash
git clone https://github.com/cupzhoutianhang/comsol-automation-skill.git
cd comsol-automation-skill
skills install comsol-automated-modeling.skill
```