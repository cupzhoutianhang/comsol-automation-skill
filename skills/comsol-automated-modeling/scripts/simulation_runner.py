#!/usr/bin/env python3
"""
COMSOL Simulation Executor
Handles running COMSOL simulations and post-processing results
"""

import json
import os
import sys
import subprocess
from typing import Dict, Any, List, Optional
from pathlib import Path


class COMSOLSimulationRunner:
    """Executes COMSOL simulations and manages the workflow"""
    
    def __init__(self, comsol_path: str = None):
        self.comsol_path = comsol_path or self._find_comsol()
        self.results = {}
        
    def _find_comsol(self) -> str:
        """Try to find COMSOL installation path"""
        # Common COMSOL installation paths
        common_paths = [
            "/Applications/COMSOL/COMSOL56/Multiphysics",  # macOS
            "/usr/local/comsol56/multiphysics",  # Linux
            "C:/Program Files/COMSOL/COMSOL56/Multiphysics",  # Windows
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        # Try environment variable
        comsol_env = os.environ.get('COMSOL_PATH')
        if comsol_env and os.path.exists(comsol_env):
            return comsol_env
        
        return None
    
    def run_batch_simulation(self, model_file: str, output_dir: str = "results") -> Dict[str, Any]:
        """Run a simulation in batch mode"""
        if not self.comsol_path:
            raise RuntimeError("COMSOL installation not found. Please set COMSOL_PATH environment variable.")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate batch command
        batch_script = self._create_batch_script(model_file, output_dir)
        
        # Execute simulation
        result = self._execute_batch_job(batch_script)
        
        # Process results
        self.results = self._process_results(output_dir)
        
        return self.results
    
    def _create_batch_script(self, model_file: str, output_dir: str) -> str:
        """Create a batch script for COMSOL"""
        script_content = f"""
        # COMSOL Batch Script
        # Generated automatically by COMSOL automation skill
        
        # Load the model
        model = mphload('{model_file}')
        
        # Solve
        model.sol('sol1').run()
        
        # Export results
        # Export solution data
        model.result().export('data1').set('data', 'dset1');
        model.result().export('data1').set('filename', '{output_dir}/solution_data.txt');
        model.result().export('data1').set('type', 'txt');
        model.result().export('data1').run();
        
        # Export mesh if available
        if model.mesh().isValid('mesh1')
            model.mesh('mesh1').export('{output_dir}/mesh_data.mphtxt');
        end
        
        # Save model with results
        mphsave(model, '{output_dir}/solved_model.mph');
        
        # Exit
        exit;
        """
        
        script_file = "batch_script.m"
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        return script_file
    
    def _execute_batch_job(self, script_file: str) -> subprocess.CompletedProcess:
        """Execute the COMSOL batch job"""
        if not self.comsol_path:
            raise RuntimeError("COMSOL installation not found")
        
        # COMSOL command line options
        mpiexec = os.path.join(self.comsol_path, "bin", "mpiexec")
        comsol = os.path.join(self.comsol_path, "bin", "comsol")
        
        # For different platforms
        if sys.platform.startswith('win'):
            mpiexec += ".exe"
            comsol += ".bat"
        
        # Build command
        cmd = [comsol, "batch", "-inputfile", script_file]
        
        print(f"Executing command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=3600)  # 1 hour timeout
            
            if result.returncode == 0:
                print("Simulation completed successfully")
            else:
                print(f"Simulation failed with return code: {result.returncode}")
                print(f"Error output: {result.stderr}")
            
            return result
            
        except subprocess.TimeoutExpired:
            print("Simulation timed out after 1 hour")
            raise
        except Exception as e:
            print(f"Error running simulation: {e}")
            raise
    
    def _process_results(self, results_dir: str) -> Dict[str, Any]:
        """Process simulation results"""
        results = {
            "files_generated": [],
            "solution_data": None,
            "mesh_data": None,
            "summary": {}
        }
        
        # Check what files were generated
        for file in os.listdir(results_dir):
            file_path = os.path.join(results_dir, file)
            results["files_generated"].append(file)
            
            if file.endswith(".txt"):
                try:
                    with open(file_path, 'r') as f:
                        data = f.read()
                        results["solution_data"] = data[:1000]  # First 1000 chars
                        
                    # Basic statistics
                    lines = data.strip().split('\n')
                    results["summary"]["data_points"] = len(lines)
                    
                except Exception as e:
                    results["summary"][f"error_reading_{file}"] = str(e)
        
        return results
    
    def run_parameter_sweep(self, base_config: str, parameter: str, 
                          values: List[float], output_dir: str = "parameter_sweep") -> Dict[str, Any]:
        """Run parameter sweep simulation"""
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        
        for i, value in enumerate(values):
            print(f"Running parameter sweep {i+1}/{len(values)}: {parameter} = {value}")
            
            # Create modified config
            sweep_dir = os.path.join(output_dir, f"sweep_{i}")
            os.makedirs(sweep_dir, exist_ok=True)
            
            # Update parameter in config
            with open(base_config, 'r') as f:
                config = json.load(f)
            
            if "parameters" not in config:
                config["parameters"] = {}
            
            config["parameters"][parameter] = value
            
            # Save modified config
            sweep_config = os.path.join(sweep_dir, "config.json")
            with open(sweep_config, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Generate model and run simulation
            model_file = self._generate_model_from_config(sweep_config, sweep_dir)
            
            try:
                single_result = self.run_batch_simulation(model_file, sweep_dir)
                results.append({
                    "parameter": parameter,
                    "value": value,
                    "result": single_result
                })
                
            except Exception as e:
                print(f"Error in parameter sweep {i+1}: {e}")
                results.append({
                    "parameter": parameter,
                    "value": value,
                    "error": str(e)
                })
        
        # Save summary
        summary_file = os.path.join(output_dir, "parameter_sweep_summary.json")
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        return {"sweep_results": results, "summary_file": summary_file}
    
    def _generate_model_from_config(self, config_file: str, output_dir: str) -> str:
        """Generate a COMSOL model from configuration"""
        # This would call the model_creator module
        # For now, return a placeholder
        return os.path.join(output_dir, "generated_model.mph")


class ResultProcessor:
    """Process and analyze simulation results"""
    
    def __init__(self, results_dir: str):
        self.results_dir = results_dir
    
    def generate_summary_report(self) -> str:
        """Generate a summary report of simulation results"""
        report = []
        report.append("# COMSOL Simulation Results Report")
        report.append("")
        
        # List all result files
        report.append("## Generated Files")
        files = os.listdir(self.results_dir)
        for file in files:
            file_path = os.path.join(self.results_dir, file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                report.append(f"- {file} ({size:,} bytes)")
        
        report.append("")
        
        # Try to parse solution data
        solution_file = None
        for file in files:
            if "solution" in file and file.endswith(".txt"):
                solution_file = file
                break
        
        if solution_file:
            report.append("## Solution Data Summary")
            try:
                with open(os.path.join(self.results_dir, solution_file), 'r') as f:
                    data = f.read()
                
                lines = data.strip().split('\n')
                report.append(f"- Total data points: {len(lines)}")
                
                # Try to extract numerical data for statistics
                if lines and '\t' in lines[0]:  # Tab-separated data
                    try:
                        # Parse numerical columns
                        numeric_lines = []
                        for line in lines:
                            parts = line.split('\t')
                            numeric_parts = []
                            for part in parts:
                                try:
                                    numeric_parts.append(float(part.strip()))
                                except ValueError:
                                    numeric_parts.append(float('nan'))
                            if any(not (x != x) for x in numeric_parts):  # Check for non-NaN
                                numeric_lines.append(numeric_parts)
                        
                        if numeric_lines:
                            import statistics
                            num_cols = len(numeric_lines[0])
                            
                            for col in range(num_cols):
                                col_data = [line[col] for line in numeric_lines if line[col] == line[col]]  # Filter NaN
                                if col_data:
                                    report.append(f"- Column {col+1}: min={min(col_data):.4e}, max={max(col_data):.4e}, mean={statistics.mean(col_data):.4e}")
                    except Exception:
                        report.append("- Unable to parse numerical statistics")
                
                # Preview data
                report.append("")
                report.append("### Data Preview (first 10 lines)")
                for i, line in enumerate(lines[:10]):
                    report.append(f"```")
                    report.append(line)
                    report.append(f"```")
                    if i < min(9, len(lines)-1):
                        report.append("")
                
            except Exception as e:
                report.append(f"- Error reading solution data: {e}")
        
        return "\n".join(report)


def create_sample_sweep_config():
    """Create a sample parameter sweep configuration"""
    sample_config = {
        "model_name": "thermal_analysis",
        "geometry": {
            "type": "rectangle",
            "dimensions": [10, 5, 2]
        },
        "physics": ["heat_transfer"],
        "materials": {
            "domain": "Copper",
            "boundary": "Air"
        },
        "mesh": {
            "element_size": "normal"
        },
        "solver": {
            "solver_type": "stationary"
        },
        "parameters": {
            "temperature": {
                "value": 293.15,
                "unit": "K",
                "description": "Initial temperature"
            },
            "heat_flux": {
                "value": 1000,
                "unit": "W/m²",
                "description": "Applied heat flux"
            }
        }
    }
    
    with open("parameter_sweep_config.json", 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print("Sample parameter sweep configuration 'parameter_sweep_config.json' created")


def main():
    """Main function for simulation runner"""
    if len(sys.argv) < 2:
        print("Usage: python3 simulation_runner.py <command> [args...]")
        print("  Commands:")
        print("    batch <model_file> [output_dir]")
        print("    sweep <config_file> <parameter> <values_file> [output_dir]")
        print("    summary <results_dir>")
        print("    sample")
        return
    
    command = sys.argv[1]
    
    if command == "sample":
        create_sample_sweep_config()
        return
    
    runner = COMSOLSimulationRunner()
    
    if command == "batch":
        if len(sys.argv) < 3:
            print("Usage: python3 simulation_runner.py batch <model_file> [output_dir]")
            return
        
        model_file = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "results"
        
        try:
            results = runner.run_batch_simulation(model_file, output_dir)
            print("Simulation completed. Results:")
            print(f"  Files generated: {results['files_generated']}")
            print(f"  Data points: {results['summary'].get('data_points', 'N/A')}")
        except Exception as e:
            print(f"Error: {e}")
    
    elif command == "sweep":
        if len(sys.argv) < 5:
            print("Usage: python3 simulation_runner.py sweep <config_file> <parameter> <values_file> [output_dir]")
            return
        
        config_file = sys.argv[2]
        parameter = sys.argv[3]
        values_file = sys.argv[4]
        output_dir = sys.argv[5] if len(sys.argv) > 5 else "parameter_sweep"
        
        # Load parameter values
        with open(values_file, 'r') as f:
            values = json.load(f)
        
        try:
            results = runner.run_parameter_sweep(config_file, parameter, values, output_dir)
            print(f"Parameter sweep completed. Summary saved to: {results['summary_file']}")
        except Exception as e:
            print(f"Error: {e}")
    
    elif command == "summary":
        if len(sys.argv) < 3:
            print("Usage: python3 simulation_runner.py summary <results_dir>")
            return
        
        results_dir = sys.argv[2]
        processor = ResultProcessor(results_dir)
        report = processor.generate_summary_report()
        print(report)


if __name__ == "__main__":
    main()