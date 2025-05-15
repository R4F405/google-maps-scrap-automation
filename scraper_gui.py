import os
import json
import requests
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from os import listdir
from os.path import isfile, join
import threading

# Funciones del scraper que vamos a reutilizar
def get_keyword_files():
    """Obtiene todos los archivos de keywords y los ordena por su prefijo numérico"""
    keyword_dir = 'keywords'
    files = [f for f in listdir(keyword_dir) if isfile(join(keyword_dir, f))]
    # Extrae el prefijo numérico y ordena por él
    files.sort(key=lambda x: int(x.split('_')[0]))
    return files

def get_location_files():
    """Obtiene todos los archivos de localización y los ordena por su prefijo numérico"""
    location_dir = 'location'
    files = [f for f in listdir(location_dir) if isfile(join(location_dir, f))]
    # Extrae el prefijo numérico y ordena por él
    files.sort(key=lambda x: int(x.split('_')[0]))
    return files

def read_keywords(keyword_file):
    """Lee keywords del archivo seleccionado"""
    with open(os.path.join('keywords', keyword_file), 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]

def read_location(location_file):
    """Lee datos de localización del archivo seleccionado"""
    with open(os.path.join('location', location_file), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return {
            'zoom': int(lines[0].strip()),
            'lat': lines[1].strip(),
            'lon': lines[2].strip()
        }

def submit_job(api_url, payload):
    """Envía un trabajo a la API"""
    try:
        response = requests.post(api_url, json=payload)
        if response.status_code in [200, 201]:
            result = response.json()
            return result.get('id'), response.status_code, result
        else:
            return None, response.status_code, response.text
    except Exception as e:
        return None, 0, str(e)

def check_job_status(job_id, api_url):
    """Verifica el estado de un trabajo"""
    status_url = f"{api_url}/{job_id}"
    try:
        response = requests.get(status_url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": f"Error {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

class GoogleMapsScraper(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("Google Maps Scraper - Interfaz Gráfica")
        self.geometry("900x700")
        self.configure(bg="#f0f0f0")
        
        # Variables para almacenar selecciones
        self.host_var = tk.StringVar(value="http://localhost:8080")
        self.job_name_var = tk.StringVar(value=f"Trabajo_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.radius_var = tk.IntVar(value=10000)
        self.depth_var = tk.IntVar(value=10)
        self.max_time_var = tk.IntVar(value=15)
        self.wait_time_var = tk.IntVar(value=30)
        
        self.keyword_files = get_keyword_files()
        self.location_files = get_location_files()
        self.selected_categories = []
        self.selected_locations = []
        self.selected_keywords = []
        
        # Crear la interfaz
        self.create_widgets()
        
        # Estado de ejecución
        self.running = False
        self.job_id = None
    
    def create_widgets(self):
        # Frame principal con pestañas
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña de configuración
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="Configuración")
        
        # Pestaña de categorías y keywords
        categories_frame = ttk.Frame(notebook)
        notebook.add(categories_frame, text="Categorías y Keywords")
        
        # Pestaña de localizaciones
        locations_frame = ttk.Frame(notebook)
        notebook.add(locations_frame, text="Localizaciones")
        
        # Pestaña de ejecución y logs
        execution_frame = ttk.Frame(notebook)
        notebook.add(execution_frame, text="Ejecución")
        
        # Configurar cada pestaña
        self.setup_config_tab(config_frame)
        self.setup_categories_tab(categories_frame)
        self.setup_locations_tab(locations_frame)
        self.setup_execution_tab(execution_frame)
    
    def setup_config_tab(self, parent):
        # Frame para configuración general
        frame = ttk.LabelFrame(parent, text="Configuración General")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Host API
        ttk.Label(frame, text="Host API:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.host_var, width=40).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Nombre del trabajo
        ttk.Label(frame, text="Nombre del trabajo:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.job_name_var, width=40).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Radio de búsqueda
        ttk.Label(frame, text="Radio (metros):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.radius_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Profundidad de búsqueda
        ttk.Label(frame, text="Profundidad:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.depth_var, width=10).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Tiempo máximo por trabajo
        ttk.Label(frame, text="Tiempo máximo (minutos):").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.max_time_var, width=10).grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Tiempo de espera
        ttk.Label(frame, text="Tiempo de espera (minutos):").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.wait_time_var, width=10).grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
    
    def setup_categories_tab(self, parent):
        # Frame para seleccionar categorías
        categories_frame = ttk.LabelFrame(parent, text="Categorías Disponibles")
        categories_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lista de categorías con checkbuttons
        self.category_vars = []
        self.category_names = []
        
        # Crear un canvas con scrollbar para las categorías
        canvas = tk.Canvas(categories_frame)
        scrollbar = ttk.Scrollbar(categories_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Crear checkbuttons para cada categoría
        for i, file in enumerate(self.keyword_files):
            category_name = file.split('_keywords_')[1].split('.')[0]
            self.category_names.append(category_name)
            var = tk.BooleanVar()
            self.category_vars.append(var)
            
            ttk.Checkbutton(
                scrollable_frame, 
                text=f"{i+1}. {category_name}", 
                variable=var,
                command=self.update_keywords_list
            ).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para mostrar keywords de la categoría seleccionada
        keywords_frame = ttk.LabelFrame(parent, text="Keywords Disponibles")
        keywords_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lista de keywords
        self.keywords_listbox = tk.Listbox(keywords_frame, selectmode=tk.EXTENDED, height=15)
        self.keywords_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar para la lista de keywords
        keywords_scrollbar = ttk.Scrollbar(keywords_frame, orient=tk.VERTICAL, command=self.keywords_listbox.yview)
        keywords_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.keywords_listbox.configure(yscrollcommand=keywords_scrollbar.set)
        
        # Botones para seleccionar todos/ninguno
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Seleccionar Todas", command=self.select_all_categories).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Deseleccionar Todas", command=self.deselect_all_categories).pack(side=tk.LEFT, padx=5)
    
    def setup_locations_tab(self, parent):
        # Frame para seleccionar localizaciones
        locations_frame = ttk.LabelFrame(parent, text="Localizaciones Disponibles")
        locations_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lista de localizaciones con checkbuttons
        self.location_vars = []
        self.location_names = []
        
        for i, file in enumerate(self.location_files):
            location_name = file.split('_location_')[1].split('.')[0]
            self.location_names.append(location_name)
            var = tk.BooleanVar()
            self.location_vars.append(var)
            
            ttk.Checkbutton(
                locations_frame, 
                text=f"{i+1}. {location_name}", 
                variable=var
            ).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Información de la localización seleccionada
        info_frame = ttk.LabelFrame(parent, text="Información de Localización")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.location_info_text = scrolledtext.ScrolledText(info_frame, height=10, wrap=tk.WORD)
        self.location_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.location_info_text.config(state=tk.DISABLED)
        
        # Botón para mostrar información de localizaciones seleccionadas
        ttk.Button(parent, text="Ver Información de Localizaciones Seleccionadas", 
                  command=self.show_location_info).pack(pady=10)
    
    def setup_execution_tab(self, parent):
        # Frame para mostrar configuración del trabajo
        summary_frame = ttk.LabelFrame(parent, text="Resumen del Trabajo")
        summary_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.summary_text = scrolledtext.ScrolledText(summary_frame, height=15, wrap=tk.WORD)
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para los logs
        log_frame = ttk.LabelFrame(parent, text="Logs")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botones de control
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.update_button = ttk.Button(button_frame, text="Actualizar Resumen", command=self.update_summary)
        self.update_button.pack(side=tk.LEFT, padx=5)
        
        self.run_button = ttk.Button(button_frame, text="Ejecutar Trabajo", command=self.run_job)
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.cancel_job, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(parent, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=10, pady=10)
    
    def update_keywords_list(self):
        # Limpiar la lista actual
        self.keywords_listbox.delete(0, tk.END)
        
        # Obtener las categorías seleccionadas
        selected_indices = [i for i, var in enumerate(self.category_vars) if var.get()]
        
        # Actualizar la lista de keywords
        all_keywords = []
        for idx in selected_indices:
            file = self.keyword_files[idx]
            keywords = read_keywords(file)
            all_keywords.extend(keywords)
        
        # Mostrar todos los keywords en la lista
        for kw in all_keywords:
            self.keywords_listbox.insert(tk.END, kw)
    
    def select_all_categories(self):
        for var in self.category_vars:
            var.set(True)
        self.update_keywords_list()
    
    def deselect_all_categories(self):
        for var in self.category_vars:
            var.set(False)
        self.update_keywords_list()
    
    def show_location_info(self):
        # Limpiar información actual
        self.location_info_text.config(state=tk.NORMAL)
        self.location_info_text.delete(1.0, tk.END)
        
        # Obtener las localizaciones seleccionadas
        selected_indices = [i for i, var in enumerate(self.location_vars) if var.get()]
        
        if not selected_indices:
            self.location_info_text.insert(tk.END, "No hay localizaciones seleccionadas.")
            self.location_info_text.config(state=tk.DISABLED)
            return
        
        # Mostrar información de cada localización
        for idx in selected_indices:
            file = self.location_files[idx]
            location_name = self.location_names[idx]
            location_data = read_location(file)
            
            info = f"Localización: {location_name}\n"
            info += f"Zoom: {location_data['zoom']}\n"
            info += f"Latitud: {location_data['lat']}\n"
            info += f"Longitud: {location_data['lon']}\n"
            info += "-" * 30 + "\n"
            
            self.location_info_text.insert(tk.END, info)
        
        self.location_info_text.config(state=tk.DISABLED)
    
    def update_summary(self):
        # Limpiar resumen actual
        self.summary_text.delete(1.0, tk.END)
        
        # Obtener configuración actual
        host = self.host_var.get()
        job_name = self.job_name_var.get()
        radius = self.radius_var.get()
        depth = self.depth_var.get()
        max_time = self.max_time_var.get()
        wait_time = self.wait_time_var.get()
        
        # Obtener categorías seleccionadas
        selected_categories = [i for i, var in enumerate(self.category_vars) if var.get()]
        category_names = [self.category_names[i] for i in selected_categories]
        
        # Obtener localizaciones seleccionadas
        selected_locations = [i for i, var in enumerate(self.location_vars) if var.get()]
        location_names = [self.location_names[i] for i in selected_locations]
        
        # Mostrar resumen
        summary = f"===== RESUMEN DEL TRABAJO =====\n\n"
        summary += f"Host API: {host}\n"
        summary += f"Nombre del trabajo: {job_name}\n"
        summary += f"Radio: {radius} metros\n"
        summary += f"Profundidad: {depth}\n"
        summary += f"Tiempo máximo: {max_time} minutos\n"
        summary += f"Tiempo de espera: {wait_time} minutos\n\n"
        
        summary += f"Categorías seleccionadas ({len(category_names)}):\n"
        for name in category_names:
            summary += f"- {name}\n"
        
        summary += f"\nLocalizaciones seleccionadas ({len(location_names)}):\n"
        for name in location_names:
            summary += f"- {name}\n"
        
        # Calcular total de trabajos
        total_jobs = len(category_names) * len(location_names)
        summary += f"\nTotal de trabajos a ejecutar: {total_jobs}\n"
        
        self.summary_text.insert(tk.END, summary)
    
    def log(self, message):
        self.log_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)
    
    def run_job(self):
        # Validar entradas
        selected_categories = [i for i, var in enumerate(self.category_vars) if var.get()]
        if not selected_categories:
            messagebox.showerror("Error", "Debes seleccionar al menos una categoría")
            return
        
        selected_locations = [i for i, var in enumerate(self.location_vars) if var.get()]
        if not selected_locations:
            messagebox.showerror("Error", "Debes seleccionar al menos una localización")
            return
        
        # Confirmar ejecución
        if not messagebox.askyesno("Confirmar", "¿Deseas iniciar la ejecución de los trabajos?"):
            return
        
        # Iniciar ejecución en un hilo aparte
        self.running = True
        self.run_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.progress.start()
        
        thread = threading.Thread(target=self.execute_jobs)
        thread.daemon = True
        thread.start()
    
    def execute_jobs(self):
        try:
            # Obtener configuración
            host = self.host_var.get()
            api_url = f"{host}/api/v1/jobs"
            job_prefix = self.job_name_var.get()
            radius = self.radius_var.get()
            depth = self.depth_var.get()
            max_time = self.max_time_var.get()
            wait_time = self.wait_time_var.get()
            
            # Obtener categorías seleccionadas
            selected_categories = [i for i, var in enumerate(self.category_vars) if var.get()]
            selected_locations = [i for i, var in enumerate(self.location_vars) if var.get()]
            
            # Contador de trabajos
            job_counter = 0
            completed_jobs = 0
            jobs_info = []
            
            # Procesar cada categoría
            for cat_idx in selected_categories:
                cat_file = self.keyword_files[cat_idx]
                category_name = self.category_names[cat_idx]
                keywords_list = read_keywords(cat_file)
                
                self.log(f"Procesando categoría: {category_name} ({len(keywords_list)} keywords)")
                
                # Procesar cada localización
                for loc_idx in selected_locations:
                    if not self.running:
                        self.log("Ejecución cancelada por el usuario")
                        return
                    
                    loc_file = self.location_files[loc_idx]
                    location_name = self.location_names[loc_idx]
                    location_data = read_location(loc_file)
                    
                    job_counter += 1
                    job_name = f"{job_prefix}_{category_name}_{location_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    
                    self.log(f"Procesando trabajo: {job_name}")
                    
                    # Crear payload
                    payload = {
                        "name": job_name,
                        "keywords": keywords_list,
                        "lang": "es",
                        "zoom": location_data['zoom'],
                        "lat": location_data['lat'],
                        "lon": location_data['lon'],
                        "fast_mode": True,
                        "radius": radius,
                        "depth": depth,
                        "email": True,
                        "max_time": max_time,
                        "proxies": []
                    }
                    
                    # Enviar trabajo
                    self.log(f"Enviando trabajo a la API...")
                    job_id, status_code, response = submit_job(api_url, payload)
                    
                    if job_id:
                        self.log(f"Trabajo creado con ID: {job_id}")
                        self.job_id = job_id
                        
                        # Esperar a que se complete (o al menos un tiempo razonable)
                        self.log(f"Esperando a que el trabajo se procese...")
                        start_time = time.time()
                        
                        try:
                            # Solo esperamos unos segundos para verificar que el trabajo ha empezado a procesarse
                            time.sleep(5)
                            status = check_job_status(job_id, api_url)
                            self.log(f"Estado: {status.get('status', 'Procesando')}")
                        except Exception as e:
                            self.log(f"Error al verificar estado, continuando con el siguiente trabajo: {str(e)}")
                    else:
                        self.log(f"No se pudo obtener ID del trabajo, pero el proceso continuará.")
                    
                    # Registrar información del trabajo
                    jobs_info.append({
                        "id": job_id if job_id else "unknown",
                        "name": job_name,
                        "category": category_name,
                        "location": location_name
                    })
                    
                    completed_jobs += 1
                    
                    # Pequeña pausa entre trabajos
                    time.sleep(2)
            
            self.log(f"Todos los trabajos ({completed_jobs}) han sido enviados al servidor.")
            self.log(f"Para descargar los resultados, por favor visita: {host}")
            
            # Mensaje final con instrucciones
            mensaje = f"Se han enviado {completed_jobs} trabajos al servidor.\n\n"
            mensaje += f"Para ver y descargar los resultados CSV, por favor visita:\n{host}"
            
            messagebox.showinfo("Proceso Completado", mensaje)
        
        except Exception as e:
            self.log(f"Error en la ejecución: {str(e)}")
            # No mostramos mensaje de error, solo lo registramos en el log
            
            # Mensaje final con instrucciones de todos modos
            mensaje = "El proceso ha terminado.\n\n"
            mensaje += f"Para ver y descargar los resultados CSV, por favor visita:\n{self.host_var.get()}"
            messagebox.showinfo("Proceso Completado", mensaje)
        
        finally:
            # Restaurar estado de la interfaz
            self.running = False
            self.job_id = None
            self.progress.stop()
            self.run_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)
    
    def cancel_job(self):
        if messagebox.askyesno("Cancelar", "¿Estás seguro de que deseas cancelar la ejecución?"):
            self.running = False
            self.log("Cancelando ejecución...")
            # No cancelamos inmediatamente el trabajo actual, solo evitamos que se procesen más

if __name__ == "__main__":
    app = GoogleMapsScraper()
    app.mainloop() 