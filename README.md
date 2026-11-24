# File Blinder

A lightweight, standalone Python GUI tool for blinding experimental files (e.g., microscopy images, datasets, or videos) to prevent experimenter bias during analysis.

<!-- Optional: Add a screenshot of the GUI here once uploaded -->
<!-- ![File Blinder GUI](docs/screenshot.png) -->

## Features
- **Simple GUI:** Built with Python's native `tkinter`—no command-line experience required.
- **Reversible Blinding:** Automatically generates a secure mapping key (`.csv`) linking original filenames to randomized IDs for easy unblinding after analysis.
- **Non-Destructive Workflow:** Preserves original files by copying and renaming them into a separate output directory *(update if your script renames in-place)*.
- **Format Agnostic:** Works with any file type (`.czi`, `.tif`, `.nd2`, `.csv`, `.mp4`, etc.).

## Requirements
- Python 3.8 or higher
- Standard library only (`tkinter`, `os`, `shutil`, `csv`, `random`) *(add any external packages like `pandas` or `openpyxl` if used)*

## Installation
1. Clone this repository or download `file_blinder.py` directly:
   ```bash
   git clone https://github.com/alpdemirhan/file-blinder.git
cd file-blinder

