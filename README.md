# PDF Data Extractor

Este proyecto permite extraer datos clave de un archivo PDF utilizando OCR (Reconocimiento Óptico de Caracteres) con la librería `pytesseract`,
junto con la conversión de PDF a imágenes mediante `pdf2image` y el procesamiento de imágenes con `PIL`. Los datos se extraen mediante expresiones regulares aplicadas al texto resultante del OCR.

## Requisitos

Asegúrate de tener instaladas las siguientes dependencias antes de ejecutar el script:

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) instalado en tu sistema.
- Las siguientes librerías de Python:

bash
`pip install pytesseract pdf2image pillow pandas`

# Además, es necesario configurar la ruta a Tesseract en tu sistema. Si utilizas Windows, puedes hacerlo de la siguiente manera en tu script:

`pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`

# Uso
Convertir PDF a texto y extraer datos clave:

El script convierte las páginas de un archivo PDF a imágenes y luego realiza OCR sobre cada una de ellas. Posteriormente, mediante expresiones regulares, extrae datos clave como:

Nombre y Apellido
Fecha de Nacimiento
Número de CI
Lugar de Nacimiento
Nacionalidad
Estado Civil
Fecha de Emisión

# Modificación del archivo PDF:

`Modifica la variable file_path con la ruta del archivo PDF que deseas analizar.`

# Salida de los datos:

Los datos extraídos se guardan en un DataFrame de Pandas y se muestran en la consola.

# Ejecución
Una vez que hayas modificado el file_path con la ruta correcta de tu archivo PDF, puedes ejecutar el script de la siguiente manera:

`python main.py`

La salida mostrará los datos extraídos en formato de tabla.

# Cargar el PDF
`file_path = 'C:/ruta/al/archivo.pdf'`  # Aca se agrega la direccion del archivo PDF a analizar
`df_datos = extraer_datos_pdf(file_path)`

# Mostrar el DataFrame con los datos extraídos
`print(df_datos)`

# Notas adicionales
Las expresiones regulares utilizadas están basadas en un OCR aproximado, por lo que algunos patrones pueden necesitar ajustes dependiendo de la calidad del PDF y el texto extraído.
El archivo PDF debe contener información estructurada en un formato compatible con las expresiones regulares para que la extracción sea exitosa.
Verifica que la resolución de las imágenes generadas desde el PDF sea adecuada para el OCR (300 dpi es recomendado).
# Contribución
Si deseas contribuir a este proyecto, puedes hacerlo abriendo un Pull Request o reportando problemas en la sección de Issues.

Licencia
Este proyecto está bajo la licencia MIT.
