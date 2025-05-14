import os
import json
import requests
import time
import argparse
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

def save_job_results(job_id, result, location_name, keywords, category):
    """Guarda los resultados del trabajo en un archivo"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results_{location_name}_{category}_{timestamp}.json"
    
    os.makedirs('results', exist_ok=True)
    
    with open(os.path.join('results', filename), 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Resultados guardados en: results/{filename}")
    return filename

def submit_job(api_url, payload):
    """Envía un trabajo a la API"""
    try:
        response = requests.post(api_url, json=payload)
        print(f"API Response (Status {response.status_code})")
        
        if response.status_code in [200, 201]:
            result = response.json()
            return result.get('id') if 'id' in result else None
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Error al enviar la solicitud: {str(e)}")
        return None

def wait_for_job_completion(job_id, api_url, max_wait_time=30, check_interval=10):
    """Espera a que un trabajo se complete, con tiempo límite"""
    print(f"Esperando a que el trabajo {job_id} se complete...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait_time * 60:  # Convertir a segundos
        status = check_job_status(job_id, api_url)
        
        if status:
            print(f"Estado: {status.get('status', 'Desconocido')}")
            
            if 'result' in status and status['result']:
                print("¡Trabajo completado!")
                return status
            
            if status.get('status') == 'failed':
                print("El trabajo ha fallado")
                if 'error' in status:
                    print(f"Error: {status['error']}")
                return None
        
        print(f"Esperando {check_interval} segundos...")
        time.sleep(check_interval)
    
    print(f"Tiempo de espera agotado para el trabajo {job_id}")
    return None

def get_args():
    """Analiza los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description='Google Maps Batch Scraper')
    parser.add_argument('--host', default='http://localhost:8000', help='API host URL')
    parser.add_argument('--categories', type=str, help='Índices de categorías separados por comas (ej: "1,2,3")')
    parser.add_argument('--locations', type=str, help='Índices de localizaciones separados por comas (ej: "1,2")')
    parser.add_argument('--keywords', type=str, default='all', help='Keywords específicos o "all" para todos')
    parser.add_argument('--radius', type=int, default=10000, help='Radio de búsqueda en metros')
    parser.add_argument('--depth', type=int, default=10, help='Profundidad de búsqueda')
    parser.add_argument('--max-time', type=int, default=15, help='Tiempo máximo para cada trabajo en minutos')
    parser.add_argument('--wait-time', type=int, default=30, help='Tiempo máximo de espera para completar un trabajo en minutos')
    parser.add_argument('--job-prefix', type=str, default='', help='Prefijo para los nombres de trabajos')
    parser.add_argument('--dry-run', action='store_true', help='Mostrar detalles sin enviar trabajos')
    
    return parser.parse_args()

