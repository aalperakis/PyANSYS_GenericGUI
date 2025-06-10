"""
File Selection Example for ANSYS Files
This snippet demonstrates how to implement file selection and validation 
for different ANSYS file types.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class ANSYSFileSelector:
    """File selector for ANSYS files with validation."""
    
    def __init__(self, root):
        self.root = root
        self.selected_files = []
        
        # Define supported file types
        self.file_types = {
            'mechanical': {
                'extensions': ['.mechdat'],
                'description': 'Mechanical Files'
            },
            'results': {
                'extensions': ['.rst'],
                'description': 'Result Files'
            }
        }
        
        self.create_ui()
    
    def create_ui(self):
        """Create the file selection interface."""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(main_frame, text="ANSYS File Selection", 
                 font=("Segoe UI", 14, "bold")).pack(pady=(0, 20))
        
        # File type selection
        type_frame = ttk.LabelFrame(main_frame, text="File Type")
        type_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.file_type_var = tk.StringVar(value="mechanical")
        
        ttk.Radiobutton(type_frame, text="Mechanical Files (.mechdat)",
                       variable=self.file_type_var, value="mechanical").pack(anchor=tk.W, padx=10, pady=5)
        
        ttk.Radiobutton(type_frame, text="Result Files (.rst)",
                       variable=self.file_type_var, value="results").pack(anchor=tk.W, padx=10, pady=5)
        
        # Selection button
        ttk.Button(main_frame, text="Select Files", 
                  command=self.select_files).pack(pady=10)
        
        # File list
        list_frame = ttk.LabelFrame(main_frame, text="Selected Files")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Treeview for file display
        columns = ("Name", "Size", "Type")
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.file_tree.heading(col, text=col)
            self.file_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
    
    def select_files(self):
        """Open file dialog and validate selected files."""
        file_type = self.file_type_var.get()
        type_info = self.file_types[file_type]
        
        # Create file type filters
        extensions = type_info['extensions']
        file_filter = " ".join([f"*{ext}" for ext in extensions])
        
        filetypes = [
            (type_info['description'], file_filter),
            ("All Files", "*.*")
        ]
        
        # Open file dialog
        files = filedialog.askopenfilenames(
            title=f"Select {type_info['description']}",
            filetypes=filetypes
        )
        
        if files:
            valid_files = self.validate_files(files, extensions)
            self.selected_files = valid_files
            self.update_file_list()
    
    def validate_files(self, files, valid_extensions):
        """Validate selected files against supported extensions."""
        valid_files = []
        invalid_files = []
        
        for file_path in files:
            if os.path.exists(file_path):
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext in valid_extensions:
                    valid_files.append(file_path)
                else:
                    invalid_files.append(file_path)
        
        if invalid_files:
            invalid_names = [os.path.basename(f) for f in invalid_files]
            messagebox.showwarning(
                "Invalid Files",
                f"The following files are not supported:\\n" + "\\n".join(invalid_names)
            )
        
        return valid_files
    
    def update_file_list(self):
        """Update the file list display."""
        # Clear existing items
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # Add valid files
        for file_path in self.selected_files:
            name = os.path.basename(file_path)
            size = os.path.getsize(file_path)
            size_mb = f"{size / (1024*1024):.1f} MB"
            file_type = os.path.splitext(file_path)[1]
            
            self.file_tree.insert("", "end", values=(name, size_mb, file_type))

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("ANSYS File Selector Example")
    root.geometry("600x500")
    
    app = ANSYSFileSelector(root)
    root.mainloop()
