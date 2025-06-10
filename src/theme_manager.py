"""
Theme Manager - Handles UI styling and theming
Provides a consistent look and feel across the application.
"""

import tkinter as tk
from tkinter import ttk

class ThemeManager:
    """Manages application themes and styling."""
    
    def __init__(self):
        self.colors = {
            "background": "#f0f0f0",
            "secondary": "#e0e0e0", 
            "accent": "#ff6b35",
            "text": "#333333",
            "success": "#28a745",
            "warning": "#ffc107",
            "error": "#dc3545",
            "info": "#17a2b8"
        }
        
    def apply_theme(self, root):
        """Apply the theme to the root window and configure styles."""
        root.configure(bg=self.colors["background"])
        
        # Create and configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure basic styles
        style.configure("TFrame", background=self.colors["background"])
        style.configure("TLabel", background=self.colors["background"], 
                       foreground=self.colors["text"])
        style.configure("TButton", font=("Segoe UI", 10))
        
        # Configure accent button
        style.configure("Accent.TButton", 
                       foreground="white",
                       font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton",
                 background=[('active', '#ff8c69'), 
                           ('!active', self.colors["accent"])])
        
        # Configure title label
        style.configure("Title.TLabel", 
                       font=("Segoe UI", 16, "bold"),
                       background=self.colors["background"],
                       foreground=self.colors["text"])
        
        # Configure notebook
        style.configure("TNotebook", background=self.colors["background"])
        style.configure("TNotebook.Tab", 
                       font=("Segoe UI", 10),
                       padding=[20, 8])
        
        # Configure labelframe
        style.configure("TLabelframe", 
                       background=self.colors["background"],
                       borderwidth=1,
                       relief="solid")
        style.configure("TLabelframe.Label", 
                       background=self.colors["background"],
                       foreground=self.colors["text"],
                       font=("Segoe UI", 10, "bold"))
