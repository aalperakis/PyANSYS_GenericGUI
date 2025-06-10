"""
Summary: RST Result File Viewer with GUI and PyVista/DPF Integration
This Python script provides a complete solution for viewing ANSYS .rst result files using a graphical interface built with Tkinter, combined with PyVista and Ansys DPF Post for visualization.
Key Components:
GUI Viewer (Tkinter):
Allows users to select multiple .rst files.
Users can choose between Von Mises Stress and Total Deformation.
Includes interactive status updates and a launch button to view results.
Interactive Viewer Backend:
Upon launching, a temporary Python script is created and executed as a subprocess.
This worker script loads the RST file, extracts the selected result (stress or deformation), and visualizes it using PyVista.
Includes fallback plotting logic in case direct plotting fails.
Standalone Visualization Examples:
direct_rst_example(): A reusable code snippet for viewing a single RST file.
open_rst_with_time_steps(): Demonstrates how to handle multiple time steps.
advanced_rst_visualization(): Shows multiple result types in subplots (Von Mises, Displacement, Principal Stress, etc.).
create_simple_integration(): A minimal file dialog-based viewer for quick integration.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading
import subprocess
import sys
import tempfile

class ResultFileViewer:
    """Working RST result file viewer using PyVista and DPF."""
    
    def __init__(self, root):
        self.root = root
        self.current_files = []
        self.result_type = tk.StringVar(value="Von Mises Stress")
        self.create_ui()
    
    def create_ui(self):
        """Create the result viewer interface."""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="ANSYS RST Result File Viewer",
                               font=("Segoe UI", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Result type selection
        type_frame = ttk.LabelFrame(main_frame, text="Result Type")
        type_frame.pack(fill=tk.X, pady=(0, 20))
        
        type_combo = ttk.Combobox(type_frame, textvariable=self.result_type,
                                 values=["Von Mises Stress", "Total Deformation"],
                                 state="readonly")
        type_combo.pack(pady=20)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="File Selection")
        file_frame.pack(fill=tk.X, pady=(0, 20))
        
        select_btn = ttk.Button(file_frame,
                               text="Select RST Files",
                               command=self.select_files)
        select_btn.pack(pady=20)
        
        # File list
        self.file_listbox = tk.Listbox(file_frame, height=4)
        self.file_listbox.pack(fill=tk.X, pady=(0, 10))
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        self.view_btn = ttk.Button(button_frame,
                                  text="🚀 Open 3D Interactive Viewer",
                                  command=self.open_viewer,
                                  state=tk.DISABLED)
        self.view_btn.pack()
        
        # Status
        self.status_var = tk.StringVar(value="Ready - Select result type and files")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.pack(pady=(20, 0))
    
    def select_files(self):
        """Select RST result files."""
        file_paths = filedialog.askopenfilenames(
            title="Select RST Result Files",
            filetypes=[("RST Files", "*.rst"), ("All Files", "*.*")]
        )
        
        if file_paths:
            self.current_files = list(file_paths)
            self.update_file_list()
            self.view_btn.config(state=tk.NORMAL)
            self.status_var.set(f"Selected {len(file_paths)} file(s) - Ready to view")
    
    def update_file_list(self):
        """Update the file list display."""
        self.file_listbox.delete(0, tk.END)
        for file_path in self.current_files:
            filename = os.path.basename(file_path)
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            self.file_listbox.insert(tk.END, f"{filename} ({size_mb:.1f} MB)")
    
    def open_viewer(self):
        """Open the result viewer."""
        if not self.current_files:
            messagebox.showwarning("No Files", "Please select files first.")
            return
        
        # Use first selected file
        selected_file = self.current_files[0]
        result_type = self.result_type.get()
        
        self.status_var.set(f"Opening {result_type} visualization...")
        
        # Run in separate thread
        thread = threading.Thread(target=self.launch_viewer, args=(selected_file, result_type))
        thread.daemon = True
        thread.start()
    
    def launch_viewer(self, file_path, result_type):
        """Launch the PyVista result viewer."""
        try:
            # Create the working result viewer script
            worker_content = f'''
# Working RST Result Viewer Worker Script
import sys
import os

try:
    # Import required modules
    import pyvista as pv
    from ansys.dpf import post
    print("PyVista and DPF Post imported successfully")
    
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python script.py <rst_file_path> [result_type]")
        sys.exit(1)
    
    # Get parameters
    rst_path = sys.argv[1]
    result_type = "{result_type}" if len(sys.argv) < 3 else sys.argv[2]
    
    print(f"Opening RST file: {{rst_path}}")
    print(f"Result type: {{result_type}}")
    
    # Load the simulation
    simulation = post.load_simulation(rst_path)
    print("Simulation loaded successfully")
    
    # Get the result based on type
    if result_type == "Von Mises Stress":
        try:
            result = simulation.stress_eqv_von_mises_nodal()
            title = "Von Mises Stress"
            unit = "Pa"
            print("SUCCESS: Von Mises stress obtained")
        except Exception as e:
            print(f"Failed to get Von Mises stress: {{e}}")
            sys.exit(1)
    else:  # Total Deformation
        try:
            result = simulation.displacement(norm=True)
            title = "Total Deformation"
            unit = "m"
            print("SUCCESS: Total deformation obtained")
        except Exception as e:
            print(f"Failed to get Total Deformation: {{e}}")
            sys.exit(1)
    
    print(f"Result obtained successfully: {{title}}")
    
    # Try direct plotting first (simplest method)
    try:
        print("Attempting direct result plotting...")
        result.plot(cmap="jet", show_edges=True, 
                   window_size=[1024, 768],
                   title=f"{{title}} - {{os.path.basename(rst_path)}}")
        print("SUCCESS: Direct result plotting worked!")
        
    except Exception as e1:
        print(f"Direct plotting failed: {{e1}}")
        print("Trying manual PyVista plotting...")
        
        # Manual PyVista plotting as fallback
        try:
            # Get mesh
            mesh = simulation.mesh
            
            # Get mesh grid
            try:
                grid = mesh.grid
                print("Got mesh grid using .grid property")
            except:
                try:
                    grid = mesh.to_pyvista()
                    print("Got mesh grid using .to_pyvista() method")
                except Exception as e:
                    print(f"Failed to get mesh grid: {{e}}")
                    sys.exit(1)
            
            # Add result data to grid
            grid[title] = result.data
            print(f"Added result data to grid: {{len(result.data)}} points")
            
            # Create plotter
            plotter = pv.Plotter()
            plotter.add_mesh(grid, scalars=title, show_edges=True, cmap="jet")
            plotter.add_scalar_bar(title=f"{{title}} ({{unit}})")
            plotter.add_axes()
            plotter.window_size = [1024, 768]
            plotter.title = f"{{title}} - {{os.path.basename(rst_path)}}"
            
            print("PyVista visualization configured, showing...")
            plotter.show()
            print("SUCCESS: Manual PyVista plotting worked!")
            
        except Exception as e2:
            print(f"Manual plotting also failed: {{e2}}")
            sys.exit(1)
    
    print("RST visualization completed successfully")

except Exception as e:
    print(f"Error in RST viewer: {{e}}")
    import traceback
    traceback.print_exc()
    input("Press Enter to continue...")
    sys.exit(1)
'''
            
            # Write to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(worker_content)
                temp_script = f.name
            
            # Launch subprocess
            process = subprocess.run([
                sys.executable, temp_script, file_path, result_type
            ], capture_output=True, text=True)
            
            # Clean up temp file
            try:
                os.unlink(temp_script)
            except:
                pass
            
            if process.returncode == 0:
                self.root.after(0, self.on_success)
            else:
                error_msg = process.stderr or process.stdout
                self.root.after(0, lambda: self.on_error(error_msg))
                
        except Exception as e:
            self.root.after(0, lambda: self.on_error(str(e)))
    
    def on_success(self):
        """Handle successful completion."""
        self.status_var.set("Result visualization completed successfully")
        messagebox.showinfo("Success", "RST result viewer completed!")
    
    def on_error(self, error_msg):
        """Handle errors."""
        self.status_var.set("Error launching viewer")
        messagebox.showerror("Error", f"Failed to launch viewer:\\n\\n{error_msg}")

# Standalone PyVista/DPF code example
def direct_rst_example():
    """
    Direct PyVista and DPF usage example for RST files.
    This is the core code for opening and viewing RST result files.
    """
    
    example_code = '''
# Direct PyVista and DPF RST Example
import pyvista as pv
from ansys.dpf import post
import os

def open_rst_file(file_path, result_type="Von Mises Stress"):
    """Open and view an RST result file with PyVista and DPF."""
    
    try:
        print(f"Opening RST file: {file_path}")
        print(f"Result type: {result_type}")
        
        # Load simulation with DPF Post
        simulation = post.load_simulation(file_path)
        print("Simulation loaded successfully")
        
        # Get the desired result
        if result_type == "Von Mises Stress":
            # Von Mises stress
            result = simulation.stress_eqv_von_mises_nodal()
            title = "Von Mises Stress"
            unit = "Pa"
        else:
            # Total deformation
            result = simulation.displacement(norm=True)
            title = "Total Deformation" 
            unit = "m"
        
        print(f"Result obtained: {title}")
        
        # Method 1: Direct plotting (easiest)
        try:
            result.plot(cmap="jet", show_edges=True,
                       window_size=[1024, 768],
                       title=f"{title} - {os.path.basename(file_path)}")
            return True
            
        except Exception:
            # Method 2: Manual PyVista plotting
            print("Trying manual PyVista plotting...")
            
            # Get mesh
            mesh = simulation.mesh
            grid = mesh.grid  # or mesh.to_pyvista()
            
            # Add result data
            grid[title] = result.data
            
            # Create plotter
            plotter = pv.Plotter()
            plotter.add_mesh(grid, scalars=title, show_edges=True, cmap="jet")
            plotter.add_scalar_bar(title=f"{title} ({unit})")
            plotter.add_axes()
            plotter.window_size = [1024, 768]
            plotter.title = f"{title} - {os.path.basename(file_path)}"
            
            # Show visualization
            plotter.show()
            return True
        
    except Exception as e:
        print(f"Error opening RST file: {e}")
        import traceback
        traceback.print_exc()
        return False

# Example of working with multiple time steps
def open_rst_with_time_steps(file_path):
    """Example showing how to handle multiple time steps."""
    
    try:
        simulation = post.load_simulation(file_path)
        
        # Get available time steps
        time_freq_support = simulation.time_freq_support
        print(f"Available time steps: {len(time_freq_support.time_frequencies)}")
        
        # Get results for specific time step (last step)
        last_step = len(time_freq_support.time_frequencies) - 1
        
        # Von Mises stress at last time step
        stress = simulation.stress_eqv_von_mises_nodal()
        stress_last = stress.get_data_at_field(last_step)
        
        # Plot the result
        stress_last.plot(cmap="jet", show_edges=True,
                        title=f"Von Mises Stress - Step {last_step}")
        
        return True
        
    except Exception as e:
        print(f"Error with time steps: {e}")
        return False

# Advanced example with multiple result types
def advanced_rst_visualization(file_path):
    """Advanced example showing multiple result types."""
    
    try:
        simulation = post.load_simulation(file_path)
        
        # Create subplot layout
        plotter = pv.Plotter(shape=(2, 2))
        
        # Von Mises stress
        try:
            stress = simulation.stress_eqv_von_mises_nodal()
            mesh = simulation.mesh.grid
            mesh["Stress"] = stress.data
            
            plotter.subplot(0, 0)
            plotter.add_mesh(mesh, scalars="Stress", cmap="jet")
            plotter.add_scalar_bar(title="Von Mises Stress (Pa)")
            plotter.add_text("Von Mises Stress")
        except Exception as e:
            print(f"Could not add stress: {e}")
        
        # Total deformation
        try:
            displacement = simulation.displacement(norm=True)
            mesh = simulation.mesh.grid
            mesh["Displacement"] = displacement.data
            
            plotter.subplot(0, 1)
            plotter.add_mesh(mesh, scalars="Displacement", cmap="viridis")
            plotter.add_scalar_bar(title="Total Deformation (m)")
            plotter.add_text("Total Deformation")
        except Exception as e:
            print(f"Could not add displacement: {e}")
        
        # X displacement
        try:
            disp_x = simulation.displacement(components=["X"])
            mesh = simulation.mesh.grid
            mesh["Disp_X"] = disp_x.data
            
            plotter.subplot(1, 0)
            plotter.add_mesh(mesh, scalars="Disp_X", cmap="coolwarm")
            plotter.add_scalar_bar(title="X Displacement (m)")
            plotter.add_text("X Displacement")
        except Exception as e:
            print(f"Could not add X displacement: {e}")
        
        # Principal stress
        try:
            principal = simulation.stress_principal_nodal()[0]  # First principal
            mesh = simulation.mesh.grid
            mesh["Principal"] = principal.data
            
            plotter.subplot(1, 1)
            plotter.add_mesh(mesh, scalars="Principal", cmap="plasma")
            plotter.add_scalar_bar(title="Principal Stress (Pa)")
            plotter.add_text("Principal Stress")
        except Exception as e:
            print(f"Could not add principal stress: {e}")
        
        # Show all subplots
        plotter.show()
        return True
        
    except Exception as e:
        print(f"Error in advanced visualization: {e}")
        return False

# Example usage
if __name__ == "__main__":
    # Replace with your RST file path
    rst_file = "path/to/your/file.rst"
    
    if os.path.exists(rst_file):
        print("Testing basic RST visualization...")
        success = open_rst_file(rst_file, "Von Mises Stress")
        
        if success:
            print("\\nTesting time steps...")
            open_rst_with_time_steps(rst_file)
            
            print("\\nTesting advanced visualization...")
            advanced_rst_visualization(rst_file)
    else:
        print(f"File not found: {rst_file}")
    '''
    
    return example_code

# Simple integration example
def create_simple_integration():
    """Create a simple integration example."""
    
    simple_code = '''
# Simple RST Viewer Integration
import tkinter as tk
from tkinter import filedialog, messagebox
import pyvista as pv
from ansys.dpf import post

def simple_rst_viewer():
    """Simple RST file viewer with file dialog."""
    
    # Create file dialog
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    # Select RST file
    file_path = filedialog.askopenfilename(
        title="Select RST Result File",
        filetypes=[("RST Files", "*.rst"), ("All Files", "*.*")]
    )
    
    if file_path:
        try:
            # Load simulation
            simulation = post.load_simulation(file_path)
            
            # Get Von Mises stress
            stress = simulation.stress_eqv_von_mises_nodal()
            
            # Direct plotting
            stress.plot(cmap="jet", show_edges=True,
                       window_size=[1024, 768],
                       title=f"Von Mises Stress - {file_path}")
            
            messagebox.showinfo("Success", "RST file visualized successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open RST file:\\n{e}")
    
    root.destroy()

# Run the simple viewer
if __name__ == "__main__":
    simple_rst_viewer()
    '''
    
    return simple_code

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("RST Result Viewer Example")
    root.geometry("500x500")
    
    viewer = ResultFileViewer(root)
    root.mainloop()
    
    # Print code examples
    print("\\n" + "="*60)
    print("DIRECT PYVISTA/DPF RST EXAMPLE:")
    print("="*60)
    print(direct_rst_example())
    
    print("\\n" + "="*60)
    print("SIMPLE INTEGRATION EXAMPLE:")
    print("="*60)
    print(create_simple_integration())
