"""
RBXMX/RBXLX/RBXM/RBXL to Rojo Converter - GUI Application
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from pathlib import Path
from converter import RojoConverter


class ConverterApp:
    """Main application window"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox to Rojo Converter")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Variables
        self.rbxmx_file = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.status_text = tk.StringVar(value="Waiting for file selection...")
        
        # Setup UI
        self._setup_ui()
        
        # Center window
        self._center_window()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = ttk.Frame(self.root, padding="20 20 20 10")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            title_frame,
            text="Roblox to Rojo Converter",
            font=("Arial", 16, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Convert RBXMX/RBXLX/RBXM/RBXL files to Rojo projects",
            font=("Arial", 10)
        )
        subtitle_label.pack()
        
        # Main content frame
        content_frame = ttk.Frame(self.root, padding="20 10 20 10")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection section
        file_section = ttk.LabelFrame(content_frame, text="Roblox File (RBXMX/RBXLX/RBXM/RBXL)", padding="10")
        file_section.pack(fill=tk.X, pady=(0, 10))
        
        file_entry_frame = ttk.Frame(file_section)
        file_entry_frame.pack(fill=tk.X)
        
        ttk.Entry(
            file_entry_frame,
            textvariable=self.rbxmx_file,
            state="readonly"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(
            file_entry_frame,
            text="Select File",
            command=self._select_file
        ).pack(side=tk.RIGHT)
        
        # Output folder section
        output_section = ttk.LabelFrame(content_frame, text="Output Folder", padding="10")
        output_section.pack(fill=tk.X, pady=(0, 10))
        
        output_entry_frame = ttk.Frame(output_section)
        output_entry_frame.pack(fill=tk.X)
        
        ttk.Entry(
            output_entry_frame,
            textvariable=self.output_folder,
            state="readonly"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(
            output_entry_frame,
            text="Select Folder",
            command=self._select_output
        ).pack(side=tk.RIGHT)
        
        # Convert button
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.convert_button = ttk.Button(
            button_frame,
            text="Convert",
            command=self._start_conversion,
            state=tk.DISABLED
        )
        self.convert_button.pack(pady=5)
        
        # Progress section
        progress_section = ttk.LabelFrame(content_frame, text="Status", padding="10")
        progress_section.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.status_label = ttk.Label(
            progress_section,
            textvariable=self.status_text,
            wraplength=540
        )
        self.status_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            progress_section,
            mode='indeterminate'
        )
        self.progress_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Footer
        footer_frame = ttk.Frame(self.root, padding="10")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        footer_label = ttk.Label(
            footer_frame,
            text="RBXMX to Rojo Converter v1.0",
            font=("Arial", 8)
        )
        footer_label.pack()
    
    def _center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _select_file(self):
        """Open file dialog to select RBXMX file"""
        filename = filedialog.askopenfilename(
            title="Select Roblox file",
            filetypes=[
                ("All Roblox Files", "*.rbxmx;*.rbxlx;*.rbxm;*.rbxl"),
                ("Roblox XML Files", "*.rbxmx;*.rbxlx"),
                ("Roblox Binary Files", "*.rbxm;*.rbxl"),
                ("All Files", "*.*")
            ]
        )
        
        if filename:
            self.rbxmx_file.set(filename)
            self._update_convert_button()
            self.status_text.set("Roblox file selected. Now select output folder.")
    
    def _select_output(self):
        """Open folder dialog to select output folder"""
        folder = filedialog.askdirectory(
            title="Select output folder"
        )
        
        if folder:
            # Create a subfolder with the name of the RBXMX file
            if self.rbxmx_file.get():
                base_name = Path(self.rbxmx_file.get()).stem
                output_path = Path(folder) / base_name
            else:
                output_path = Path(folder) / "rojo_project"
            
            self.output_folder.set(str(output_path))
            self._update_convert_button()
            self.status_text.set("Output folder selected. Ready to convert.")
    
    def _update_convert_button(self):
        """Enable convert button if both file and folder are selected"""
        if self.rbxmx_file.get() and self.output_folder.get():
            self.convert_button.config(state=tk.NORMAL)
        else:
            self.convert_button.config(state=tk.DISABLED)
    
    def _start_conversion(self):
        """Start the conversion process in a separate thread"""
        # Disable button during conversion
        self.convert_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.status_text.set("Converting... Please wait.")
        
        # Run conversion in separate thread
        thread = threading.Thread(target=self._convert)
        thread.daemon = True
        thread.start()
    
    def _convert(self):
        """Perform the actual conversion"""
        try:
            converter = RojoConverter(self.output_folder.get())
            success = converter.convert(self.rbxmx_file.get())
            
            # Update UI in main thread
            self.root.after(0, self._conversion_complete, success)
        except Exception as e:
            self.root.after(0, self._conversion_error, str(e))
    
    def _conversion_complete(self, success: bool):
        """Called when conversion is complete"""
        self.progress_bar.stop()
        self.convert_button.config(state=tk.NORMAL)
        
        if success:
            self.status_text.set(
                f"Conversion completed successfully!\n"
                f"Project created at: {self.output_folder.get()}"
            )
            messagebox.showinfo(
                "Success",
                f"Conversion completed successfully!\n\n"
                f"Rojo project created at:\n{self.output_folder.get()}"
            )
        else:
            self.status_text.set("Error during conversion. Check the file and try again.")
            messagebox.showerror(
                "Error",
                "An error occurred during conversion. "
                "Make sure the file is valid and contains scripts.\n\n"
                "Note: Binary files (.rbxm/.rbxl) are not currently supported.\n"
                "Please export as XML (.rbxmx/.rbxlx) from Roblox Studio."
            )
    
    def _conversion_error(self, error_msg: str):
        """Called when an error occurs during conversion"""
        self.progress_bar.stop()
        self.convert_button.config(state=tk.NORMAL)
        self.status_text.set(f"Error: {error_msg}")
        messagebox.showerror("Error", f"Error during conversion:\n{error_msg}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
