"""
Basic GUI Setup Example for PyANSYS Applications
This snippet shows how to create a basic PyANSYS GUI window with proper styling.
"""

import tkinter as tk
from tkinter import ttk

def create_styled_application():
    """Create a basic styled PyANSYS application window."""
    
    # Create root window
    root = tk.Tk()
    root.title("PyANSYS Modern GUI")
    root.geometry("800x600")
    
    # Configure colors and styling
    colors = {
        "background": "#f0f0f0",
        "accent": "#ff6b35",
        "text": "#333333"
    }
    
    root.configure(bg=colors["background"])
    
    # Create and configure ttk style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure custom styles
    style.configure("TFrame", background=colors["background"])
    style.configure("TLabel", 
                   background=colors["background"], 
                   foreground=colors["text"],
                   font=("Segoe UI", 10))
    
    style.configure("Title.TLabel", 
                   font=("Segoe UI", 16, "bold"),
                   background=colors["background"],
                   foreground=colors["text"])
    
    style.configure("Accent.TButton", 
                   foreground="white",
                   font=("Segoe UI", 10, "bold"))
    style.map("Accent.TButton",
             background=[('active', '#ff8c69'), 
                        ('!active', colors["accent"])])
    
    # Create main frame
    main_frame = ttk.Frame(root, style="TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Add title
    title_label = ttk.Label(main_frame, 
                           text="PyANSYS Modern GUI", 
                           style="Title.TLabel")
    title_label.pack(pady=(0, 20))
    
    # Add description
    desc_label = ttk.Label(main_frame,
                          text="A modern interface for ANSYS file visualization",
                          style="TLabel")
    desc_label.pack(pady=(0, 30))
    
    # Add action button
    action_btn = ttk.Button(main_frame,
                           text="Get Started",
                           style="Accent.TButton")
    action_btn.pack(pady=10)
    
    return root

if __name__ == "__main__":
    app = create_styled_application()
    app.mainloop()
