#!/usr/bin/env python3
"""
COMSOL Model Creator
Handles the creation of COMSOL models through the API
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional
from parameter_handler import COMSOLParameter, ParameterValidator


class COMSOLModelCreator:
    """Creates COMSOL models using the COMSOL API"""
    
    def __init__(self):
        self.model = None
        self.geometry = None
        self.mesh = None
        self.physics = {}
        self.study = None
        self.solver = None
        
    def generate_java_code(self, parameters: Dict[str, COMSOLParameter], 
                          config: Dict[str, Any]) -> str:
        """Generate Java code for COMSOL API"""
        java_code = []
        java_code.append("import com.comsol.model.*;")
        java_code.append("import com.comsol.model.util.*;")
        java_code.append("")
        java_code.append(f"public class {config.get('model_name', 'GeneratedModel')} {{")
        java_code.append("    public static Model run() {")
        java_code.append("        Model model = ModelUtil.create(\"Model1\");")
        java_code.append("")
        
        # Add parameters
        if "parameters" in parameters:
            java_code.append("        // Define parameters")
            for name, param in parameters.items():
                if name != "parameters":  # Skip the parameters group
                    java_code.append(f"        model.param().set(\"{name}\", \"{param.to_comsol_string()}\");")
                        
            # Handle nested parameters
            if "parameters" in parameters and isinstance(parameters["parameters"].value, dict):
                for name, value in parameters["parameters"].value.items():
                    if isinstance(value, dict):
                        param_val = value.get("value", "")
                        unit = value.get("unit", "")
                        java_code.append(f"        model.param().set(\"{name}\", \"{param_val}\");")
        
        java_code.append("")
        
        # Create geometry
        java_code.extend(self._generate_geometry_code(parameters, config))
        
        # Create mesh
        java_code.extend(self._generate_mesh_code(parameters, config))
        
        # Add physics
        java_code.extend(self._generate_physics_code(parameters, config))
        
        # Add study
        java_code.extend(self._generate_study_code(parameters, config))
        
        # Add solver
        java_code.extend(self._generate_solver_code(parameters, config))
        
        java_code.append("")
        java_code.append("        return model;")
        java_code.append("    }")
        java_code.append("}")
        
        return "\n".join(java_code)
    
    def _generate_geometry_code(self, parameters: Dict[str, COMSOLParameter], 
                              config: Dict[str, Any]) -> List[str]:
        """Generate geometry creation code"""
        code = []
        
        geometry_config = config.get("geometry", {})
        geom_type = geometry_config.get("type", "rectangle")
        
        code.append("        // Create geometry")
        code.append("        model.component().create(\"comp1\", true);")
        code.append("        model.component(\"comp1\").geom().create(\"geom1\", 3);  // 3D geometry")
        
        if geom_type == "rectangle":
            dims = geometry_config.get("dimensions", [1, 1, 1])
            code.append(f"        model.component(\"comp1\").geom(\"geom1\").create(\"blk1\", \"Block\");")
            code.append(f"        model.component(\"comp1\").geom(\"geom1\").feature(\"blk1\").set(\"size\", {dims});")
        elif geom_type == "cylinder":
            radius = geometry_config.get("radius", 1.0)
            height = geometry_config.get("height", 1.0)
            code.append(f"        model.component(\"comp1\").geom(\"geom1\").create(\"cyl1\", \"Cylinder\");")
            code.append(f"        model.component(\"comp1\").geom(\"geom1\").feature(\"cyl1\").set(\"r\", {radius});")
            code.append(f"        model.component(\"comp1\").geom(\"geom1\").feature(\"cyl1\").set(\"h\", {height});")
        elif geom_type == "sphere":
            radius = geometry_config.get("radius", 1.0)
            code.append(f"        model.component(\"comp1\").geom(\"geom1\").create(\"sph1\", \"Sphere\");")
            code.append(f"        model.component(\"comp1\").geom(\"geom1\").feature(\"sph1\").set(\"r\", {radius});")
        
        code.append("        model.component(\"comp1\").geom(\"geom1\").run();")
        code.append("")
        
        return code
    
    def _generate_mesh_code(self, parameters: Dict[str, COMSOLParameter], 
                          config: Dict[str, Any]) -> List[str]:
        """Generate mesh creation code"""
        code = []
        
        mesh_config = config.get("mesh", {})
        element_size = mesh_config.get("element_size", "normal")
        
        code.append("        // Create mesh")
        code.append("        model.component(\"comp1\").mesh().create(\"mesh1\");")
        
        if element_size == "coarse":
            code.append("        model.component(\"comp1\").mesh(\"mesh1\").automatic(true, \"coarse\");")
        elif element_size == "fine":
            code.append("        model.component(\"comp1\").mesh(\"mesh1\").automatic(true, \"fine\");")
        elif element_size == "normal":
            code.append("        model.component(\"comp1\").mesh(\"mesh1\").automatic(true);")
        
        code.append("")
        return code
    
    def _generate_physics_code(self, parameters: Dict[str, COMSOLParameter], 
                             config: Dict[str, Any]) -> List[str]:
        """Generate physics setup code"""
        code = []
        
        physics_list = config.get("physics", [])
        if isinstance(physics_list, str):
            physics_list = [physics_list]
        
        code.append("        // Add physics")
        
        for physics in physics_list:
            if physics == "electrostatics":
                code.append("        model.component(\"comp1\").physics().create(\"es1\", \"Electrostatics\", \"geom1\");")
                # Add boundary conditions
                code.append("        model.component(\"comp1\").physics(\"es1\").create(\"pot1\", \"Pointwise\", 2);")
                code.append("        model.component(\"comp1\").physics(\"es1\").feature(\"pot1\").selection().all();")
            
            elif physics == "heat_transfer":
                code.append("        model.component(\"comp1\").physics().create(\"ht1\", \"HeatTransfer\", \"geom1\");")
                code.append("        model.component(\"comp1\").physics(\"ht1\").create(\"init1\", \"Init\", \"geom1\");")
                code.append("        model.component(\"comp1\").physics(\"ht1\").feature(\"init1\").selection().all();")
            
            elif physics == "fluid_flow":
                code.append("        model.component(\"comp1\").physics().create(\"spf1\", \"LaminarFlow\", \"geom1\");")
                code.append("        model.component(\"comp1\").physics(\"spf1\").create(\"init1\", \"Init\", \"geom1\");")
                code.append("        model.component(\"comp1\").physics(\"spf1\").feature(\"init1\").selection().all();")
            
            elif physics == "structural_mechanics":
                code.append("        model.component(\"comp1\").physics().create(\"solid1\", \"SolidMechanics\", \"geom1\");")
                code.append("        model.component(\"comp1\").physics(\"solid1\").create(\"fix1\", \"Fixed\", \"geom1\");")
                code.append("        model.component(\"comp1\").physics(\"solid1\").feature(\"fix1\").selection().all();")
        
        code.append("")
        return code
    
    def _generate_study_code(self, parameters: Dict[str, COMSOLParameter], 
                           config: Dict[str, Any]) -> List[str]:
        """Generate study setup code"""
        code = []
        
        solver_config = config.get("solver", {})
        solver_type = solver_config.get("solver_type", "stationary")
        
        code.append("        // Create study")
        
        if solver_type == "stationary":
            code.append("        model.study().create(\"std1\");")
            code.append("        model.study(\"std1\").create(\"stat\", \"Stationary\");")
        elif solver_type == "time_dependent":
            time_range = solver_config.get("time_range", [0, 1])
            code.append("        model.study().create(\"std1\");")
            code.append("        model.study(\"std1\").create(\"time\", \"Time\");")
            code.append(f"        model.study(\"std1\").feature(\"time\").set(\"tlist\", \"range({time_range[0]}, 0.1, {time_range[1]})\")")
        elif solver_type == "eigenfrequency":
            code.append("        model.study().create(\"std1\");")
            code.append("        model.study(\"std1\").create(\"eig\", \"Eigenfrequency\");")
        
        code.append("")
        return code
    
    def _generate_solver_code(self, parameters: Dict[str, COMSOLParameter], 
                            config: Dict[str, Any]) -> List[str]:
        """Generate solver setup code"""
        code = []
        
        solver_config = config.get("solver", {})
        rel_tol = solver_config.get("relative_tolerance", 0.001)
        
        code.append("        // Configure solver")
        code.append("        model.sol().create(\"sol1\");")
        code.append("        model.sol(\"sol1\").study(\"std1\");")
        code.append(f"        model.sol(\"sol1\").feature(\"s1\").set(\"rtol\", {rel_tol});")
        
        code.append("")
        return code
    
    def generate_matlab_code(self, parameters: Dict[str, COMSOLParameter], 
                           config: Dict[str, Any]) -> str:
        """Generate MATLAB code for COMSOL API"""
        matlab_code = []
        matlab_code.append("% COMSOL Model Generation")
        matlab_code.append("")
        matlab_code.append("model = mphload('blank_model.mph'); % Load a blank model template")
        matlab_code.append("")
        
        # Add parameters
        matlab_code.append("% Set parameters")
        for name, param in parameters.items():
            if name != "parameters":
                matlab_code.append(f"model.param.set('{name}', '{param.to_comsol_string()}');")
        
        # Add nested parameters
        if "parameters" in parameters and isinstance(parameters["parameters"].value, dict):
            for name, value in parameters["parameters"].value.items():
                if isinstance(value, dict):
                    param_val = value.get("value", "")
                    matlab_code.append(f"model.param.set('{name}', '{param_val}');")
        
        matlab_code.append("")
        
        # Build geometry
        geometry_config = config.get("geometry", {})
        geom_type = geometry_config.get("type", "rectangle")
        matlab_code.append("% Build geometry")
        
        if geom_type == "rectangle":
            dims = geometry_config.get("dimensions", [1, 1, 1])
            matlab_code.append("model.component.create('comp1', true);")
            matlab_code.append("model.component('comp1').geom.create('geom1', 3);")
            matlab_code.append(f"model.component('comp1').geom('geom1').create('blk1', 'Block');")
            matlab_code.append(f"model.component('comp1').geom('geom1').feature('blk1').set('size', [{dims[0]} {dims[1]} {dims[2]}]);")
            matlab_code.append("model.component('comp1').geom('geom1').run;")
        
        matlab_code.append("")
        matlab_code.append("% Build mesh")
        matlab_code.append("model.component('comp1').mesh.create('mesh1');")
        matlab_code.append("model.component('comp1').mesh('mesh1').run;")
        matlab_code.append("")
        
        # Add physics
        physics_list = config.get("physics", [])
        if isinstance(physics_list, str):
            physics_list = [physics_list]
        
        matlab_code.append("% Add physics")
        for physics in physics_list:
            if physics == "electrostatics":
                matlab_code.append("model.component('comp1').physics.create('es1', 'Electrostatics', 'geom1');")
        
        matlab_code.append("")
        matlab_code.append("% Create study")
        solver_config = config.get("solver", {})
        solver_type = solver_config.get("solver_type", "stationary")
        
        if solver_type == "stationary":
            matlab_code.append("model.study.create('std1');")
            matlab_code.append("model.study('std1').create('stat', 'Stationary');")
        
        matlab_code.append("")
        matlab_code.append("% Solve")
        matlab_code.append("model.sol.create('sol1');")
        matlab_code.append("model.sol('sol1').study('std1');")
        matlab_code.append("model.sol('sol1').run;")
        matlab_code.append("")
        matlab_code.append("% Save model")
        model_name = config.get("model_name", "generated_model")
        matlab_code.append(f"mphsave(model, '{model_name}.mph');")
        
        return "\n".join(matlab_code)


def main():
    """Main function for model creation"""
    if len(sys.argv) < 2:
        print("Usage: python3 model_creator.py <config_file.json> [output_format]")
        print("  output_format: 'java' or 'matlab' (default: java)")
        return
    
    config_file = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "java"
    
    try:
        # Load configuration
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Process parameters
        validator = ParameterValidator()
        parameters = validator.process_parameters(config_file)
        
        # Create model generator
        creator = COMSOLModelCreator()
        
        # Generate code
        if output_format.lower() == "matlab":
            code = creator.generate_matlab_code(parameters, config)
            output_file = f"{config.get('model_name', 'generated_model')}.m"
        else:
            code = creator.generate_java_code(parameters, config)
            output_file = f"{config.get('model_name', 'GeneratedModel')}.java"
        
        # Save generated code
        with open(output_file, 'w') as f:
            f.write(code)
        
        print(f"Generated {output_format} code: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()