def process_job(api_url, name, category_name, keywords, location_data, location_name, radius, depth, max_time, wait_time, dry_run=False):
    """Procesa un trabajo individual"""
    payload = {
        "name": name,
        "keywords": keywords,
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
    
    print("\n" + "="*50)
    print(f"TRABAJO: {name}")
    print(f"Categoría: {category_name}")
    print(f"Keywords: {', '.join(keywords[:3])}{'...' if len(keywords) > 3 else ''}")
    print(f"Total keywords: {len(keywords)}")
    print(f"Localización: {location_name}")
    print(f"Coordenadas: Lat {location_data['lat']}, Lon {location_data['lon']}")
    print(f"Zoom: {location_data['zoom']}, Radio: {radius}m, Profundidad: {depth}")
    print("="*50)
    
    if dry_run:
        print("Modo simulación: No se enviará el trabajo")
        return None, None
    
    # Enviar trabajo
    job_id = submit_job(api_url, payload)
    
    if not job_id:
        print("No se pudo crear el trabajo")
        return None, None
    
    print(f"Trabajo creado con ID: {job_id}")
    
    # Esperar a que se complete
    result = wait_for_job_completion(job_id, api_url, max_wait_time=wait_time)
    
    if result and 'result' in result:
        filename = save_job_results(job_id, result['result'], location_name, keywords, category_name)
        return job_id, filename
    
    return job_id, None

def main():
    args = get_args()
    
    # Configuración
    api_url = f"{args.host}/api/v1/jobs"
    
    # Obtener archivos de keywords y localización disponibles
    keyword_files = get_keyword_files()
    location_files = get_location_files()
    
    # Determinar qué categorías procesar
    if args.categories:
        category_indices = [int(idx.strip()) for idx in args.categories.split(',')]
        selected_categories = []
        for idx in category_indices:
            if 1 <= idx <= len(keyword_files):
                selected_categories.append(keyword_files[idx-1])
            else:
                print(f"Índice de categoría inválido: {idx}")
    else:
        selected_categories = keyword_files
    
    # Determinar qué localizaciones procesar
    if args.locations:
        location_indices = [int(idx.strip()) for idx in args.locations.split(',')]
        selected_locations = []
        for idx in location_indices:
            if 1 <= idx <= len(location_files):
                selected_locations.append(location_files[idx-1])
            else:
                print(f"Índice de localización inválido: {idx}")
    else:
        selected_locations = location_files
    
    # Resumen de elementos seleccionados
    print("\n===== GOOGLE MAPS BATCH SCRAPER =====")
    print(f"Procesando {len(selected_categories)} categorías:")
    for cat in selected_categories:
        category = cat.split('_keywords_')[1].split('.')[0]
        print(f"- {category}")
    
    print(f"\nProcesando {len(selected_locations)} localizaciones:")
    for loc in selected_locations:
        location = loc.split('_location_')[1].split('.')[0]
        print(f"- {location}")
    
    print(f"\nConfiguración:")
    print(f"- API Host: {args.host}")
    print(f"- Radio: {args.radius}m")
    print(f"- Profundidad: {args.depth}")
    print(f"- Tiempo máximo por trabajo: {args.max_time} minutos")
    print(f"- Tiempo de espera por trabajo: {args.wait_time} minutos")
    
    if args.dry_run:
        print("\nMODO SIMULACIÓN ACTIVADO: No se enviarán trabajos reales")
    
    if not args.dry_run:
        confirm = input("\n¿Deseas proceder con los trabajos? (s/n): ")
        if confirm.lower() != 's':
            print("Operación cancelada")
            return
    
    # Crear archivo de resumen
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = f"batch_summary_{timestamp}.json"
    summary = {
        "timestamp": timestamp,
        "api_host": args.host,
        "categories": [],
        "total_jobs": 0,
        "successful_jobs": 0,
        "failed_jobs": 0,
        "jobs": []
    }
    
    job_counter = 0
    
    # Procesar cada combinación de categoría-localización
    for cat_file in selected_categories:
        category_name = cat_file.split('_keywords_')[1].split('.')[0]
        keywords_list = read_keywords(cat_file)
        
        # Filtrar keywords si se solicita
        if args.keywords.lower() != 'all':
            requested_keywords = [kw.strip() for kw in args.keywords.split(',')]
            keywords_list = [kw for kw in keywords_list if any(req.lower() in kw.lower() for req in requested_keywords)]
            if not keywords_list:
                print(f"No se encontraron keywords que coincidan con '{args.keywords}' en la categoría {category_name}")
                continue
        
        category_info = {
            "name": category_name,
            "total_keywords": len(keywords_list),
            "locations": []
        }
        
        for loc_file in selected_locations:
            location_name = loc_file.split('_location_')[1].split('.')[0]
            location_data = read_location(loc_file)
            
            job_counter += 1
            job_name = f"{args.job_prefix}Trabajo_{category_name}_{location_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Procesar trabajo
            job_id, result_file = process_job(
                api_url, job_name, category_name, keywords_list, location_data, location_name,
                args.radius, args.depth, args.max_time, args.wait_time, args.dry_run
            )
            
            # Actualizar resumen
            location_info = {
                "name": location_name,
                "job_id": job_id,
                "result_file": result_file,
                "status": "success" if result_file else "failed" if job_id else "not_submitted"
            }
            
            category_info["locations"].append(location_info)
            
            if job_id:
                job_info = {
                    "id": job_id,
                    "name": job_name,
                    "category": category_name,
                    "location": location_name,
                    "result_file": result_file,
                    "status": "success" if result_file else "failed"
                }
                summary["jobs"].append(job_info)
                
                if result_file:
                    summary["successful_jobs"] += 1
                else:
                    summary["failed_jobs"] += 1
            
            # Esperar entre trabajos para evitar sobrecargar la API
            if not args.dry_run and job_id:
                print("Esperando 5 segundos antes del siguiente trabajo...")
                time.sleep(5)
        
        summary["categories"].append(category_info)
    
    summary["total_jobs"] = job_counter
    
    # Guardar resumen
    os.makedirs('results', exist_ok=True)
    with open(os.path.join('results', summary_file), 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\nResumen del batch guardado en: results/{summary_file}")
    print(f"Total de trabajos: {summary['total_jobs']}")
    print(f"Trabajos exitosos: {summary['successful_jobs']}")
    print(f"Trabajos fallidos: {summary['failed_jobs']}")
    
    print("\nFin del procesamiento por lotes")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
    finally:
        print("\nFin del programa") 