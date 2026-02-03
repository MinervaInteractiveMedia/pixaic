#!/usr/bin/env python3
"""
Photomosaic Creator - True Tile Matching Version
A GUI application that recreates one image using tiles extracted from another image.
Each tile is selected to best match the target region's average color.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from pathlib import Path
import threading
import random


class PhotomosaicCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Photomosaic Creator - Tile Matching")
        self.root.geometry("900x750")
        
        # Variables
        self.target_image = None
        self.tile_image = None
        self.result_image = None
        self.target_path = None
        self.tile_path = None
        self.tile_library = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Photomosaic Creator - Tile Matching", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input Images", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Target image
        ttk.Label(input_frame, text="Target Image:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.target_label = ttk.Label(input_frame, text="No file selected", 
                                     foreground="gray")
        self.target_label.grid(row=0, column=1, sticky=tk.W, padx=10)
        ttk.Button(input_frame, text="Browse...", 
                  command=self.load_target_image).grid(row=0, column=2, padx=5)
        
        # Source/Tile image
        ttk.Label(input_frame, text="Source Image:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.tile_label = ttk.Label(input_frame, text="No file selected", 
                                   foreground="gray")
        self.tile_label.grid(row=1, column=1, sticky=tk.W, padx=10)
        ttk.Button(input_frame, text="Browse...", 
                  command=self.load_tile_image).grid(row=1, column=2, padx=5)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Settings section
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(settings_frame, text="Tile Size:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.tile_size_var = tk.IntVar(value=20)
        tile_size_spinner = ttk.Spinbox(settings_frame, from_=5, to=100, 
                                       textvariable=self.tile_size_var, width=10)
        tile_size_spinner.grid(row=0, column=1, sticky=tk.W, padx=10)
        ttk.Label(settings_frame, text="pixels").grid(row=0, column=2, sticky=tk.W)
        
        ttk.Label(settings_frame, text="Output Width:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_width_var = tk.IntVar(value=800)
        width_spinner = ttk.Spinbox(settings_frame, from_=200, to=3000, 
                                   textvariable=self.output_width_var, width=10)
        width_spinner.grid(row=1, column=1, sticky=tk.W, padx=10)
        ttk.Label(settings_frame, text="pixels").grid(row=1, column=2, sticky=tk.W)
        
        ttk.Label(settings_frame, text="Tiles to Extract:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.num_tiles_var = tk.IntVar(value=1000)
        tiles_spinner = ttk.Spinbox(settings_frame, from_=100, to=10000, 
                                   textvariable=self.num_tiles_var, width=10)
        tiles_spinner.grid(row=2, column=1, sticky=tk.W, padx=10)
        ttk.Label(settings_frame, text="from source").grid(row=2, column=2, sticky=tk.W)
        
        # Color matching method
        ttk.Label(settings_frame, text="Matching:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.match_mode_var = tk.StringVar(value="average")
        match_combo = ttk.Combobox(settings_frame, textvariable=self.match_mode_var, 
                                  values=["average", "weighted"], state="readonly", width=12)
        match_combo.grid(row=3, column=1, sticky=tk.W, padx=10)
        ttk.Label(settings_frame, text="color comparison").grid(row=3, column=2, sticky=tk.W)
        
        # Generate button
        self.generate_btn = ttk.Button(settings_frame, text="Generate Photomosaic", 
                                      command=self.generate_mosaic, state=tk.DISABLED)
        self.generate_btn.grid(row=4, column=0, columnspan=3, pady=15)
        
        # Progress bar
        self.progress = ttk.Progressbar(settings_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(settings_frame, text="", foreground="blue")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Preview section
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Canvas for preview
        self.canvas = tk.Canvas(preview_frame, width=800, height=400, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Export button
        self.export_btn = ttk.Button(main_frame, text="Export Result", 
                                    command=self.export_result, state=tk.DISABLED)
        self.export_btn.grid(row=4, column=0, columnspan=3, pady=10)
        
        main_frame.rowconfigure(3, weight=1)
        
    def load_target_image(self):
        filename = filedialog.askopenfilename(
            title="Select Target Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), 
                      ("All files", "*.*")]
        )
        if filename:
            try:
                self.target_image = Image.open(filename)
                self.target_path = filename
                self.target_label.config(text=Path(filename).name, foreground="black")
                self.check_ready()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load target image: {str(e)}")
    
    def load_tile_image(self):
        filename = filedialog.askopenfilename(
            title="Select Source Image (for tiles)",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), 
                      ("All files", "*.*")]
        )
        if filename:
            try:
                self.tile_image = Image.open(filename)
                self.tile_path = filename
                self.tile_label.config(text=Path(filename).name, foreground="black")
                self.check_ready()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load source image: {str(e)}")
    
    def check_ready(self):
        if self.target_image and self.tile_image:
            self.generate_btn.config(state=tk.NORMAL)
    
    def generate_mosaic(self):
        # Disable button during generation
        self.generate_btn.config(state=tk.DISABLED)
        self.export_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.status_label.config(text="Generating photomosaic...", foreground="blue")
        
        # Run in separate thread to keep UI responsive
        thread = threading.Thread(target=self._create_mosaic)
        thread.start()
    
    def _extract_tiles(self, source_image, tile_size, num_tiles):
        """Extract random tiles from source image"""
        source_rgb = source_image.convert('RGB')
        source_array = np.array(source_rgb)
        
        height, width = source_array.shape[:2]
        tiles = []
        
        # Calculate how many unique positions are possible
        max_y = height - tile_size
        max_x = width - tile_size
        
        if max_y <= 0 or max_x <= 0:
            # Source image is too small, resize it
            min_size = tile_size * 10
            source_rgb = source_rgb.resize((min_size, min_size), Image.Resampling.LANCZOS)
            source_array = np.array(source_rgb)
            height, width = source_array.shape[:2]
            max_y = height - tile_size
            max_x = width - tile_size
        
        self.root.after(0, lambda: self.status_label.config(
            text=f"Extracting {num_tiles} tiles from source image..."))
        
        for i in range(num_tiles):
            # Random position
            y = random.randint(0, max_y)
            x = random.randint(0, max_x)
            
            # Extract tile
            tile_array = source_array[y:y+tile_size, x:x+tile_size].copy()
            
            # Calculate average color
            avg_color = np.mean(tile_array, axis=(0, 1))
            
            tiles.append({
                'array': tile_array,
                'avg_color': avg_color
            })
        
        return tiles
    
    def _find_best_tile(self, target_color, tiles, match_mode='average'):
        """Find the tile that best matches the target color"""
        best_tile = None
        best_distance = float('inf')
        
        for tile in tiles:
            if match_mode == 'weighted':
                # Weighted color distance (human perception)
                diff = target_color - tile['avg_color']
                distance = np.sqrt(2 * diff[0]**2 + 4 * diff[1]**2 + 3 * diff[2]**2)
            else:
                # Simple euclidean distance
                distance = np.linalg.norm(target_color - tile['avg_color'])
            
            if distance < best_distance:
                best_distance = distance
                best_tile = tile
        
        return best_tile
    
    def _create_mosaic(self):
        try:
            tile_size = self.tile_size_var.get()
            output_width = self.output_width_var.get()
            num_tiles = self.num_tiles_var.get()
            match_mode = self.match_mode_var.get()
            
            # Ensure images are in RGB mode
            target_rgb = self.target_image.convert('RGB')
            
            # Calculate dimensions
            aspect_ratio = target_rgb.height / target_rgb.width
            output_height = int(output_width * aspect_ratio)
            
            # Resize target image to match grid
            grid_width = output_width // tile_size
            grid_height = output_height // tile_size
            target_resized = target_rgb.resize((grid_width, grid_height), 
                                              Image.Resampling.LANCZOS)
            
            # Convert target to array
            target_array = np.array(target_resized)
            
            # Extract tiles from source image
            self.tile_library = self._extract_tiles(self.tile_image, tile_size, num_tiles)
            
            self.root.after(0, lambda: self.status_label.config(
                text=f"Building mosaic from {len(self.tile_library)} tiles..."))
            
            # Create output image
            result = Image.new('RGB', (grid_width * tile_size, grid_height * tile_size))
            
            total_tiles = grid_width * grid_height
            processed = 0
            
            # Create photomosaic by matching tiles
            for y in range(grid_height):
                for x in range(grid_width):
                    # Get target color for this position
                    target_color = target_array[y, x]
                    
                    # Find best matching tile
                    best_tile = self._find_best_tile(target_color, self.tile_library, match_mode)
                    
                    # Paste tile
                    tile_img = Image.fromarray(best_tile['array'])
                    result.paste(tile_img, (x * tile_size, y * tile_size))
                    
                    processed += 1
                    if processed % 100 == 0:
                        progress_pct = (processed / total_tiles) * 100
                        self.root.after(0, lambda p=progress_pct: self.status_label.config(
                            text=f"Building mosaic... {p:.1f}% complete"))
            
            self.result_image = result
            
            # Update UI in main thread
            self.root.after(0, self._display_result)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", 
                                                           f"Failed to generate mosaic: {str(e)}"))
            self.root.after(0, self._reset_ui)
    
    def _display_result(self):
        # Display result on canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width < 100:  # Canvas not yet rendered
            canvas_width = 800
            canvas_height = 400
        
        # Calculate preview size maintaining aspect ratio
        img_aspect = self.result_image.width / self.result_image.height
        canvas_aspect = canvas_width / canvas_height
        
        if img_aspect > canvas_aspect:
            preview_width = canvas_width - 20
            preview_height = int(preview_width / img_aspect)
        else:
            preview_height = canvas_height - 20
            preview_width = int(preview_height * img_aspect)
        
        preview = self.result_image.resize((preview_width, preview_height), 
                                          Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage and display
        self.photo = ImageTk.PhotoImage(preview)
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width//2, canvas_height//2, 
                                image=self.photo, anchor=tk.CENTER)
        
        # Re-enable buttons
        self.generate_btn.config(state=tk.NORMAL)
        self.export_btn.config(state=tk.NORMAL)
        self.progress.stop()
        self.status_label.config(text="Photomosaic generated successfully!", 
                                foreground="green")
    
    def _reset_ui(self):
        self.generate_btn.config(state=tk.NORMAL)
        self.progress.stop()
        self.status_label.config(text="")
    
    def export_result(self):
        if not self.result_image:
            messagebox.showwarning("Warning", "No result to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Photomosaic",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), 
                      ("JPEG files", "*.jpg"),
                      ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.result_image.save(filename)
                messagebox.showinfo("Success", f"Photomosaic saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")


def main():
    root = tk.Tk()
    app = PhotomosaicCreator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
