#!/usr/bin/env python3
"""
COMSOL Batch Generator
Specialized script for mass COMSOL model generation with parameter sweeps
Replicates and extends functionality from comsol.py
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

try:
    import mph
except ImportError:
    print("Error: mph library not installed.")
    print("Please install it using:")
    print("  /Users/zhoutianhang/anaconda3/bin/pip install mph")
    print("Or activate the anaconda environment with 'conda activate'")
    sys.exit(1)


class COMSOLBatchGenerator:
    """Batch generator for COMSOL models with parameter sweeps"""
    
    def __init__(self, config_file: str):
        self.config = self._load_config(config_file)
        self.client = None
        self.setup_logging()
        
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
        log_level = getattr(logging, self.config.get('execution_settings', {}).get('log_level', 'INFO'))
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("comsol_skill_batch.log", encoding='utf-8'),
                logging.StreamHandler()
            ],
            encoding='utf-8'
        )
        self.logger = logging.getLogger(__name__)
        
    def create_output_directory(self):
        """Create output directory if it doesn't exist"""
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
        """Generate all parameter combinations with filtering"""
        self.logger.info("=== Generating Parameter Combinations ===")
        
        parameters = self.config['parameters']
        param_names = list(parameters.keys())
        param_values = list(parameters.values())
        
        # Generate all possible combinations
        all_combinations = []
        for values in product(*param_values):
            combination = dict(zip(param_names, values))
            all_combinations.append(combination)
            
        self.logger.info(f"Total theoretical combinations: {len(all_combinations)}")
        
        # Apply filtering based on configuration
        filtering_config = self.config.get('batch_filtering', {})
        target_count = filtering_config.get('target_count', 868)
        
        if filtering_config:
            filtered_combinations = self._apply_filtering(all_combinations, filtering_config)
        else:
            filtered_combinations = all_combinations
            
        # If we have more than target count, randomly sample
        if len(filtered_combinations) > target_count:
            random.shuffle(filtered_combinations)
            filtered_combinations = filtered_combinations[:target_count]
            
        final_count = len(filtered_combinations)
        self.logger.info(f"Filtered to {final_count} combinations ({target_count} target)")
        
        return filtered_combinations
        
    def _apply_filtering(self, combinations: List[Dict], filtering_config: Dict) -> List[Dict]:
        """Apply filtering rules to parameter combinations"""
        exclude_condition = filtering_config.get('exclude_condition', {})
        sample_rate = filtering_config.get('sample_rate', 0.5)
        
        filtered = []
        excluded_count = 0
        
        for combo in combinations:
            # Check exclusion conditions (simplified logic matching your script)
            if (combo["K_ch"] > 2.4 and combo["W_ch"] > 2.4 and combo["W_rib"] > 9):
                # 50% probability to skip (matching your random.random() < 0.5)
                if random.random() < sample_rate:
                    excluded_count += 1
                    continue
                    
            filtered.append(combo)
            
        self.logger.info(f"Excluded {excluded_count} combinations due to filtering")
        return filtered
        
    def generate_filename(self, param_values: Dict[str, float]) -> str:
        """Generate systematic filename based on parameters"""
        naming_config = self.config.get('file_naming', {})
        format_str = naming_config.get('format', 'batch_model_param1_{param1}_param2_{param2}')
        extension = naming_config.get('extension', '.mph')
        
        # Replace placeholders in format string
        filename = format_str.format(**param_values)
        filename += extension
        
        return filename
        
    def connect_comsol_server(self):
        """Connect to COMSOL server"""
        self.logger.info("=== Connecting to COMSOL Server ===")
        try:
            # Try different connection methods
            try:
                self.client = mph.Client()
            except Exception as e1:
                self.logger.warning(f"Direct connection failed: {e1}")
                # Try with specific port
                self.client = mph.Client(8080)
                
            self.logger.info("COMSOL server connection established")
            return True
        except Exception as e:
            self.logger.error(f"COMSOL server connection failed: {e}")
            self.logger.error("Make sure COMSOL is installed and running")
            return False
            
    def calculate_mesh_parameters(self, geom_params: Dict[str, float]) -> Dict[str, float]:
        """Calculate mesh parameters based on geometry"""
        mesh_config = self.config.get('mesh_settings', {})
        mesh_params = {}
        
        # Extract base mesh size from configuration
        for config_key, config_value in mesh_config.items():
            if isinstance(config_value, str) and '/' in config_value:
                # Parse expressions like "K_ch/5"
                param_name, divisor = config_value.split('/')
                if param_name in geom_params:
                    mesh_params[config_key] = geom_params[param_name] / float(divisor)
                    
        self.logger.info(f"Calculated mesh parameters: {mesh_params}")
        return mesh_params
        
    def setup_parameters_in_model(self, model, param_values: Dict[str, float]):
        """Setup parameters in COMSOL model"""
        units = self.config.get('parameter_units', {})
        
        # List all parameters for debugging
        all_params = model.parameters()
        self.logger.info(f"Model has {len(all_params)} parameters: {list(all_params.keys())[:10]}...")
        
        for param_name, param_value in param_values.items():
            try:
                if param_name not in all_params:
                    self.logger.warning(f"  Parameter {param_name} not found in model, skipping")
                    continue
                    
                unit = units.get(param_name, "")
                
                # Format parameter value with unit (matching your script format)
                formatted_value = f"{param_value:.2f}[{unit}]"
                
                # Get old value
                old_value = model.parameter(param_name)
                
                # Set new value
                model.parameter(param_name, formatted_value)
                
                # Verify
                set_value = model.parameter(param_name)
                self.logger.info(f"  Set {param_name}: {old_value} -> {set_value}")
                
            except Exception as e:
                self.logger.error(f"Failed to set parameter {param_name}: {e}")
                raise
                
    def generate_mesh_for_model(self, model, param_values: Dict[str, float], mesh_params: Dict[str, float]) -> bool:
        """Generate mesh for the model"""
        self.logger.info("=== Generating Mesh ===")
        try:
            # Try to build mesh
            model.mesh('mesh1').run()
            self.logger.info("Mesh generation completed successfully")
            return True
        except Exception as e:
            self.logger.error(f"Mesh generation failed: {e}")
            if self.config.get('execution_settings', {}).get('error_tolerance') == 'continue':
                return False
            else:
                raise
                
    def verify_mesh_quality(self, model):
        """Verify mesh quality"""
        try:
            # Get mesh statistics if available
            mesh_stats = model.mesh('mesh1').get()
            self.logger.info(f"Mesh statistics: {mesh_stats}")
        except Exception as e:
            self.logger.warning(f"Could not get mesh statistics: {e}")
            
    def verify_output_file(self, output_path: str, param_values: Dict[str, float]):
        """Verify the generated output file"""
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            self.logger.info(f"Output file verified: {output_path} ({file_size} bytes)")
        else:
            self.logger.error(f"Output file not found: {output_path}")
            
    def process_single_combination(self, param_values: Dict[str, float], idx: int, total: int) -> bool:
        """Process a single parameter combination"""
        self.logger.info(f"Processing combination {idx}/{total}: {param_values}")
        
        model = None
        try:
            # Check if template exists
            template_path = self.config['template_model']
            if not os.path.exists(template_path):
                self.logger.error(f"Template file not found: {template_path}")
                return False
                
            # Load template model
            self.logger.info(f"Loading template: {template_path}")
            model = self.client.load(template_path)
            
            # Setup parameters
            self.setup_parameters_in_model(model, param_values)
            
            # Calculate mesh parameters
            mesh_params = self.calculate_mesh_parameters(param_values)
            
            # Generate mesh
            mesh_success = self.generate_mesh_for_model(model, param_values, mesh_params)
            
            if mesh_success:
                # Verify mesh quality
                self.verify_mesh_quality(model)
            else:
                self.logger.warning("Mesh generation failed, but continuing with model save")
                
            # Generate filename and save
            filename = self.generate_filename(param_values)
            output_path = os.path.join(self.config['output_directory'], filename)
            
            self.logger.info(f"Saving model: {output_path}")
            model.save(output_path)
            
            # Verify output
            if self.config.get('post_processing', {}).get('verify_output', True):
                self.verify_output_file(output_path, param_values)
                
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to process combination {idx}: {e}")
            self.logger.error(traceback.format_exc())
            return False
            
        finally:
            # Clean up model
            if model is not None:
                try:
                    self.client.remove(model)
                    self.logger.info("Model cleaned up")
                except Exception as e:
                    self.logger.warning(f"Failed to clean up model: {e}")
                    
    def run_batch_generation(self):
        """Run the complete batch generation process"""
        self.logger.info("=== Starting COMSOL Batch Generation ===")
        
        try:
            # Create output directory
            if not self.create_output_directory():
                return False
                
            # Connect to COMSOL server
            if not self.connect_comsol_server():
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
                    
            # Final summary
            self.logger.info("=== Batch Generation Complete ===")
            self.logger.info(f"Total combinations: {len(combinations)}")
            self.logger.info(f"Successful: {success_count}")
            self.logger.info(f"Errors: {error_count}")
            
            return True
            
        except KeyboardInterrupt:
            self.logger.info("Batch generation interrupted by user")
            return False
        except Exception as e:
            self.logger.error(f"Batch generation failed: {e}")
            self.logger.error(traceback.format_exc())
            return False
        finally:
            # Cleanup
            if self.client is not None:
                try:
                    self.client.disconnect()
                    self.logger.info("COMSOL server connection closed")
                except Exception as e:
                    self.logger.warning(f"Failed to close COMSOL connection: {e}")


def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python3 batch_generator.py <config_file.json>")
        print("Example: python3 batch_generator.py interdigitated_flow_batch.json")
        sys.exit(1)
        
    config_file = sys.argv[1]
    
    # Initialize and run batch generator
    generator = COMSOLBatchGenerator(config_file)
    success = generator.run_batch_generation()
    
    if success:
        print("\n✅ Batch generation completed successfully!")
        print(f"Check the log file and output directory: {generator.config['output_directory']}")
    else:
        print("\n❌ Batch generation failed. Check the log file for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()