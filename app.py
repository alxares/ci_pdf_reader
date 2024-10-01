import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
from lector import extraer_datos_pdf  # Importar la función de extracción del lector.py

# Función para cargar el archivo y mostrar el nombre en la interfaz
def cargar_archivo():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")],
        title="Seleccionar archivo PDF"
    )
    if file_path:
        label_archivo.config(text=f"Archivo seleccionado: {file_path}")
        return file_path
    return None

# Función para ejecutar la extracción de datos en segundo plano
def extraer_datos_thread():
    # Ejecutar la extracción en un hilo aparte para evitar que la GUI se congele
    thread = threading.Thread(target=extraer_datos)
    thread.start()

# Función para extraer datos usando la función del lector.py
def extraer_datos():
    file_path = label_archivo.cget("text").replace("Archivo seleccionado: ", "")
    if not file_path:
        messagebox.showwarning("Advertencia", "Por favor, seleccione un archivo PDF primero.")
        return

    try:
        # Llamar a la función de extracción de datos en el archivo lector.py
        df_datos = extraer_datos_pdf(file_path)

        # Limpiar el widget de texto y mostrar los datos extraídos
        text_resultado.delete("1.0", tk.END)
        if not df_datos.empty:
            text_resultado.insert(tk.END, df_datos.to_string(index=False))
        else:
            text_resultado.insert(tk.END, "No se encontraron datos en el documento.")

        # Eliminar el archivo temporal si se ha creado uno
        if os.path.exists("temp.pdf"):
            os.remove("temp.pdf")

    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Extractor de Datos de PDF - Ligero")
ventana.geometry("700x500")

# Evitar redimensionamiento para reducir la carga de renderizado
ventana.resizable(False, False)

# Etiqueta y Botón para cargar el archivo
label_archivo = tk.Label(ventana, text="No se ha seleccionado ningún archivo", wraplength=600)
label_archivo.pack(pady=20)

boton_cargar = tk.Button(ventana, text="Cargar Archivo PDF", command=cargar_archivo)
boton_cargar.pack(pady=10)

# Botón para extraer los datos (usa threading)
boton_extraer = tk.Button(ventana, text="Extraer Datos", command=extraer_datos_thread)
boton_extraer.pack(pady=10)

# Text Widget para mostrar los resultados
text_resultado = tk.Text(ventana, height=15, width=80, wrap=tk.WORD)
text_resultado.pack(pady=20)

# Ejecutar la interfaz gráfica
ventana.mainloop()
