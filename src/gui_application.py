"""
PyANSYS GUI Application - Core Module
Handles the main application window and user interface components.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess

from theme_manager import ThemeManager
from file_manager import FileManager
from result_viewer import ResultViewer
from mechanical_viewer import MechanicalViewer

class PyANSYSApplication:
    """Main application class for PyANSYS GUI."""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Initialize components
        self.theme_manager = ThemeManager()
        self.file_manager = FileManager()
        self.result_viewer = None
        self.mechanical_viewer = None
        
        # Initialize status
        self.status_var = tk.StringVar(value="Ready")
        
        # Apply theme
        self.theme_manager.apply_theme(self.root)
        
        # Create UI
        self.create_ui()
        
    def setup_window(self):
        """Configure the main window."""
        self.root.title("PyANSYS Modern GUI - Mechanical & Results Viewer")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
    def create_ui(self):
        """Create the main user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="PyANSYS Modern GUI - Article Version", 
                               style="Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Create notebook for different viewers
        self.notebook = ttk.Notebook(main_frame, style="TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_mechanical_tab()
        self.create_results_tab()
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_mechanical_tab(self):
        """Create the mechanical viewer tab."""
        mech_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(mech_frame, text="Mechanical Viewer")
        
        # Initialize mechanical viewer
        self.mechanical_viewer = MechanicalViewer(mech_frame, self.file_manager)
        
    def create_results_tab(self):
        """Create the results viewer tab."""
        results_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(results_frame, text="Results Viewer")
        
        # Initialize result viewer
        self.result_viewer = ResultViewer(results_frame, self.file_manager)
        
    def create_status_bar(self, parent):
        """Create status bar at the bottom."""
        status_frame = ttk.Frame(parent, style="TFrame")
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Status label
        status_label = ttk.Label(status_frame, 
                                textvariable=self.status_var, 
                                style="TLabel")
        status_label.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, 
                                       mode='determinate', 
                                       length=200)
        self.progress.pack(side=tk.RIGHT, padx=(10, 0))
