#!/usr/bin/env python3
"""
PyANSYS Clean Launcher - Working Version
Improved launcher script for the working PyANSYS implementation
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are available."""
    dependencies = {
        'tkinter': False,
        'pyvista': False,
        'ansys-dpf-post': False
    }
    
    # Check tkinter (usually built-in with Python)
    try:
        import tkinter
        dependencies['tkinter'] = True
    except ImportError:
        pass
    
    # Check PyVista
    try:
        import pyvista
        dependencies['pyvista'] = True
    except ImportError:
        pass
    
    # Check ANSYS DPF Post
    try:
        from ansys.dpf import post
        dependencies['ansys-dpf-post'] = True
    except ImportError:
        pass
    
    return dependencies

def install_missing_dependencies(missing_deps):
    """Offer to install missing dependencies."""
    if not missing_deps:
        return
    
    print(f"\\n⚠️  Missing dependencies: {', '.join(missing_deps)}")
    
    response = input("\\n❓ Would you like to install them automatically? (y/n): ").strip().lower()
    
    if response in ['y', 'yes']:
        print("\\n📦 Installing dependencies...")
        
        install_commands = {
            'pyvista': 'pip install pyvista',
            'ansys-dpf-post': 'pip install ansys-dpf-post'
        }
        
        for dep in missing_deps:
            if dep in install_commands:
                print(f"Installing {dep}...")
                try:
                    subprocess.run(install_commands[dep].split(), check=True)
                    print(f"✅ {dep} installed successfully")
                except subprocess.CalledProcessError:
                    print(f"❌ Failed to install {dep}")
    else:
        print("\\n💡 You can install them manually:")
        print("   pip install pyvista ansys-dpf-post")

def main():
    """Main launcher function."""
    print("🚀 PyANSYS Modern GUI Launcher (Working Version)")
    print("=" * 50)
    print("🔥 Now using working methods from viewer_fix.py!")
    print()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    deps = check_dependencies()
    
    missing_deps = [dep for dep, available in deps.items() if not available and dep != 'tkinter']
    
    if deps['tkinter']:
        print("✅ Tkinter: Available")
    else:
        print("❌ Tkinter: Not available (required)")
        print("   Install Python with tkinter support")
        return
    
    if deps['pyvista']:
        print("✅ PyVista: Available")
    else:
        print("❌ PyVista: Not available")
    
    if deps['ansys-dpf-post']:
        print("✅ ANSYS DPF Post: Available") 
    else:
        print("❌ ANSYS DPF Post: Not available")
    
    # Install missing dependencies if any
    if missing_deps:
        install_missing_dependencies(missing_deps)
    
    # Get the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(current_dir, "main.py")
    
    if not os.path.exists(main_script):
        print(f"❌ Main script not found: {main_script}")
        return
    
    print(f"\\n🎯 Launching PyANSYS GUI (Working Version)...")
    print(f"📁 Working directory: {current_dir}")
    print(f"🐍 Python executable: {sys.executable}")
    print("\\n🎉 Features available:")
    print("   ✅ RST file visualization (Von Mises, Total Deformation)")
    print("   ✅ MECHDAT file viewing")
    print("   ✅ 3D Interactive PyVista viewer")
    print("   ✅ Working methods from viewer_fix.py")
    
    try:
        # Change to the script directory
        os.chdir(current_dir)
        
        # Run the main script
        subprocess.run([sys.executable, main_script], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch application: {e}")
        print("\\n🔧 Troubleshooting tips:")
        print("   1. Make sure all dependencies are installed")
        print("   2. Check that Python is properly configured")
        print("   3. Try running 'python main.py' manually")
    except KeyboardInterrupt:
        print("\\n🛑 Application interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
