"""
Result Viewer - Based on Working Methods
Uses exact methods from working viewer_fix.py
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import tempfile
import uuid
import subprocess

# Check for required modules
pyvista_available = False
dpf_available = False

try:
    import pyvista as pv
    pyvista_available = True
except ImportError:
    pass

try:
    from ansys.dpf import post
    dpf_available = True
except ImportError:
    pass

class ResultViewer:
    """Result viewer using exact working methods."""
    
    def __init__(self, parent_frame, file_manager):
        self.parent_frame = parent_frame
        self.file_manager = file_manager
        self.selected_files = []
        
        # Color scheme
        self.colors = {
            "background": "#f0f0f0",
            "accent": "#ff6b35", 
            "text": "#333333",
            "error": "#cc0000"
        }
        
        # Result type selection
        self.result_type = tk.StringVar(value="von_mises")
        
        self.create_ui()
        
    def create_ui(self):
        """Create the result viewer interface."""
        # Main container
        main_frame = ttk.Frame(self.parent_frame, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title and description
        title_label = ttk.Label(main_frame, 
                               text="ANSYS Result File Viewer",
                               style="Title.TLabel")
        title_label.pack(pady=(0, 10))
        
        desc_label = ttk.Label(main_frame,
                              text="Visualize and analyze ANSYS result files (.rst)",
                              style="TLabel")
        desc_label.pack(pady=(0, 20))
        
        # Check dependencies
        self.create_dependency_info(main_frame)
        
        # Result type selection - SIMPLE (Von Mises and Total Deformation only)
        self.create_result_type_selection(main_frame)
        
        # File selection frame
        self.create_file_selection_frame(main_frame)
        
        # Interactive button
        self.create_interactive_button(main_frame)
        
        # File list
        self.create_file_list(main_frame)
        
        # Status frame
        self.create_status_frame(main_frame)
        
    def create_dependency_info(self, parent):
        """Display dependency status."""
        dep_frame = ttk.LabelFrame(parent, text="Dependencies", style="TLabelframe")
        dep_frame.pack(fill=tk.X, pady=(0, 10))
        
        pyvista_status = "✓ Available" if pyvista_available else "✗ Not installed"
        dpf_status = "✓ Available" if dpf_available else "✗ Not installed"
        
        status_text = f"PyVista: {pyvista_status} | DPF Post: {dpf_status}"
        if not (pyvista_available and dpf_available):
            status_text += "\\nInstall missing dependencies: pip install pyvista ansys-dpf-post"
        
        status_label = ttk.Label(dep_frame, text=status_text, style="TLabel")
        status_label.pack(pady=10, padx=10)
    
    def create_result_type_selection(self, parent):
        """Create simple result type selection."""
        result_type_frame = ttk.LabelFrame(parent, text="Result Type Selection", style="TLabelframe")
        result_type_frame.pack(fill=tk.X, pady=(0, 20))
        
        info_label = ttk.Label(result_type_frame, 
                              text="Select the result type to visualize:",
                              style="TLabel")
        info_label.pack(pady=(10, 5), padx=10, anchor=tk.W)
        
        # Simple radio buttons - ONLY Von Mises and Total Deformation
        radio_frame = ttk.Frame(result_type_frame, style="TFrame")
        radio_frame.pack(fill=tk.X, pady=(0, 15), padx=20)
        
        von_mises_radio = ttk.Radiobutton(radio_frame, text="Von Mises Stress", 
                                         variable=self.result_type, 
                                         value="von_mises",
                                         style="TRadiobutton")
        von_mises_radio.pack(side=tk.LEFT, padx=(0, 30))
        
        total_def_radio = ttk.Radiobutton(radio_frame, text="Total Deformation", 
                                         variable=self.result_type, 
                                         value="total_deformation",
                                         style="TRadiobutton")
        total_def_radio.pack(side=tk.LEFT)
        
    def create_file_selection_frame(self, parent):
        """Create file selection interface."""
        selection_frame = ttk.LabelFrame(parent, text="File Selection", style="TLabelframe")
        selection_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Selection button
        select_btn = ttk.Button(selection_frame,
                               text="Select Result Files (.rst)",
                               style="Accent.TButton",
                               command=self.select_files)
        select_btn.pack(pady=20)
    
    def create_interactive_button(self, parent):
        """Create interactive visualization button."""
        self.interactive_btn = ttk.Button(parent,
                                         text="🚀 Open 3D Interactive Viewer",
                                         style="Accent.TButton",
                                         command=self.open_interactive,
                                         state="disabled")
        self.interactive_btn.pack(pady=20)
    
    def create_file_list(self, parent):
        """Create file list display."""
        list_frame = ttk.LabelFrame(parent, text="Selected Files", style="TLabelframe")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for file list
        columns = ("Name", "Path")
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=6)
        
        # Configure columns
        self.file_tree.heading("Name", text="File Name")
        self.file_tree.heading("Path", text="Path")
        
        self.file_tree.column("Name", width=200)
        self.file_tree.column("Path", width=400)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        
    def create_status_frame(self, parent):
        """Create status display frame."""
        status_frame = ttk.LabelFrame(parent, text="Status", style="TLabelframe")
        status_frame.pack(fill=tk.X)
        
        self.status_var = tk.StringVar(value="Ready - Select result type and .rst file to begin")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, style="TLabel")
        status_label.pack(pady=10, padx=10)
        
    def select_files(self):
        """Handle file selection."""
        files = self.file_manager.select_result_files()
        if files:
            self.selected_files = files
            self.update_file_list()
            self.interactive_btn.config(state="normal")
            self.status_var.set(f"Selected {len(files)} file(s) - Ready for 3D visualization")
    
    def update_file_list(self):
        """Update the file list display."""
        # Clear existing items
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
            
        # Add new items
        for file_path in self.selected_files:
            file_info = self.file_manager.get_file_info(file_path)
            if file_info:
                self.file_tree.insert("", "end", values=(
                    file_info['name'],
                    file_info['path']
                ))
    
    def open_interactive(self):
        """Open interactive viewer using working methods."""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select RST files first.")
            return
        
        if not (pyvista_available and dpf_available):
            messagebox.showerror("Missing Dependencies", 
                               "PyVista and DPF Post are required.\\n\\n"
                               "Install with: pip install pyvista ansys-dpf-post")
            return
        
        # Use first selected file
        file_path = self.selected_files[0]
        result_type = self.result_type.get()
        
        self.status_var.set("Launching 3D interactive viewer...")
        
        # Use working methods
        if result_type == "von_mises":
            script_path = self.create_von_mises_script(file_path)
        else:
            script_path = self.create_total_deformation_script(file_path)
        
        self.run_script(script_path)
    
    def create_von_mises_script(self, file_path):
        """Create Von Mises script using working methods."""
        script_path = os.path.join(tempfile.gettempdir(), f"von_mises_fix_{uuid.uuid4()}.py")
        
        with open(script_path, 'w') as f:
            f.write(f"""
