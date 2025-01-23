# STEM-EDX ML  

**Full documentation available here :** https://edx-ai-84a865.gitlab.io/

## Description  
STEM-EDX ML is a graphical application designed for managing and analyzing STEM-EDX (Scanning Transmission Electron Microscopy - Energy Dispersive X-ray Spectroscopy) data using machine learning algorithms.  

The graphical user interface, built with PySide6, allows users to:  
- Load STEM-EDX data files (.pts)  
- Visualize images and spectra  
- Apply decomposition algorithms such as PCA (Principal Component Analysis) and NMF (Non-negative Matrix Factorization)  
- Interact with results through dynamic graphs  

## Features  
- Load and manage STEM-EDX data files  
- Select and display analyzed objects  
- Apply and visualize PCA and NMF results  
- Interactive and responsive user interface  

## Scientific Context  
This project is based on STEM-EDX measurement results. The full study framework and experimental details can be found in the "Report" (in French) located in the `Presentations` folder.  

## Installation  

### Installation of Hyperspy and Exspy
Run the following commands:
```bash
conda install hyperspy -c conda-forge
conda install exspy
```

### Prerequisites  
- Python 3.x  
- [Hyperspy](https://hyperspy.org/) for spectral analysis
- Exspy (exspy) for TEM-EELS data type managment
- PySide6 for the graphical interface  

### Installation with pip
Run the following commands:
```bash
pip install EDX-AI
```

## Usage  
Run the application with the following command:  
```bash
EDX-AI
```

## Project structure
STEM-EDX-ML/  
│── mainwindow.py   # Main graphical interface

│── stem.py         # STEM-EDX data management and ML algorithms  

│── utils.py        # Utility functions and widget management  

|── colorscales.py  # Colorscales available

|── main.py         # The main program to execute

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Author

Anthony Pecquenard, 2025.