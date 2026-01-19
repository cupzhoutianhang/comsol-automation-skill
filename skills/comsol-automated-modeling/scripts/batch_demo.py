#!/usr/bin/env python3
"""
COMSOL Batch Generator Demo (COMSOL-free version)
Demonstrates the core functionality without requiring COMSOL installation
"""

import os
import sys
import json
import logging
import random
import traceback
from typing import List, Dict, Any, Tuple
from itertools import product
from pathlib import Path


class COMSOLBatchGeneratorDemo:
    """Demo version of batch generator - shows core logic without COMSOL dependency"""
    
    def __init__(self, config_file: str):
        self.config = self._load_config(config_file)
        self.setup_logging()
        self.generated_files = []
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except Exception as e:
            print(f"Error loading config file: {e}")
            sys.exit(1)
            
    def setup_logging(self):
        """Setup logging configuration"""
        log_level = self.config.get('execution_settings', {}).get('log_level', 'INFO')
        level = getattr(logging, log_level)
        
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("comsol_demo_batch.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def create_output_directory(self):
        """Create output directory"""
        output_dir = self.config['output_directory']
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                self.logger.info(f"Created output directory: {output_dir}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create output directory: {e}")
            return False
            
    def generate_parameter_combinations(self) -> List[Dict[str, float]]:
        """Generate all parameter combinations with filtering (same as your original script)"""
        self.logger.info("=== Generating Parameter Combinations ===")
        
        parameters = self.config['parameters']
        param_names = list(parameters.keys())
        param_values = list(parameters.values())
        
        # Generate all possible combinations (笛卡尔积)
        all_combinations = []
        for values in product(*param_values):
            combination = dict(zip(param_names, values))
            all_combinations.append(combination)
            
        self.logger.info(f"Total theoretical combinations: {len(all_combinations)}")
        
        # Apply filtering logic from your script (K_ch > 2.4 and W_ch > 2.4 and W_rib > 9)
        parameter_combinations = []
        for combo in all_combinations:
            if combo["K_ch"] > 2.4 and combo["W_ch"] > 2.4 and combo["W_rib"] > 9:
                # 50% probability to skip (matching random.random() < 0.5 in your script)
                if random.random() < 0.5:
                    continue
            parameter_combinations.append(combo)
        
        # Limit to target count (868 in your case)
        target_count = self.config.get('batch_filtering', {}).get('target_count', 868)
        if len(parameter_combinations) > target_count:
            random.shuffle(parameter_combinations)
            parameter_combinations = parameter_combinations[:target_count]
        
        final_count = len(parameter_combinations)
        self.logger.info(f"Filtered to {final_count} combinations for processing")
        
        return parameter_combinations
        
    def calculate_mesh_parameters(self, geom_params: Dict[str, float]) -> Dict[str, float]:
        """Calculate mesh parameters (same logic as your script)"""
        mesh_config = self.config.get('mesh_settings', {})
        mesh_params = {}
        
        # Calculate interior mesh size (K_ch/5 as in your script)
        K_ch = geom_params["K_ch"]
        interior_mesh_size = K_ch / 5
        mesh_params["interior_mesh_size"] = interior_mesh_size
        
        # Calculate actual cell counts and mesh sizes
        stream_width_cells = K_ch / interior_mesh_size
        actual_stream_width_cells = max(1, round(stream_width_cells))
        stream_width_mesh_size = K_ch / actual_stream_width_cells
        mesh_params["stream_width_mesh_size"] = stream_width_mesh_size
        mesh_params["stream_width_cells"] = actual_stream_width_cells
        
        W_ch = geom_params["W_ch"]
        stream_depth_cells = W_ch / interior_mesh_size
        actual_stream_depth_cells = max(1, round(stream_depth_cells))
        stream_depth_mesh_size = W_ch / actual_stream_depth_cells
        mesh_params["stream_depth_mesh_size"] = stream_depth_mesh_size
        mesh_params["stream_depth_cells"] = actual_stream_depth_cells
        
        self.logger.info(f"Calculated mesh parameters: {mesh_params}")
        return mesh_params
        
    def generate_filename(self, param_values: Dict[str, float]) -> str:
        """Generate filename following your naming convention"""
        naming_config = self.config.get('file_naming', {})
        format_str = naming_config.get('format', 'batch_model_Kch_{K_ch}_Wch_{W_ch}_Wrib_{W_rib}')
        extension = naming_config.get('extension', '.mph')
        
        # Format values to match your script (三位小数 or scientific notation)
        formatted_params = {}
        for key, value in param_values.items():
            if abs(value) < 1e-2 or abs(value) > 1e6:
                formatted_params[key] = f"{value:.3e}"
            else:
                formatted_params[key] = f"{value:.3f}"
        
        filename = format_str.format(**formatted_params)
        filename += extension
        
        # Replace scientific notation e+ with e
        filename = filename.replace("e+", "e")
        
        return filename
        
    def create_model_metadata(self, param_values: Dict[str, float], mesh_params: Dict[str, float]) -> Dict[str, Any]:
        """Create model metadata file (simulates model generation)"""
        metadata = {
            "model_parameters": param_values,
            "mesh_parameters": mesh_params,
            "generation_timestamp": "2026-01-19T15:30:00Z",
            "template_source": self.config.get('template_model', 'unknown'),
            "generation_script": "comsol_skill_batch_generator",
            "version": "1.0",
        }
        return metadata
        
    def process_single_combination(self, param_values: Dict[str, float], idx: int, total: int) -> bool:
        """Process a single parameter combination (demo version)"""
        self.logger.info(f"Processing combination {idx}/{total}: {param_values}")
        
        try:
            # Simulate loading template (logging only)
            self.logger.info(f"Loading template: {self.config['template_model']}")
            
            # Set up parameters with units (same as your script)
            units = self.config.get('parameter_units', {})
            for param_name, param_value in param_values.items():
                unit = units.get(param_name, "")
                # Format like your script: f"{param_value:.2f}[{unit}]"
                formatted_value = f"{param_value:.2f}[{unit}]"
                self.logger.info(f"  Parameter {param_name}: {formatted_value}")
            
            # Calculate mesh parameters
            mesh_params = self.calculate_mesh_parameters(param_values)
            
            # Simulate mesh generation
            self.logger.info("Generating mesh...")
            self.logger.info(f"  Stream interior mesh: {mesh_params['interior_mesh_size']:.4f}")
            self.logger.info(f"  Width cells: {mesh_params['stream_width_cells']}")
            self.logger.info(f"  Depth cells: {mesh_params['stream_depth_cells']}")
            
            # Generate filename
            filename = self.generate_filename(param_values)
            output_path = os.path.join(self.config['output_directory'], filename)
            
            # Save metadata file instead of actual COMSOL model
            metadata = self.create_model_metadata(param_values, mesh_params)
            metadata_file = output_path.replace('.mph', '_metadata.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            # Create placeholder .mph file
            with open(output_path, 'w') as f:
                f.write(f"# COMSOL Model File (Demo)")
                f.write(f"# Generated by COMSOL Automation Skill")
                f.write(f"# Parameters: {param_values}")
                f.write(f"# Mesh params: {mesh_params}")
            
            # Verify output
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                self.logger.info(f"Generated model: {output_path} ({file_size} bytes)")
                self.generated_files.append(output_path)
                return True
            else:
                self.logger.error(f"Failed to create output file: {output_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to process combination {idx}: {e}")
            self.logger.error(traceback.format_exc())
            return False
            
    def run_batch_generation(self):
        """Run the complete batch generation process (demo version)"""
        self.logger.info("=== Starting COMSOL Batch Generation Demo ===")
        self.logger.info("Note: This is a demo version that simulates the workflow")
        self.logger.info("without requiring COMSOL software to be installed.")
        print()
        
        try:
            # Create output directory
            if not self.create_output_directory():
                return False
                
            # Generate parameter combinations
            combinations = self.generate_parameter_combinations()
            
            # Process each combination
            success_count = 0
            error_count = 0
            
            for idx, param_values in enumerate(combinations, 1):
                success = self.process_single_combination(param_values, idx, len(combinations))
                if success:
                    success_count += 1
                else:
                    error_count += 1
                    
                # Progress reporting
                if idx % 100 == 0 or idx == len(combinations):
                    self.logger.info(f"Progress: {idx}/{len(combinations)} ({success_count} successful, {error_count} errors)")
                    
            # Create summary report
            self.create_summary_report(success_count, error_count, len(combinations))
            
            # Final results
            print("\n" + "="*60)
            print("🎉 DEMO COMPLETED SUCCESSFULLY!")
            print("="*60)
            print(f"🎯 Target: {len(combinations)} parameter combinations")
            print(f"✅ Generated: {success_count} model files")
            print(f"❌ Errors: {error_count}")
            print(f"📁 Output directory: {self.config['output_directory']}")
            print(f"📝 Log file: comsol_demo_batch.log")
            print()
            print("📋 Files generated:")
            for i, filepath in enumerate(self.generated_files[:5], 1):
                filename = os.path.basename(filepath)
                print(f"   {i}. {filename}")
            if len(self.generated_files) > 5:
                print(f"   ... and {len(self.generated_files)-5} more files")
            print()
            print("🔍 To see the actual functionality:")
            print("   1. Install COMSOL Multiphysics")
            print("   2. Update COMSOL_PATH in the script")
            print("   3. Run without _demo.py extension")
            print("="*60)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Demo failed: {e}")
            self.logger.error(traceback.format_exc())
            return False
            
    def create_summary_report(self, success_count: int, error_count: int, total: int):
        """Create a summary report of the generation process"""
        report = {
            "generation_summary": {
                "timestamp": "2026-01-19T15:30:00Z",
                "total_combinations": total,
                "successful_generations": success_count,
                "failed_generations": error_count,
                "success_rate": f"{(success_count/total)*100:.1f}%" if total > 0 else "0%"
            },
            "configuration": self.config,
            "generated_files": [
                {
                    "filename": os.path.basename(f),
                    "relative_path": os.path.relpath(f, self.config['output_directory']),
                    "size_bytes": os.path.getsize(f) if os.path.exists(f) else 0
                }
                for f in self.generated_files
            ]
        }
        
        report_file = os.path.join(self.config['output_directory'], "generation_summary.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Summary report saved to: {report_file}")


def main():
    """Main function"""
    print("🚀 COMSOL Automation Skill - Batch Generator Demo")
    print("This demo shows the workflow without requiring COMSOL installation")
    print()
    
    if len(sys.argv) != 2:
        print("Usage: python3 batch_demo.py <config_file.json>")
        print("Example: python3 batch_demo.py test_batch_config.json")
        print()
        print("This will demonstrate:")
        print("✓ Parameter combination generation")
        print("✓ Filtering logic (matching your 868 files target)")  
        print("✓ Mesh parameter calculation")
        print("✓ Systematic file naming")
        print("✓ Batch processing workflow")
        sys.exit(1)
        
    config_file = sys.argv[1]
    
    # Initialize and run batch generator demo
    demo = COMSOLBatchGeneratorDemo(config_file)
    success = demo.run_batch_generation()
    
    if not success:
        print("\n❌ Demo failed. Check the log file for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()