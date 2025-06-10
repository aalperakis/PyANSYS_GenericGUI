"""
Theme and Styling Example
This snippet shows how to create a consistent, modern theme for PyANSYS applications.
"""

import tkinter as tk
from tkinter import ttk

class ModernTheme:
    """Modern theme manager for PyANSYS applications."""
    
    def __init__(self):
        # Define color palette
        self.colors = {
            "background": "#f5f5f5",      # Light gray background
            "surface": "#ffffff",         # White surface
            "primary": "#ff6b35",         # Orange primary color
            "primary_dark": "#e85a30",    # Darker orange for hover
            "secondary": "#e0e0e0",       # Light gray secondary
            "text": "#333333",            # Dark gray text
            "text_light": "#666666",      # Light gray text
            "success": "#28a745",         # Green for success
            "warning": "#ffc107",         # Yellow for warning
            "error": "#dc3545",           # Red for error
            "info": "#17a2b8"            # Blue for info
        }
        
        # Define fonts
        self.fonts = {
            "default": ("Segoe UI", 10),
            "title": ("Segoe UI", 16, "bold"),
            "heading": ("Segoe UI", 12, "bold"),
            "small": ("Segoe UI", 8),
            "monospace": ("Consolas", 10)
        }
    
    def apply_theme(self, root):
        """Apply the theme to a tkinter root window."""
        root.configure(bg=self.colors["background"])
        
        # Create and configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure frame styles
        style.configure("TFrame", 
                       background=self.colors["background"],
                       borderwidth=0)
        
        style.configure("Card.TFrame",
                       background=self.colors["surface"],
                       relief="solid",
                       borderwidth=1)
        
        # Configure label styles
        style.configure("TLabel",
                       background=self.colors["background"],
                       foreground=self.colors["text"],
                       font=self.fonts["default"])
        
        style.configure("Title.TLabel",
                       background=self.colors["background"],
                       foreground=self.colors["text"],
                       font=self.fonts["title"])
        
        style.configure("Heading.TLabel",
                       background=self.colors["background"],
                       foreground=self.colors["text"],
                       font=self.fonts["heading"])
        
        # Configure button styles
        style.configure("TButton",
                       font=self.fonts["default"],
                       padding=(20, 10))
        
        style.configure("Primary.TButton",
                       foreground="white",
                       font=self.fonts["default"])
        style.map("Primary.TButton",
                 background=[('active', self.colors["primary_dark"]),
                           ('!active', self.colors["primary"])])
        
        # Configure notebook and other widgets
        style.configure("TNotebook",
                       background=self.colors["background"])
        
        style.configure("TNotebook.Tab",
                       background=self.colors["secondary"],
                       foreground=self.colors["text"],
                       font=self.fonts["default"],
                       padding=[20, 8])

class ThemedApplication:
    """Example application using the modern theme."""
    
    def __init__(self, root):
        self.root = root
        self.theme = ModernTheme()
        self.setup_window()
        self.create_ui()
    
    def setup_window(self):
        """Setup the main window."""
        self.root.title("PyANSYS Modern Theme Example")
        self.root.geometry("800x600")
        self.theme.apply_theme(self.root)
    
    def create_ui(self):
        """Create the user interface with themed components."""
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame,
                               text="PyANSYS Modern Theme",
                               style="Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Create sections
        self.create_button_section(main_frame)
        self.create_data_section(main_frame)
    
    def create_button_section(self, parent):
        """Create a section with different button styles."""
        button_frame = ttk.LabelFrame(parent, text="Action Buttons")
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        content_frame = ttk.Frame(button_frame, style="TFrame")
        content_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(content_frame, text="Load File", style="Primary.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(content_frame, text="Process", style="Primary.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(content_frame, text="Save Results", style="Primary.TButton").pack(side=tk.LEFT)
    
    def create_data_section(self, parent):
        """Create a section with data display widgets."""
        data_frame = ttk.LabelFrame(parent, text="Data Display")
        data_frame.pack(fill=tk.BOTH, expand=True)
        
        notebook = ttk.Notebook(data_frame, style="TNotebook")
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # File list tab
        file_tab = ttk.Frame(notebook, style="TFrame")
        notebook.add(file_tab, text="Files")
        
        # Create treeview with sample data
        columns = ("Name", "Type", "Size")
        tree = ttk.Treeview(file_tab, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        sample_data = [
            ("model.mechdat", "Mechanical", "45.2 MB"),
            ("results.rst", "Results", "78.5 MB")
        ]
        
        for item in sample_data:
            tree.insert("", "end", values=item)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ThemedApplication(root)
    root.mainloop()
