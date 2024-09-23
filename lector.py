import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import re
import pandas as pd

# Función para extraer datos clave desde un archivo PDF
def extraer_datos_pdf(file_path):
    # Convertir el PDF a imágenes
    pages = convert_from_path(file_path, 300)
    
    # Realizar OCR en cada página
    text = ''
    for page in pages:
        text += pytesseract.image_to_string(page)
    
    # Expresiones regulares para extraer los datos clave
    dob_pattern = r'FECHA DE NACIMIENTO\n(\d{2}-\d{2}-\d{4})'
    lugar_nacimiento_pattern = r'LUGAR DE NACIMENTO\n(\w+)'
    ci_pattern_idpry = r'IDPRY(\d{7})<<'
    nacionalidad_pattern = r'NACIONALIDAD:\s*(\w+)'
    estado_civil_pattern = r'estapocwwi:\s*(\w+)'  # Basado en el OCR aproximado
    emision_pattern = r'FECHADEEMISION\s*(\d{2}-\d{2}-\d{4})'
    nombre_pattern_completo = r'([A-Z]+(?:<[A-Z]+)+)<<([A-Z]+(?:<[A-Z]+)+)'


    # Buscar los datos clave en el texto extraído
    fecha_nacimiento = re.search(dob_pattern, text)
    lugar_nacimiento = re.search(lugar_nacimiento_pattern, text)
    numero_ci = re.search(ci_pattern_idpry, text)
    nacionalidad = re.search(nacionalidad_pattern, text)
    estado_civil = re.search(estado_civil_pattern, text)
    fecha_emision = re.search(emision_pattern, text)
    nombre_apellido = re.search(nombre_pattern_completo, text)

    # Extraer los datos si se encuentran
    fecha_nacimiento = fecha_nacimiento.group(1) if fecha_nacimiento else None
    lugar_nacimiento = lugar_nacimiento.group(1) if lugar_nacimiento else None
    numero_ci = numero_ci.group(1) if numero_ci else None
    nacionalidad = nacionalidad.group(1) if nacionalidad else None
    estado_civil = estado_civil.group(1) if estado_civil else None
    fecha_emision = fecha_emision.group(1) if fecha_emision else None
    nombre_completo = (nombre_apellido.group(1).replace('<', ' ') + ' ' + 
                       nombre_apellido.group(2).replace('<', ' ')) if nombre_apellido else None

    # Crear un diccionario con los datos extraídos
    datos = {
        'Nombre y Apellido': nombre_completo,
        'Fecha de Nacimiento': fecha_nacimiento,
        'Número de CI': numero_ci,
        'Lugar de Nacimiento': lugar_nacimiento,
        'Nacionalidad': nacionalidad,
        'Estado Civil': estado_civil,
        'Fecha de Emisión': fecha_emision
    }

    # Retornar los datos en formato DataFrame
    df = pd.DataFrame([datos])
    return df

# Cargar el PDF
file_path = 'C:/Users/argal/Downloads/ci_prueba_2.pdf'  # Aca se agrega la direccion del archivo PDF a analizar
df_datos = extraer_datos_pdf(file_path)

# Mostrar el DataFrame con los datos extraídos
print(df_datos)
