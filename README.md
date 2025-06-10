# PyANSYS Clean - Modern GUI Application

A comprehensive Python GUI application for visualizing and analyzing ANSYS Mechanical and result files with an intuitive modern interface.

## Overview

This GUI  provides a user-friendly interface for working with ANSYS simulation files, offering both mechanical file viewing and advanced result visualization capabilities through PyVista and DPF Post integration.

## Features

### 🔧 Mechanical Viewer
- **MECHDAT File Support**: Load and view ANSYS Mechanical database files
- **Interactive 3D Visualization**: Direct integration with PyANSYS for 3D model viewing
- **File Management**: Easy file selection and management interface

### 📊 Results Viewer
- **RST File Analysis**: Comprehensive result file (.rst) visualization
- **Result Types**: 
  - Von Mises Stress 
  - Total Deformation 
- **3D Interactive Plotting**: Real-time 3D visualization using PyVista
- **Multiple Visualization Methods**: Fallback options for different system configurations

### 🎨 User Interface
- **Modern GUI**: Clean, intuitive interface built with tkinter
- **Tabbed Interface**: Separate viewers for mechanical and results analysis
- **Theme Management**: Professional styling and color schemes
- **Status Monitoring**: Real-time status updates and progress tracking

## Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)

### Dependencies
Install required packages using pip:

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install pyvista ansys-dpf-post ansys-mechanical-core matplotlib numpy
```

## Quick Start

### 1. Launch Application
```bash
python launch.py
```

The launcher will:
- Check for required dependencies
- Offer to install missing packages automatically
- Launch the main GUI application

### 2. Alternative Launch
```bash
python main.py
```

## Usage

### Mechanical File Viewing
1. Switch to the **Mechanical Viewer** tab
2. Click **"Select Mechanical Files (.mechdat)"**
3. Choose your ANSYS mechanical database file
4. Click **"Open Interactive 3D View"** for visualization

### Result File Analysis
1. Switch to the **Results Viewer** tab
2. Select result type (Von Mises Stress or Total Deformation)
3. Click **"Select Result Files (.rst)"**
4. Choose your ANSYS result file
5. Click **"Open 3D Interactive Viewer"** for analysis

## Project Structure


```
Overview_GenericGUI.zip is a presentation of the overview.

PyANSYS_Dev_Alper/
├── launch.py              # Application launcher with dependency checking
├── main.py                # Main application entry point
├── requirements.txt       # Python dependencies
├── src/                   # Source code modules
│   ├── gui_application.py # Main GUI application class
│   ├── file_manager.py    # File handling and management
│   ├── result_viewer.py   # Result file visualization
│   ├── mechanical_viewer.py # Mechanical file viewing
│   ├── theme_manager.py   # UI theming and styling
│   └── interactive_worker.py # Background processing worker
└── article_snippets/      # Example files and code snippets
    ├── *.py               # Example implementation files
    ├── 1a.mechdat         # Sample mechanical file
    └── 1b_Result.rst      # Sample result file
```

## Key Components

### Core Modules
- **GUI Application**: Main application window and UI management
- **File Manager**: Handles file selection and information retrieval
- **Result Viewer**: Advanced result visualization with multiple rendering methods
- **Mechanical Viewer**: Direct PyANSYS integration for mechanical files
- **Theme Manager**: Professional UI styling and theming

### Visualization Engine
- **PyVista Integration**: High-performance 3D visualization
- **DPF Post Support**: ANSYS Data Processing Framework integration
- **Fallback Methods**: Multiple visualization approaches for compatibility

## Dependencies

### Required
- **ansys-dpf-post**: ANSYS Data Processing Framework
- **pyvista**: 3D visualization and mesh analysis
- **ansys-mechanical-core**: Core ANSYS Mechanical functionality

### Optional
- **matplotlib**: Alternative plotting capabilities
- **numpy**: Numerical computing support

## Troubleshooting

### Common Issues
1. **Missing Dependencies**: The launcher will automatically detect and offer to install missing packages
2. **Visualization Errors**: Multiple fallback methods ensure compatibility across different systems
3. **File Loading Issues**: Comprehensive error handling with detailed status messages

## Development

### Architecture
- **Modular Design**: Separate modules for different functionalities
- **Thread Safety**: Background processing for non-blocking UI operations
- **Error Handling**: Comprehensive error management and user feedback

### Extension Points
- **Custom Viewers**: Easy to add new file type support
- **Visualization Methods**: Pluggable visualization backends
- **Theme Customization**: Extensible theming system

## Version Information

**Version**: 1.1 - Working Version  
**Author**: A. Alper Akis  
**Focus**: Production-ready ANSYS file visualization with modern GUI

## License

This project is designed for educational and research purposes in conjunction with ANSYS software licensing requirements.

---

*For technical support or feature requests, please refer to the project documentation or contact the development team.*
