import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os

class ScraperLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("Google Maps Scraper - Launcher")
        self.geometry("500x350")
        self.configure(bg="#f0f0f0")
        
        # Crear la interfaz
        self.create_widgets()
    
    def create_widgets(self):
        # Título
        title_label = ttk.Label(
            self, 
            text="Google Maps Scraper", 
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=20)
        
        # Frame para los botones
        frame = ttk.LabelFrame(self, text="Selecciona una opción")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Botón para Scraper Simple
        ttk.Button(
            frame, 
            text="Scraper Simple", 
            command=self.run_simple_scraper,
            width=30,
            padding=10
        ).pack(fill=tk.X, padx=20, pady=10)
        
        # Botón para Batch Scraper
        ttk.Button(
            frame, 
            text="Batch Scraper", 
            command=self.run_batch_scraper,
            width=30,
            padding=10
        ).pack(fill=tk.X, padx=20, pady=10)
        
        # Botón para la interfaz gráfica
        ttk.Button(
            frame, 
            text="Interfaz Gráfica (GUI)", 
            command=self.run_gui_scraper,
            width=30,
            padding=10
        ).pack(fill=tk.X, padx=20, pady=10)
        
        # Botón para salir
        ttk.Button(
            self, 
            text="Salir", 
            command=self.quit,
            width=20
        ).pack(pady=20)
    
    def run_simple_scraper(self):
        self.destroy()  # Cerrar la ventana actual
        
        # Ejecutar el script de scraper simple
        try:
            subprocess.run([sys.executable, "scraper.py"])
        except Exception as e:
            print(f"Error al ejecutar scraper.py: {str(e)}")
        
        sys.exit(0)
    
    def run_batch_scraper(self):
        self.destroy()  # Cerrar la ventana actual
        
        # Ejecutar el script de batch scraper
        try:
            # Abrir una nueva consola con el script
            if sys.platform == 'win32':
                subprocess.Popen(["start", "cmd", "/k", sys.executable, "batch_scraper.py"], shell=True)
            else:
                subprocess.Popen(["xterm", "-e", sys.executable, "batch_scraper.py"])
        except Exception as e:
            print(f"Error al ejecutar batch_scraper.py: {str(e)}")
        
        sys.exit(0)
    
    def run_gui_scraper(self):
        self.destroy()  # Cerrar la ventana actual
        
        # Ejecutar el script de interfaz gráfica
        try:
            subprocess.run([sys.executable, "scraper_gui.py"])
        except Exception as e:
            print(f"Error al ejecutar scraper_gui.py: {str(e)}")
        
        sys.exit(0)

if __name__ == "__main__":
    app = ScraperLauncher()
    app.mainloop() 