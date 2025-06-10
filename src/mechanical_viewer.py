"""
Simple Mechanical Viewer - Direct Call to Original Worker
No error handling, just calls your working PyANSYS code directly.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading

class MechanicalViewer:
    """Simple mechanical viewer - direct call to working PyANSYS."""
    
    def __init__(self, parent_frame, file_manager):
        self.parent_frame = parent_frame
        self.file_manager = file_manager
        self.selected_files = []
        
        self.create_ui()
        
    def create_ui(self):
        """Create the mechanical viewer interface."""
        # Main container
        main_frame = ttk.Frame(self.parent_frame, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title and description
        title_label = ttk.Label(main_frame, 
                               text="ANSYS Mechanical File Viewer",
                               style="Title.TLabel")
        title_label.pack(pady=(0, 10))
        
        desc_label = ttk.Label(main_frame,
                              text="Open and view ANSYS Mechanical files (.mechdat)",
                              style="TLabel")
        desc_label.pack(pady=(0, 20))
        
        # File selection frame
        self.create_file_selection_frame(main_frame)
        
        # File list frame
        self.create_file_list_frame(main_frame)
        
        # Action buttons frame
        self.create_action_buttons_frame(main_frame)
        
        # Status frame
        self.create_status_frame(main_frame)
        
    def create_file_selection_frame(self, parent):
        """Create file selection interface."""
        selection_frame = ttk.LabelFrame(parent, text="File Selection", style="TLabelframe")
        selection_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Selection button
        select_btn = ttk.Button(selection_frame,
                               text="Select Mechanical Files (.mechdat)",
                               style="Accent.TButton",
                               command=self.select_files)
        select_btn.pack(pady=20)
        
    def create_file_list_frame(self, parent):
        """Create file list display."""
        list_frame = ttk.LabelFrame(parent, text="Selected Files", style="TLabelframe")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create treeview for file list
        columns = ("Name", "Path", "Size")
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        
        # Configure columns
        self.file_tree.heading("Name", text="File Name")
        self.file_tree.heading("Path", text="Path")
        self.file_tree.heading("Size", text="Size (MB)")
        
        self.file_tree.column("Name", width=200)
        self.file_tree.column("Path", width=400)
        self.file_tree.column("Size", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        
    def create_action_buttons_frame(self, parent):
        """Create action buttons."""
        buttons_frame = ttk.Frame(parent, style="TFrame")
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Single interactive view button
        self.view_btn = ttk.Button(buttons_frame,
                                  text="Open Interactive 3D View",
                                  style="Accent.TButton",
                                  command=self.open_interactive_view,
                                  state=tk.DISABLED)
        self.view_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        clear_btn = ttk.Button(buttons_frame,
                              text="Clear Selection",
                              style="TButton",
                              command=self.clear_selection)
        clear_btn.pack(side=tk.LEFT)
        
    def create_status_frame(self, parent):
        """Create status display frame."""
        status_frame = ttk.LabelFrame(parent, text="Status", style="TLabelframe")
        status_frame.pack(fill=tk.X)
        
        self.status_var = tk.StringVar(value="Ready - Select a .mechdat file to begin")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, style="TLabel")
        status_label.pack(pady=10, padx=10)
        
    def select_files(self):
        """Handle file selection."""
        files = self.file_manager.select_mechanical_files()
        if files:
            self.selected_files = files
            self.update_file_list()
            self.view_btn.config(state=tk.NORMAL)
            self.status_var.set(f"Selected {len(files)} file(s) - Ready for interactive view")
        
    def update_file_list(self):
        """Update the file list display."""
        # Clear existing items
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
            
        # Add new items
        for file_path in self.selected_files:
            file_info = self.file_manager.get_file_info(file_path)
            if file_info:
                size_mb = round(file_info['size'] / (1024 * 1024), 2)
                self.file_tree.insert("", "end", values=(
                    file_info['name'],
                    file_info['path'],
                    f"{size_mb} MB"
                ))
                
    def clear_selection(self):
        """Clear file selection."""
        self.selected_files = []
        self.update_file_list()
        self.view_btn.config(state=tk.DISABLED)
        self.status_var.set("Ready - Select a .mechdat file to begin")
        
    def open_interactive_view(self):
        """Open interactive view - direct call to worker."""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select files first.")
            return
            
        # Get selected item from treeview
        selection = self.file_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a file from the list.")
            return
            
        # Get file path from selection
        item = self.file_tree.item(selection[0])
        file_path = item['values'][1]
        
        # Launch interactive viewer directly
        self.launch_interactive_viewer(file_path)
        
    def launch_interactive_viewer(self, file_path):
        """Launch the interactive viewer using original worker."""
        self.status_var.set("Launching interactive 3D viewer...")
        
        def viewer_worker():
            try:
                # Get path to the interactive worker script in src directory
                current_dir = os.path.dirname(os.path.abspath(__file__))
                worker_script = os.path.join(current_dir, "interactive_worker.py")
                
                print(f"DEBUG: Looking for worker script at: {worker_script}")
                
                # Check if worker script exists
                if not os.path.exists(worker_script):
                    # Try alternative path
                    alt_worker_script = os.path.join(os.path.dirname(current_dir), "interactive_worker.py")
                    print(f"DEBUG: Trying alternative path: {alt_worker_script}")
                    if os.path.exists(alt_worker_script):
                        worker_script = alt_worker_script
                    else:
                        raise FileNotFoundError(f"Interactive worker script not found at {worker_script} or {alt_worker_script}")
                
                print(f"DEBUG: Using worker script: {worker_script}")
                print(f"DEBUG: Launching with file: {file_path}")
                
                # Launch subprocess
                process = subprocess.run([
                    sys.executable, worker_script, file_path
                ], check=True, capture_output=True, text=True)
                
                print(f"DEBUG: Process completed successfully")
                self.parent_frame.after(0, lambda: self.viewer_success())
                          
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr if e.stderr else e.stdout
                print(f"DEBUG: Process failed with error: {error_msg}")
                self.parent_frame.after(0, lambda: self.viewer_failed(error_msg))
            except Exception as e:
                print(f"DEBUG: Exception occurred: {str(e)}")
                self.parent_frame.after(0, lambda: self.viewer_failed(str(e)))
        
        thread = threading.Thread(target=viewer_worker)
        thread.daemon = True
        thread.start()
    
    def viewer_success(self):
        """Handle successful viewer launch."""
        self.status_var.set("Interactive 3D viewer completed successfully")
        messagebox.showinfo("Success", "PyANSYS Mechanical viewer completed successfully!")
    
    def viewer_failed(self, error):
        """Handle viewer launch failure."""
        self.status_var.set("Viewer launch failed")
        messagebox.showerror("Viewer Error", 
                           f"Failed to launch PyANSYS viewer:\\n\\n{error}")
