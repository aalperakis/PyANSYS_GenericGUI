"""
Summary:
This script opens a .mechdat file in ANSYS Mechanical using PyAnsys and launches a 3D interactive viewer.
Workflow:
Imports necessary modules (sys, os, shutil, App from ansys.mechanical.core).
Defines the path to the .mechdat file.
Creates an instance of the ANSYS Mechanical App (version=242).
Opens the specified .mechdat file.
Launches the 3D interactive view.
Waits for the user to press Enter to exit.
Attempts to delete the extracted temporary folder (*_Mech_Files) created during file loading.
If any error occurs, it prints the error and exits gracefully.
A.Alper Akis
"""

import sys
import os
import shutil


mechdat_path = r"C:\Users\ahmet.alper.ext\Desktop\PyANSYS_Clean\article_snippets\1a.mechdat"

try:
    from ansys.mechanical.core import App

    print(f"Opening file: {mechdat_path}")

    app = App(version=242)
    print("App instance created")

    app.open(mechdat_path)
    print("File opened successfully")

    print("Launching 3D view...")
    app.plot()
    print("Interactive view launched")

    input("Press Enter to exit...")

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
