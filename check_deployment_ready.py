#!/usr/bin/env python3
"""
Deployment Readiness Checker
Verifies that all required files exist for Render deployment
"""

import os
import sys

def check_file(filepath, description, required=True):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        status = "❌ MISSING" if required else "⚠️  OPTIONAL"
        print(f"{status} {description}: {filepath}")
        return required

def check_directory(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        files = len([f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))])
        print(f"✅ {description}: {dirpath} ({files} files)")
        return True
    else:
        print(f"❌ MISSING: {description}: {dirpath}")
        return False

def verify_procfile():
    """Verify Procfile content"""
    if os.path.exists('Procfile'):
        with open('Procfile', 'r') as f:
            content = f.read().strip()
            if 'gunicorn' in content and 'app:app' in content:
                print("✅ Procfile content is correct")
                return True
            else:
                print("⚠️  Procfile exists but content may be incorrect")
                print(f"   Current content: {content}")
                return False
    return False

def verify_requirements():
    """Verify requirements.txt has essential packages"""
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            content = f.read()
            essential = ['flask', 'gunicorn']
            missing = [pkg for pkg in essential if pkg.lower() not in content.lower()]
            if not missing:
                print("✅ requirements.txt contains essential packages")
                return True
            else:
                print(f"⚠️  requirements.txt missing: {', '.join(missing)}")
                return False
    return False

def main():
    print("=" * 70)
    print("🚀 RENDER DEPLOYMENT READINESS CHECK")
    print("=" * 70)
    
    all_good = True
    
    # Check required files
    print("\n📁 Checking Required Files:")
    print("-" * 70)
    all_good &= check_file('app.py', 'Main Flask application', required=True)
    all_good &= check_file('requirements.txt', 'Python dependencies', required=True)
    all_good &= check_file('Procfile', 'Process configuration', required=True)
    all_good &= check_file('runtime.txt', 'Python version', required=False)
    
    # Verify file contents
    print("\n📋 Verifying File Contents:")
    print("-" * 70)
    all_good &= verify_procfile()
    all_good &= verify_requirements()
    
    # Check directories
    print("\n📂 Checking Required Directories:")
    print("-" * 70)
    all_good &= check_directory('templates', 'Templates directory')
    all_good &= check_directory('static', 'Static files directory')
    
    # Check for app object in app.py
    print("\n🔍 Checking Flask App Structure:")
    print("-" * 70)
    if os.path.exists('app.py'):
        with open('app.py', 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if 'app = Flask(__name__)' in content or 'app=Flask' in content:
                print("✅ Flask app object found in app.py")
            else:
                print("⚠️  Flask app object not found - check app.py structure")
                all_good = False
    
    # Check sensitive files (should NOT be committed)
    print("\n🔒 Checking Security (Sensitive Files):")
    print("-" * 70)
    sensitive_files = ['env_file.txt', '.env', 'instance/students.db']
    for filepath in sensitive_files:
        if os.path.exists(filepath):
            print(f"⚠️  {filepath} exists - make sure it's in .gitignore")
        else:
            print(f"✅ {filepath} not in project (good)")
    
    # Final summary
    print("\n" + "=" * 70)
    if all_good:
        print("✅ ALL CHECKS PASSED! Your project is ready for Render deployment!")
        print("\n📋 Next Steps:")
        print("   1. Push to GitHub: git add . && git commit -m 'Ready for deployment' && git push")
        print("   2. Go to render.com and create a new Web Service")
        print("   3. Connect your GitHub repository")
        print("   4. Add environment variables (OPENAI_API_KEY, SECRET_KEY, FLASK_ENV)")
        print("   5. Deploy and wait for build to complete")
        print("\n📖 See RENDER_DEPLOYMENT_STEPS.md for detailed instructions")
        return 0
    else:
        print("❌ SOME ISSUES FOUND!")
        print("   Please fix the issues above before deploying to Render")
        return 1

if __name__ == '__main__':
    sys.exit(main())

