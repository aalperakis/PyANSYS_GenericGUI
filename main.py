#!/usr/bin/env python3
"""
PyANSYS Modern GUI Application - Main Entry Point (Working Version)
A comprehensive visualization tool for ANSYS Mechanical and result files.
Uses working methods from viewer_fix.py for RST visualization.

Author: A. Alper Akis
Version: 2.1 - Working Version
"""

import os
import sys
import tkinter as tk

def setup_path():
    """Add src directory to Python path for imports."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

def main():
    """Main application entry point."""
    print("Starting PyANSYS Modern GUI Application (Working Version)...")
    print("Using working methods from viewer_fix.py for RST visualization")
    
    # Setup import paths
    setup_path()
    
    try:
        from gui_application import PyANSYSApplication
        
        # Create root window
        root = tk.Tk()
        
        # Initialize application
        app = PyANSYSApplication(root)
        
        print("✅ Application initialized successfully")
        print("📋 Features:")
        print("   - RST file visualization (Von Mises Stress, Total Deformation)")
        print("   - MECHDAT file viewing")
        print("   - 3D Interactive PyVista viewer")
        print("\n🚀 Starting GUI...")
        
        # Start main loop
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
