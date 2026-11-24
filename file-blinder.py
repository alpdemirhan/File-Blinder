import os
import shutil
import random
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from openpyxl import Workbook
from openpyxl.styles import Font

class FileBlinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blind File Analyzer Setup")
        self.root.geometry("540x240")
        self.root.resizable(False, False)

        self.folder_path = tk.StringVar()
        self.shuffle_var = tk.BooleanVar(value=True)

        # Header
        tk.Label(
            root, 
            text="Select Source Folder to Blind:", 
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(15, 5), padx=20, anchor="w")

        # Folder Selection Frame
        frame = tk.Frame(root)
        frame.pack(padx=20, fill="x")

        self.entry = tk.Entry(frame, textvariable=self.folder_path, width=52)
        self.entry.pack(side="left", padx=(0, 10), ipady=3)

        tk.Button(frame, text="Browse...", command=self.browse_folder, width=10).pack(side="left")

        # Options
        tk.Checkbutton(
            root, 
            text="Randomize number assignment (prevents alphabetical order bias)", 
            variable=self.shuffle_var,
            font=("Segoe UI", 9)
        ).pack(pady=15, padx=20, anchor="w")

        # Action Button
        tk.Button(
            root, 
            text="Create Blinded Folder & Excel Key", 
            command=self.process_files,
            bg="#2563eb", 
            fg="white", 
            font=("Segoe UI", 10, "bold"),
            padx=15, 
            pady=8
        ).pack(pady=5)

        # Status Bar
        self.status_label = tk.Label(root, text="Ready.", fg="gray", font=("Segoe UI", 9))
        self.status_label.pack(pady=(5, 0))

    def browse_folder(self):
        selected = filedialog.askdirectory(title="Select Folder Containing Files")
        if selected:
            self.folder_path.set(selected)

    def process_files(self):
        source_dir = self.folder_path.get().strip()
        if not source_dir or not os.path.isdir(source_dir):
            messagebox.showerror("Error", "Please select a valid source folder first.")
            return

        # Gather all top-level files (ignore subfolders, hidden files, and existing key files)
        all_items = os.listdir(source_dir)
        files = [
            f for f in all_items 
            if os.path.isfile(os.path.join(source_dir, f)) 
            and not f.startswith("Blinding_Key_")
            and not f.startswith(".")
        ]

        if not files:
            messagebox.showwarning("No Files Found", "The selected folder contains no valid files to blind.")
            return

        # Shuffle or sort
        if self.shuffle_var.get():
            random.shuffle(files)
        else:
            files.sort()

        # Create output folder next to the source folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = os.path.basename(os.path.normpath(source_dir))
        parent_dir = os.path.dirname(os.path.normpath(source_dir))
        blinded_dir = os.path.join(parent_dir, f"{folder_name}_Blinded_{timestamp}")

        try:
            os.makedirs(blinded_dir, exist_ok=True)

            # Initialize Excel Workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "Blinding Key"
            
            headers = ["Assigned Number", "Blinded Filename", "Original Filename"]
            ws.append(headers)
            for col_num in range(1, 4):
                ws.cell(row=1, column=col_num).font = Font(bold=True)

            # Determine zero-padding (minimum 3 digits, e.g., 001, 002)
            pad_length = max(3, len(str(len(files))))

            for idx, filename in enumerate(files, start=1):
                _, ext = os.path.splitext(filename)
                assigned_num = f"{idx:0{pad_length}d}"
                new_filename = f"{assigned_num}{ext}"

                src_file = os.path.join(source_dir, filename)
                dst_file = os.path.join(blinded_dir, new_filename)

                # Copy file content without preserving original creation/modification timestamps
                shutil.copyfile(src_file, dst_file)

                # Log mapping in Excel
                ws.append([assigned_num, new_filename, filename])

            # Auto-adjust column widths for readability
            ws.column_dimensions["A"].width = 18
            ws.column_dimensions["B"].width = 22
            ws.column_dimensions["C"].width = 45

            # Save the Excel key inside the original source folder
            excel_filename = f"Blinding_Key_{timestamp}.xlsx"
            excel_path = os.path.join(source_dir, excel_filename)
            wb.save(excel_path)

            self.status_label.config(text=f"Success! Blinded {len(files)} files.", fg="green")
            messagebox.showinfo(
                "Complete",
                f"Blinding complete!\n\n"
                f"Files processed: {len(files)}\n\n"
                f"Blinded Folder Created:\n{blinded_dir}\n\n"
                f"Key Saved in Source Folder:\n{excel_filename}"
            )

        except Exception as e:
            self.status_label.config(text="Error occurred.", fg="red")
            messagebox.showerror("Error", f"An error occurred while processing:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileBlinderApp(root)
    root.mainloop()