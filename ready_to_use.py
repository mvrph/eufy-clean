#!/usr/bin/env python3
"""
Quick verification script - checks if everything is ready to use

This script verifies:
1. All dependencies are installed
2. Credentials are set up
3. Library can be imported

Run this to confirm you're ready to go!
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required = {
        'aiohttp': 'aiohttp',
        'paho.mqtt': 'paho-mqtt',
        'google.protobuf': 'protobuf',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing.append(package)
    
    return missing

def check_credentials():
    """Check if credentials are set up"""
    print("\n🔍 Checking credentials...")
    
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        username = os.getenv('EUFY_USERNAME')
        password = os.getenv('EUFY_PASSWORD')
        
        if username and password:
            print(f"  ✅ Username: {username}")
            print(f"  ✅ Password: {'*' * len(password)}")
            return True
        else:
            print("  ❌ Credentials not found in .env file")
            print("\n  Create a .env file with:")
            print("    EUFY_USERNAME=your-email@example.com")
            print("    EUFY_PASSWORD=your-password")
            return False
    except Exception as e:
        print(f"  ⚠️  Could not check credentials: {e}")
        return False

def check_library():
    """Check if the library can be imported"""
    print("\n🔍 Checking library...")
    
    try:
        from custom_components.robovac_mqtt.EufyClean import EufyClean
        print("  ✅ EufyClean can be imported")
        return True
    except Exception as e:
        print(f"  ❌ Cannot import library: {e}")
        return False

def main():
    print("=" * 60)
    print("Eufy Clean - Ready Check")
    print("=" * 60)
    print()
    
    # Check dependencies
    missing_deps = check_dependencies()
    
    # Check library
    library_ok = check_library()
    
    # Check credentials
    credentials_ok = check_credentials()
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print("\nInstall them with:")
        print(f"  pip install {' '.join(missing_deps)}")
        return False
    
    if not library_ok:
        print("❌ Library import failed")
        return False
    
    if not credentials_ok:
        print("⚠️  Credentials not set up (but library is ready)")
        print("\nYou can still test the library by passing credentials directly:")
        print("  eufy_clean = EufyClean('your-email', 'your-password')")
        return False
    
    print("✅ Everything is ready!")
    print("\nYou can now use the library:")
    print("  python3 standalone_example.py")
    print("\nOr use it in your own code:")
    print("  from custom_components.robovac_mqtt.EufyClean import EufyClean")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
