"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    import pandas as pd
    import re
    
    # Leer el archivo
    with open('files/input/clusters_report.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Procesar las líneas para extraer los datos
    data = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Saltar líneas vacías, encabezados y líneas de separación
        if (not line or 
            line.startswith('Cluster') or 
            line.startswith('-----') or
            'palabras clave' in line):
            i += 1
            continue
        
        # Buscar líneas que empiecen con un número (datos del cluster)
        if re.match(r'^\s*\d+', line):
            # Extraer los datos usando regex para manejar espacios múltiples
            match = re.match(r'^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)', line)
            
            if match:
                cluster = int(match.group(1))
                cantidad = int(match.group(2))
                porcentaje = float(match.group(3).replace(',', '.'))
                palabras_inicio = match.group(4).strip()
                
                # Recolectar todas las líneas de palabras clave
                palabras_completas = [palabras_inicio] if palabras_inicio else []
                j = i + 1
                
                # Continuar leyendo líneas indentadas (continuación de palabras clave)
                while j < len(lines):
                    next_line = lines[j].rstrip()
                    if (next_line and 
                        next_line.startswith(' ') and 
                        not re.match(r'^\s*\d+', next_line)):
                        palabras_completas.append(next_line.strip())
                        j += 1
                    else:
                        break
                
                # Unir todas las palabras clave
                palabras_texto = ' '.join(palabras_completas)
                
                # Limpiar espacios extra y normalizar
                palabras_texto = re.sub(r'\s+', ' ', palabras_texto)
                
                # Remover el punto final si existe
                if palabras_texto.endswith('.'):
                    palabras_texto = palabras_texto[:-1]
                
                # Separar por comas y limpiar cada palabra clave
                palabras_lista = []
                for palabra in palabras_texto.split(','):
                    palabra = palabra.strip()
                    if palabra:
                        palabras_lista.append(palabra)
                
                # Unir con formato requerido: coma + espacio
                palabras_formateadas = ', '.join(palabras_lista)
                
                data.append({
                    'cluster': cluster,
                    'cantidad_de_palabras_clave': cantidad,
                    'porcentaje_de_palabras_clave': porcentaje,
                    'principales_palabras_clave': palabras_formateadas
                })
                
                i = j
            else:
                i += 1
        else:
            i += 1
    
    # Crear el DataFrame
    df = pd.DataFrame(data)
    
    return df