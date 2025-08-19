#!/usr/bin/env python3
"""
Setup script to fix Streamlit Cloud deployment issues
"""

import os
import shutil
import sys
from pathlib import Path

def fix_deployment_structure():
    """Fix common deployment structure issues"""
    print("🔧 Fixing deployment structure...\n")
    
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Check if we're in a nested structure
    if "Tender Optimization" in str(current_dir):
        print("⚠️  Detected nested 'Tender Optimization' directory structure")
        print("   This might be causing the 'Optimization/requirements.txt' error")
        
        # Create a flattened structure
        parent_dir = current_dir.parent
        print(f"   Consider moving files to: {parent_dir}")
    
    # Ensure requirements.txt is clean
    requirements_files = [
        "requirements.txt",
        "requirements_clean.txt"
    ]
    
    for req_file in requirements_files:
        if os.path.exists(req_file):
            print(f"✅ Found {req_file}")
            with open(req_file, 'r') as f:
                content = f.read()
                if "streamlit" in content.lower():
                    print(f"   ✅ Streamlit dependency found in {req_file}")
                else:
                    print(f"   ❌ Streamlit not found in {req_file}")
    
    # Check for problematic files/folders
    problematic_items = [
        "Optimization",
        "Tender Optimization/Optimization"
    ]
    
    for item in problematic_items:
        if os.path.exists(item):
            print(f"⚠️  Found problematic path: {item}")
            print("   This might be causing deployment issues")
    
    # Create deployment-ready structure
    deployment_files = {
        "dashboard.py": "Main Streamlit application",
        "requirements.txt": "Dependencies file", 
        "components/": "Application modules directory",
        ".streamlit/config.toml": "Streamlit configuration"
    }
    
    print("\n📋 Deployment checklist:")
    all_good = True
    
    for file_path, description in deployment_files.items():
        if os.path.exists(file_path):
            print(f"   ✅ {file_path} - {description}")
        else:
            print(f"   ❌ {file_path} - {description} (MISSING)")
            all_good = False
    
    if all_good:
        print("\n🎉 All deployment files are present!")
    else:
        print("\n⚠️  Some files are missing. Please ensure all required files exist.")
    
    # Generate clean requirements
    print("\n🧹 Creating clean requirements file...")
    clean_requirements = [
        "streamlit>=1.28.0",
        "pandas>=2.0.0", 
        "numpy>=1.24.0",
        "plotly>=5.15.0",
        "pulp>=2.7.0",
        "scikit-learn>=1.3.0",
        "openpyxl>=3.1.0",
        "xlrd>=2.0.0"
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(clean_requirements) + "\n")
    
    print("✅ Clean requirements.txt created")
    
    # Deployment instructions
    print("""
🚀 DEPLOYMENT INSTRUCTIONS:

1. REPOSITORY STRUCTURE:
   Your GitHub repo should have files at the ROOT level:
   
   your-repo/
   ├── dashboard.py          ← Main file
   ├── requirements.txt      ← Dependencies  
   ├── components/           ← Modules
   └── .streamlit/          ← Config (optional)

2. STREAMLIT CLOUD SETTINGS:
   - Repository: your-github-repo
   - Branch: main
   - Main file path: dashboard.py
   - Python version: 3.9+ (default)
   - Advanced settings: LEAVE BLANK

3. COMMON ISSUES:
   - Do NOT put files in "Tender Optimization" subfolder
   - Do NOT specify requirements path manually
   - Make sure dashboard.py is at repo root

4. IF YOU STILL GET "Optimization/requirements.txt" ERROR:
   - Delete your Streamlit Cloud app
   - Create a NEW repository with files at ROOT level
   - Redeploy with new repository
   
The error suggests your repo structure has extra folder nesting!
""")

if __name__ == "__main__":
    fix_deployment_structure()
