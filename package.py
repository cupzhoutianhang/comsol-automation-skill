#!/usr/bin/env python3
"""
COMSOL Automated Modeling Skill Packaging Script
Developed by: Zhou Tianhang, China University of Petroleum (Beijing)
Contact: zhouth@cup.edu.cn

This script packages the COMSOL automation skill for distribution.
"""

import os
import shutil
import json
from datetime import datetime

def create_skill_package(skill_dir, output_dir):
    """
    Create a packaged skill from the skill directory
    """
    skill_name = os.path.basename(skill_dir)
    package_name = f"{skill_name}.skill"
    package_path = os.path.join(output_dir, package_name)
    
    # Create temporary directory for packaging
    temp_dir = f"/tmp/{skill_name}_package"
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Copy all skill files
        for item in os.listdir(skill_dir):
            source = os.path.join(skill_dir, item)
            dest = os.path.join(temp_dir, item)
            if os.path.isdir(source):
                shutil.copytree(source, dest)
            else:
                shutil.copy2(source, dest)
        
        # Create package metadata
        metadata = {
            "name": skill_name,
            "version": "1.0.0",
            "description": "COMSOL Multiphysics automation solution for end-to-end simulation workflows",
            "created": datetime.now().isoformat(),
            "author": "Zhou Tianhang, China University of Petroleum (Beijing)",
            "contact": "zhouth@cup.edu.cn",
            "dependencies": [
                "mph>=1.0.0",
                "numpy",
                "pandas",
                "scipy"
            ]
        }
        
        with open(os.path.join(temp_dir, "skill.json"), "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Create final package
        shutil.make_archive(
            os.path.join(output_dir, skill_name),
            'zip',
            temp_dir
        )
        
        # Rename to .skill extension
        os.rename(
            os.path.join(output_dir, f"{skill_name}.zip"),
            package_path
        )
        
        print(f"Skill package created: {package_path}")
        return package_path
        
    finally:
        # Cleanup
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def main():
    """
    Main packaging function
    """
    skill_dir = "/Users/zhoutianhang/skills/skills/skills/comsol-automated-modeling"
    output_dir = "/Users/zhoutianhang/skills"
    
    if not os.path.exists(skill_dir):
        print(f"Error: Skill directory not found: {skill_dir}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        package_path = create_skill_package(skill_dir, output_dir)
        print(f"\nPackage created successfully!")
        print(f"Location: {package_path}")
        print(f"Size: {os.path.getsize(package_path) / 1024:.1f} KB")
        
    except Exception as e:
        print(f"Error creating package: {e}")

if __name__ == "__main__":
    main()