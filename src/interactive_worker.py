# A.Alper Akis interactive_worker.py
# https://embedding.examples.mechanical.docs.pyansys.com/examples/00_tips/tips_01.html#sphx-glr-examples-00-tips-tips-01-py

"""
interactive_worker.py

This script is launched as a subprocess from the GUI application to open and interact
with a .mechdat file in Ansys Mechanical's 3D interactive viewer.

It opens the specified file, launches the 3D view, and waits for the user to close it.
On exit, it attempts to clean up any temporary extraction folders.
"""
import sys
import os
import shutil
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for development and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
try:
    # Try to import PyAnsys
    from ansys.mechanical.core import App
    
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python interactive_worker.py <mechdat_file_path>")
        sys.exit(1)
    
    # Get the mechdat file path
    mechdat_path = sys.argv[1]
    print(f"Opening file: {mechdat_path}")
    
    # Create App instance
    app = App(version=242)
    print("App instance created")
    
    # Open the mechdat file
    app.open(mechdat_path)
    print("File opened successfully")
    
    # Launch interactive view
    print("Launching 3D view...")
    app.plot()  # Without blocking=True parameter
    print("Interactive view launched")
    
    # Keep the script alive to maintain the 3D view
    input("Press Enter to exit...")

    # Delete _Mech_Files folder if it exists
    directory = os.path.dirname(mechdat_path)
    base_name = os.path.splitext(os.path.basename(mechdat_path))[0]
    target_folder = os.path.join(directory, f"{base_name}_Mech_Files")
    if os.path.exists(target_folder) and os.path.isdir(target_folder):
        try:
            shutil.rmtree(target_folder)
            print(f"Deleted folder: {target_folder}")
        except Exception as e:
            print(f"Error deleting folder {target_folder}: {e}")
    
except Exception as e:
    print(f"Error: {e}")
    input("Press Enter to continue...")
    sys.exit(1)
