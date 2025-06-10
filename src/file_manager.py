"""
File Manager - Handles file operations and validation
Manages selection and validation of ANSYS files.
"""

import os
from tkinter import filedialog, messagebox

class FileManager:
    """Manages file operations for ANSYS files."""
    
    def __init__(self):
        self.supported_mechanical_files = ['.mechdat']
        self.supported_result_files = ['.rst']
        
    def select_mechanical_files(self):
        """Select mechanical files (.mechdat)."""
        filetypes = [
            ("Mechanical Files", "*.mechdat"),
            ("MECHDAT Files", "*.mechdat"),
            ("All Files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select Mechanical Files",
            filetypes=filetypes
        )
        
        return self.validate_files(files, self.supported_mechanical_files)
    
    def select_result_files(self):
        """Select result files (.rst)."""
        filetypes = [
            ("Result Files", "*.rst"),
            ("RST Files", "*.rst"),
            ("All Files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select Result Files",
            filetypes=filetypes
        )
        
        return self.validate_files(files, self.supported_result_files)
    
    def validate_files(self, files, supported_extensions):
        """Validate selected files against supported extensions."""
        valid_files = []
        invalid_files = []
        
        for file_path in files:
            if os.path.exists(file_path):
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext in supported_extensions:
                    valid_files.append(file_path)
                else:
                    invalid_files.append(file_path)
            else:
                invalid_files.append(file_path)
        
        if invalid_files:
            messagebox.showwarning(
                "Invalid Files",
                f"The following files are not supported or don't exist:\\n" +
                "\\n".join([os.path.basename(f) for f in invalid_files])
            )
        
        return valid_files
    
    def get_file_info(self, file_path):
        """Get basic information about a file."""
        if not os.path.exists(file_path):
            return None
            
        stat = os.stat(file_path)
        return {
            'name': os.path.basename(file_path),
            'path': file_path,
            'size': stat.st_size,
            'modified': stat.st_mtime,
            'extension': os.path.splitext(file_path)[1].lower()
        }
