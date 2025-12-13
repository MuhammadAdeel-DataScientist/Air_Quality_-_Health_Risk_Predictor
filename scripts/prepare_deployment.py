# ============================================================================
# FILE 9: scripts/prepare_deployment.py
# Prepare project for deployment
# ============================================================================

"""
Deployment Preparation Script
Validates and prepares project for deployment
"""

import os
import sys
from pathlib import Path
import json

def print_header(msg):
    print("\n" + "="*70)
    print(f"  {msg}")
    print("="*70 + "\n")

def check_file(filepath, required=True):
    """Check if file exists"""
    path = Path(filepath)
    exists = path.exists()
    
    status = "✓" if exists else "✗"
    color = "\033[92m" if exists else "\033[91m"
    print(f"{color}{status}\033[0m {filepath}")
    
    if required and not exists:
        print(f"  ERROR: Required file missing!")
        return False
    return True

def check_model_size(model_path):
    """Check model file size"""
    path = Path(model_path)
    if path.exists():
        size_mb = path.stat().st_size / (1024 * 1024)
        print(f"  Model size: {size_mb:.2f} MB")
        
        if size_mb > 100:
            print(f"  ⚠️  Warning: Large model file (>100MB)")
            print(f"  Consider using Git LFS or external storage")
        return True
    return False

def validate_requirements():
    """Validate requirements.txt"""
    req_path = Path("requirements.txt")
    if not req_path.exists():
        return False
    
    with open(req_path) as f:
        requirements = f.read()
    
    essential = ['fastapi', 'uvicorn', 'pandas', 'numpy', 'xgboost']
    missing = [pkg for pkg in essential if pkg not in requirements.lower()]
    
    if missing:
        print(f"  ⚠️  Missing packages: {', '.join(missing)}")
        return False
    
    return True

def create_render_yaml():
    """Create render.yaml if it doesn't exist"""
    if Path("render.yaml").exists():
        print("✓ render.yaml already exists")
        return True
    
    config = """services:
  - type: web
    name: aqi-predictor-api
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: ENVIRONMENT
        value: production
    healthCheckPath: /health
"""
    
    with open("render.yaml", "w") as f:
        f.write(config)
    
    print("✓ Created render.yaml")
    return True

def main():
    print_header("Deployment Preparation Check")
    
    # Check required files
    print("1. Checking required files...")
    files_ok = all([
        check_file("requirements.txt"),
        check_file("backend/app/main.py"),
        check_file("data/models/best_model_gradientboosting.pkl"),
        check_file("data/processed/feature_sets.json"),
        check_file("data/processed/features_test.csv"),
    ])
    
    if not files_ok:
        print("\n❌ Missing required files!")
        sys.exit(1)
    
    # Check model size
    print("\n2. Checking model file...")
    check_model_size("data/models/best_model_gradientboosting.pkl")
    
    # Validate requirements
    print("\n3. Validating requirements.txt...")
    if validate_requirements():
        print("✓ All essential packages present")
    else:
        print("✗ Missing essential packages")
        sys.exit(1)
    
    # Create render.yaml
    print("\n4. Checking Render configuration...")
    create_render_yaml()
    
    # Check optional files
    print("\n5. Checking optional files...")
    check_file("Dockerfile", required=False)
    check_file("docker-compose.yml", required=False)
    check_file(".dockerignore", required=False)
    
    print_header("✅ Deployment Preparation Complete!")
    
    print("\n📋 Next Steps:")
    print("1. Push code to GitHub")
    print("2. Go to https://render.com")
    print("3. Connect your GitHub repository")
    print("4. Deploy as Web Service")
    print("5. Render will auto-detect render.yaml")
    print("\n🚀 Your API will be live in ~5 minutes!")

if __name__ == "__main__":
    main()
