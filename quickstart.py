#!/usr/bin/env python3
"""
Quick start script for the Task and Agent Management System.
This script helps you get started quickly by checking dependencies
and providing usage instructions.
"""
import sys
import subprocess


def check_python_version():
    """Check if Python version is adequate."""
    version = sys.version_info
    if version < (3, 6):
        print("❌ Python 3.6 or higher is required.")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    dependencies = {
        'PyQt5': 'PyQt5',
        'yaml': 'PyYAML'
    }
    
    missing = []
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            missing.append(package)
    
    return missing


def install_dependencies(packages):
    """Attempt to install missing dependencies."""
    print(f"\nAttempting to install: {', '.join(packages)}")
    print("This may take a moment...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
        print("\n✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Failed to install dependencies.")
        print("Please install manually using: pip install -r requirements.txt")
        return False


def main():
    """Main entry point."""
    print("=" * 70)
    print(" Task and Agent Management System - Quick Start")
    print("=" * 70)
    print()
    
    # Check Python version
    print("Checking Python version...")
    if not check_python_version():
        return 1
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    missing = check_dependencies()
    print()
    
    if missing:
        response = input(f"Install missing dependencies? (y/n): ").lower()
        if response == 'y':
            if not install_dependencies(missing):
                return 1
        else:
            print("\nPlease install dependencies before running the application.")
            print("Run: pip install -r requirements.txt")
            return 1
    
    print("=" * 70)
    print(" System Check Complete ✓")
    print("=" * 70)
    print()
    print("You can now run the application using:")
    print()
    print("  1. GUI Application:")
    print("     $ python gui.py")
    print()
    print("  2. Command-line Demo:")
    print("     $ python demo_cli.py")
    print()
    print("  3. Run Tests:")
    print("     $ python test_basic.py")
    print()
    print("For detailed usage instructions, see:")
    print("  - README.md - Overview and installation")
    print("  - USAGE_GUIDE.md - Step-by-step usage guide")
    print("  - GUI_FEATURES.md - GUI feature documentation")
    print()
    print("Quick Start Guide:")
    print("  1. Launch: python gui.py")
    print("  2. File → New Project")
    print("  3. Generate Tasks (e.g., 5 tasks)")
    print("  4. Generate Agents (e.g., 3 agents)")
    print("  5. Explore different tabs to visualize data")
    print("  6. Click on graph elements to see relationships")
    print("  7. Edit tasks/agents as needed")
    print("  8. Export project: File → Export Project")
    print()
    print("=" * 70)
    
    # Offer to run demo
    response = input("\nWould you like to run the command-line demo? (y/n): ").lower()
    if response == 'y':
        print("\nRunning demo...\n")
        try:
            subprocess.call([sys.executable, "demo_cli.py"])
        except Exception as e:
            print(f"Error running demo: {e}")
    
    print("\nThank you for using the Task and Agent Management System!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
