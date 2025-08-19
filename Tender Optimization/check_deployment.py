#!/usr/bin/env python3
"""
Test script to verify deployment readiness
"""

import sys
import os
from pathlib import Path

def check_deployment_readiness():
    """Check if the project is ready for Streamlit deployment"""
    
    print("🔍 Checking deployment readiness...\n")
    
    issues = []
    
    # Check if dashboard.py exists
    if not os.path.exists("dashboard.py"):
        issues.append("❌ dashboard.py not found in current directory")
    else:
        print("✅ dashboard.py found")
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        issues.append("❌ requirements.txt not found in current directory")
    else:
        print("✅ requirements.txt found")
        
        # Check requirements.txt content
        with open("requirements.txt", "r") as f:
            content = f.read()
            if "streamlit" in content.lower():
                print("✅ streamlit found in requirements.txt")
            else:
                issues.append("⚠️ streamlit not found in requirements.txt")
    
    # Check components directory
    if not os.path.exists("components"):
        issues.append("❌ components directory not found")
    else:
        print("✅ components directory found")
    
    # Check for common deployment issues
    if os.path.exists("Optimization"):
        issues.append("⚠️ 'Optimization' folder found - this might cause deployment path issues")
    
    # Test imports
    try:
        sys.path.append(os.getcwd())
        from components import data_loader
        print("✅ Component imports working")
    except ImportError as e:
        issues.append(f"❌ Import error: {e}")
    
    print("\n" + "="*50)
    
    if issues:
        print("🚨 Issues found:")
        for issue in issues:
            print(f"   {issue}")
        print("\n💡 Please fix these issues before deploying.")
        return False
    else:
        print("🎉 All checks passed! Ready for deployment.")
        print("\n📋 Deployment checklist:")
        print("   1. Push code to GitHub")
        print("   2. Go to share.streamlit.io")
        print("   3. Connect your repository")
        print("   4. Set main file path: dashboard.py")
        print("   5. Leave requirements path blank")
        print("   6. Deploy!")
        return True

if __name__ == "__main__":
    check_deployment_readiness()