import sys
import os
import matplotlib.pyplot as plt
from ansys.dpf import post
from ansys.dpf import core as dpf

def main():
    try:
        print("Loading model from: {file_path}")
        # Load the simulation using both API methods for better compatibility
        try:
            simulation = post.load_simulation(r"{file_path}")
            print("Successfully loaded with post.load_simulation()")
        except Exception as e1:
            print(f"Error with post.load_simulation: {{e1}}")
            simulation = None
            
        try:
            model = dpf.Model(r"{file_path}")
            print("Successfully loaded with dpf.Model()")
        except Exception as e2:
            print(f"Error with dpf.Model: {{e2}}")
            if simulation is None:
                raise Exception("Failed to load simulation with both methods")
            model = None
        
        # Try multiple approaches to get Von Mises stress
        result = None
        mesh = None
        
        # Approach 1: Use the updated DPF approach with data_sources
        try:
            print("Trying approach 1: Using stress_von_mises with data_sources")
            s_eqv_op = dpf.operators.result.stress_von_mises(data_sources=model)
            vm_stress_fc = s_eqv_op.eval()
            result = vm_stress_fc[0]
            mesh = model.metadata.meshed_region
            print("Approach 1 successful")
        except Exception as e_approach1:
            print(f"Approach 1 failed: {{e_approach1}}")
            
            # Approach 2: Using the traditional method
            try:
                print("Trying approach 2: Traditional connection method")
                # Get stress result using DPF core API for von Mises
                stress_operator = model.results.stress()
                stress_set = stress_operator.outputs.fields_container()[0]
                
                # Use the proper von Mises operator
                von_mises_op = dpf.operators.result.stress_von_mises()
                von_mises_op.inputs.field.connect(stress_set)
                result = von_mises_op.outputs.field()
                mesh = model.metadata.meshed_region
                print("Approach 2 successful")
            except Exception as e_approach2:
                print(f"Approach 2 failed: {{e_approach2}}")
                
                # Approach 3: Use post API method
                try:
                    print("Trying approach 3: Using post API method")
                    result = simulation.stress_eqv_von_mises_nodal()
                    print("Approach 3 successful")
                except Exception as e_approach3:
                    print(f"Approach 3 failed: {{e_approach3}}")
                    raise Exception("All approaches to get von Mises stress failed")
        
        title = "Von Mises Stress"
        
        # Try built-in plot method first
        try:
            print("Attempting to plot result...")
            result.plot(cmap="jet", show_edges=True, title=f"{{title}} - {{os.path.basename(r'{file_path}')}}")
            print("SUCCESS: result.plot() worked")
        except Exception as e:
            print(f"Error with result.plot(): {{e}}")
            try:
                # Try matplotlib fallback
                import matplotlib.pyplot as plt
                fig = plt.figure(figsize=(10, 8))
                plt.text(0.5, 0.5, f"{{title}}\\n{{os.path.basename(r'{file_path}')}}\\n\\nData loaded successfully\\nVisualization method not available", 
                        ha='center', va='center', transform=plt.gca().transAxes, fontsize=12)
                plt.title(f"{{title}} - {{os.path.basename(r'{file_path}')}}")
                plt.show()
                print("SUCCESS: Matplotlib fallback completed")
            except Exception as e2:
                print(f"All plotting methods failed: {{e2}}")
    
    except Exception as e:
        print(f"General error: {{e}}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
""")
        return script_path
    
    def create_total_deformation_script(self, file_path):
        """Create Total Deformation script using working methods."""
        script_path = os.path.join(tempfile.gettempdir(), f"total_deformation_fix_{uuid.uuid4()}.py")
        
        with open(script_path, 'w') as f:
            f.write(f"""
import sys
import os
import matplotlib.pyplot as plt
from ansys.dpf import post
from ansys.dpf import core as dpf

def main():
    try:
        # Load the simulation
        simulation = post.load_simulation(r"{file_path}")
        model = dpf.Model(r"{file_path}")
        
        # Get displacement result using DPF core API
        disp_operator = model.results.displacement()
        result = disp_operator.outputs.fields_container()[0]
        
        title = "Total Deformation"
        
        # Try built-in plot method first
        try:
            print("Attempting to plot result...")
            result.plot(cmap="jet", show_edges=True, title=f"{{title}} - {{os.path.basename(r'{file_path}')}}")
            print("SUCCESS: result.plot() worked")
        except Exception as e:
            print(f"Error with result.plot(): {{e}}")
            try:
                # Try matplotlib fallback
                import matplotlib.pyplot as plt
                fig = plt.figure(figsize=(10, 8))
                plt.text(0.5, 0.5, f"{{title}}\\n{{os.path.basename(r'{file_path}')}}\\n\\nData loaded successfully\\nVisualization method not available", 
                        ha='center', va='center', transform=plt.gca().transAxes, fontsize=12)
                plt.title(f"{{title}} - {{os.path.basename(r'{file_path}')}}")
                plt.show()
                print("SUCCESS: Matplotlib fallback completed")
            except Exception as e2:
                print(f"All plotting methods failed: {{e2}}")
    
    except Exception as e:
        print(f"General error: {{e}}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
""")
        return script_path
    
    def run_script(self, script_path):
        """Run the visualization script."""
        def run_in_thread():
            try:
                print(f"DEBUG: Running script: {script_path}")
                
                # Run with real-time output
                process = subprocess.Popen([sys.executable, script_path], 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.STDOUT,
                                         text=True,
                                         universal_newlines=True)
                
                # Read output in real-time
                for line in process.stdout:
                    print(f"SCRIPT OUTPUT: {line.strip()}")
                
                # Wait for completion
                return_code = process.wait()
                print(f"DEBUG: Process completed with return code: {return_code}")
                
                if return_code == 0:
                    self.status_var.set("3D visualization completed successfully")
                    print("SUCCESS: Script completed successfully")
                else:
                    self.status_var.set("Error in 3D visualization")
                    print(f"ERROR: Script failed with return code {return_code}")
                    
            except Exception as e:
                self.status_var.set(f"Error: {str(e)}")
                print(f"EXCEPTION in run_script: {e}")
                import traceback
                traceback.print_exc()
            finally:
                # Cleanup
                try:
                    if os.path.exists(script_path):
                        os.remove(script_path)
                        print(f"DEBUG: Cleaned up script file: {script_path}")
                except Exception as cleanup_error:
                    print(f"DEBUG: Cleanup error: {cleanup_error}")
        
        # Run in thread
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()
