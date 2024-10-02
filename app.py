from tkinter import filedialog, messagebox
from tkinter import ttk
import tkinter as tk
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

        # Limpiar el Treeview anterior
        for i in tree.get_children():
            tree.delete(i)

        if not df_datos.empty:
            # Configurar las columnas del Treeview
            tree["column"] = list(df_datos.columns)
            tree["show"] = "headings"  # Mostrar solo los encabezados de columna

            # Configurar encabezados y columnas
            for col in df_datos.columns:
                tree.heading(col, text=col)
                tree.column(col, width=150, anchor='center')  # Ajustar ancho y centrar

            # Insertar cada fila de datos en el Treeview
            for index, row in df_datos.iterrows():
                tree.insert("", "end", values=list(row))
        else:
            messagebox.showinfo("Información", "No se encontraron datos en el documento.")

    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Extractor de Datos de PDF - Ligero")
ventana.geometry("1000x600")  # Ajustar la ventana para mayor espacio

# Evitar redimensionamiento
ventana.resizable(True, True)

# Etiqueta y Botón para cargar el archivo
label_archivo = tk.Label(ventana, text="No se ha seleccionado ningún archivo", wraplength=600)
label_archivo.pack(pady=20)

boton_cargar = tk.Button(ventana, text="Cargar Archivo PDF", command=cargar_archivo)
boton_cargar.pack(pady=10)

# Botón para extraer los datos (usa threading)
boton_extraer = tk.Button(ventana, text="Extraer Datos", command=extraer_datos_thread)
boton_extraer.pack(pady=10)

# Crear Frame para contener el Treeview y las barras de desplazamiento
frame = tk.Frame(ventana)
frame.pack(pady=20, fill=tk.BOTH, expand=True)

# Barra de desplazamiento vertical
scroll_y = ttk.Scrollbar(frame, orient=tk.VERTICAL)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

# Barra de desplazamiento horizontal
scroll_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

# Crear el Treeview con scrollbars
tree = ttk.Treeview(frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
tree.pack(expand=True, fill=tk.BOTH)

# Configurar las barras de desplazamiento para el Treeview
scroll_y.config(command=tree.yview)
scroll_x.config(command=tree.xview)

# Ejecutar la interfaz gráfica
ventana.mainloop()
