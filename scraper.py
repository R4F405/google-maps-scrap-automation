import os
import json
import requests
import time
from os import listdir
from os.path import isfile, join

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

def main():
    print("===== GOOGLE MAPS SCRAPER =====")
    name = input("Introduce un nombre para este trabajo: ")
    
    # Seleccionar categoría de keywords
    keyword_file = display_keywords_categories()
    keywords = read_keywords(keyword_file)
    
    print(f"\nKeywords disponibles en esta categoría:")
    for i, kw in enumerate(keywords, 1):
        print(f"{i}. {kw}")
    
    kw_choice = int(input("\nSelecciona un keyword (1-" + str(len(keywords)) + "): "))
    if 1 <= kw_choice <= len(keywords):
        selected_keyword = keywords[kw_choice-1]
    else:
        print("Selección inválida, usando el primer keyword")
        selected_keyword = keywords[0]
    
    # Seleccionar localización
    location_file = display_locations()
    location_data = read_location(location_file)
    
    # Construir solicitud API
    api_url = "http://localhost:8000/api/v1/jobs"
    payload = {
        "name": name,
        "keywords": [selected_keyword],
        "lang": "es",
        "zoom": location_data['zoom'],
        "lat": location_data['lat'],
        "lon": location_data['lon'],
        "fast_mode": True,
        "radius": 10000,
        "depth": 10,
        "email": True,
        "max_time": 15,
        "proxies": []
    }
    
    print("\nResumen de la solicitud:")
    print(f"Nombre: {name}")
    print(f"Keyword: {selected_keyword}")
    print(f"Localización: {location_file.split('_location_')[1].split('.')[0]}")
    print(f"Coordenadas: Lat {location_data['lat']}, Lon {location_data['lon']}")
    print(f"Zoom: {location_data['zoom']}")
    
    confirm = input("\n¿Deseas proceder con la solicitud? (s/n): ")
    if confirm.lower() == 's':
        try:
            response = requests.post(api_url, json=payload)
            print(f"\nRespuesta de la API (Status {response.status_code}):")
            print(response.json())
            
            # Verificar estado del trabajo
            if response.status_code == 201:
                job_id = response.json().get('id')
                print(f"\nTrabajo creado con ID: {job_id}")
                print("Puedes verificar el estado con GET /api/v1/jobs/{job_id}")
        except Exception as e:
            print(f"Error al enviar la solicitud: {str(e)}")
    else:
        print("Operación cancelada")

if __name__ == "__main__":
    main() 