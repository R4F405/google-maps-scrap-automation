import os
import json
import requests
import time
from os import listdir
from os.path import isfile, join
from datetime import datetime

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

def display_keywords_categories():
    """Muestra todas las categorías de keywords para que el usuario seleccione"""
    keyword_files = get_keyword_files()
    print("\nDisponibles categorías de keywords:")
    for i, file in enumerate(keyword_files, 1):
        category = file.split('_keywords_')[1].split('.')[0]
        print(f"{i}. {category}")
    
    choice = int(input("\nSelecciona una categoría (1-13): "))
    if 1 <= choice <= len(keyword_files):
        return keyword_files[choice-1]
    else:
        print("Selección inválida")
        return display_keywords_categories()

def display_locations():
    """Muestra todas las localizaciones para que el usuario seleccione"""
    location_files = get_location_files()
    print("\nLocalizaciones disponibles:")
    for i, file in enumerate(location_files, 1):
        location = file.split('_location_')[1].split('.')[0]
        print(f"{i}. {location}")
    
    choice = int(input("\nSelecciona una localización (1-4): "))
    if 1 <= choice <= len(location_files):
        return location_files[choice-1]
    else:
        print("Selección inválida")
        return display_locations()

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

def select_multiple_keywords(keywords):
    """Permite al usuario seleccionar múltiples keywords"""
    print(f"\nKeywords disponibles en esta categoría:")
    for i, kw in enumerate(keywords, 1):
        print(f"{i}. {kw}")
    
    print("\nSelecciona keywords (separados por comas, o 'all' para todos):")
    selection = input(">>> ")
    
    if selection.lower() == 'all':
        return keywords
    
    try:
        indices = [int(idx.strip()) for idx in selection.split(',')]
        selected = []
        for idx in indices:
            if 1 <= idx <= len(keywords):
                selected.append(keywords[idx-1])
            else:
                print(f"Índice {idx} fuera de rango, ignorado")
        
        if not selected:
            print("No se seleccionaron keywords válidos, usando el primero")
            return [keywords[0]]
        
        return selected
    except ValueError:
        print("Entrada inválida, usando el primer keyword")
        return [keywords[0]]

def check_job_status(job_id, api_url):
    """Verifica el estado de un trabajo"""
    status_url = f"{api_url}/{job_id}"
    try:
        response = requests.get(status_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al verificar el estado: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al verificar el estado: {str(e)}")
        return None

def save_job_results(job_id, result, location_name, keywords):
    """Guarda los resultados del trabajo en un archivo"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    keywords_str = "_".join([kw.replace(" ", "_") for kw in keywords[:2]])  # Primeros 2 keywords para el nombre del archivo
    filename = f"results_{location_name}_{keywords_str}_{timestamp}.json"
    
    os.makedirs('results', exist_ok=True)
    
    with open(os.path.join('results', filename), 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Resultados guardados en: results/{filename}")

def submit_job(api_url, payload):
    """Envía un trabajo a la API"""
    try:
        response = requests.post(api_url, json=payload)
        print(f"\nRespuesta de la API (Status {response.status_code}):")
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result.get('id') if 'id' in result else None
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Error al enviar la solicitud: {str(e)}")
        return None

def main():
    print("===== GOOGLE MAPS SCRAPER AVANZADO =====")
    
    # Configuración de la API
    api_host = input("Introduce la dirección del servidor API (por defecto: http://localhost:8000): ")
    if not api_host:
        api_host = "http://localhost:8000"
    
    api_url = f"{api_host}/api/v1/jobs"
    
    name = input("Introduce un nombre para este trabajo: ")
    if not name:
        name = f"Trabajo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Seleccionar categoría de keywords
    keyword_file = display_keywords_categories()
    category = keyword_file.split('_keywords_')[1].split('.')[0]
    keywords = read_keywords(keyword_file)
    
    # Seleccionar múltiples keywords
    selected_keywords = select_multiple_keywords(keywords)
    print(f"\nSeleccionados {len(selected_keywords)} keywords")
    
    # Seleccionar localización
    location_file = display_locations()
    location_name = location_file.split('_location_')[1].split('.')[0]
    location_data = read_location(location_file)
    
    # Configurar parámetros adicionales
    radius = input("\nIntroduce el radio de búsqueda (por defecto: 10000): ")
    radius = int(radius) if radius.isdigit() else 10000
    
    depth = input("Introduce la profundidad de búsqueda (por defecto: 10): ")
    depth = int(depth) if depth.isdigit() else 10
    
    max_time = input("Introduce el tiempo máximo en minutos (por defecto: 15): ")
    max_time = int(max_time) if max_time.isdigit() else 15
    
    # Construir solicitud API
    payload = {
        "name": name,
        "keywords": selected_keywords,
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
    
    print("\nResumen de la solicitud:")
    print(f"Nombre: {name}")
    print(f"Categoría: {category}")
    print(f"Keywords: {', '.join(selected_keywords[:5])}{'...' if len(selected_keywords) > 5 else ''}")
    print(f"Total keywords: {len(selected_keywords)}")
    print(f"Localización: {location_name}")
    print(f"Coordenadas: Lat {location_data['lat']}, Lon {location_data['lon']}")
    print(f"Zoom: {location_data['zoom']}")
    print(f"Radio: {radius} metros")
    print(f"Profundidad: {depth}")
    print(f"Tiempo máximo: {max_time} minutos")
    
    confirm = input("\n¿Deseas proceder con la solicitud? (s/n): ")
    if confirm.lower() != 's':
        print("Operación cancelada")
        return
    
    # Enviar trabajo
    job_id = submit_job(api_url, payload)
    
    if not job_id:
        print("No se pudo crear el trabajo")
        return
    
    print(f"\nTrabajo creado con ID: {job_id}")
    
    # Monitorear estado del trabajo
    monitor = input("¿Deseas monitorear el estado del trabajo? (s/n): ")
    if monitor.lower() != 's':
        return
    
    print("\nMonitorizando el estado del trabajo...")
    print("Presiona Ctrl+C para detener el monitoreo")
    
    try:
        while True:
            status = check_job_status(job_id, api_url)
            if status:
                print(f"\nEstado actual: {status.get('status', 'Desconocido')}")
                
                if 'result' in status and status['result']:
                    print("¡Trabajo completado!")
                    save_job_results(job_id, status['result'], location_name, selected_keywords)
                    break
                
                if status.get('status') == 'failed':
                    print("El trabajo ha fallado")
                    if 'error' in status:
                        print(f"Error: {status['error']}")
                    break
            
            print("Esperando 10 segundos para la próxima verificación...")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nMonitoreo detenido por el usuario")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
    finally:
        print("\nFin del programa") 