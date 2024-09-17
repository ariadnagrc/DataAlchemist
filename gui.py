import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages
from dataAlchemist import convert_file, df_global
import os

def open_file(event=None):
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if file_path:
        file_label.config(text=file_path)
        load_preview(file_path)

def drop(event):
    file_path = event.data
    file_label.config(text=file_path)
    load_preview(file_path)

def load_preview(file_path):
    try:
        df = pd.read_excel(file_path)
        tree.delete(*tree.get_children())

        tree["columns"] = list(df.columns)
        for col in tree["columns"]:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=100, minwidth=100, stretch=tk.NO, anchor="center")

        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        tree["show"] = "headings"

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar vista previa: {str(e)}")

def on_format_select(event):
    format_selected = format_combobox.get()

# Crear ventana principal
root = TkinterDnD.Tk()
root.title("Data Alchemist")
root.geometry("800x600")
root.configure(bg="#2c2c2c")

# Establecer icono
root.iconbitmap('assets/icon/iconoDataAlchemist.ico')

# Marco principal
main_frame = tk.Frame(root, bg="#2c2c2c")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Configurar columnas y filas del marco principal
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=2) 
main_frame.columnconfigure(2, weight=3)
main_frame.columnconfigure(3, weight=4)
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=2)

# Crear frame para seleccionar archivo
file_select_frame = tk.Frame(main_frame, bg="#1e1e1e", width=250, height=300)
file_select_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
file_select_frame.pack_propagate(False)

file_select_title = tk.Label(file_select_frame, text="Selecciona o arrastra un archivo", font=("Helvetica Neue", 12, "bold"), bg="#1e1e1e", fg="white")
file_select_title.pack(pady=(30, 10))

drag_drop_frame = tk.Frame(file_select_frame, bg="#1e1e1e", highlightbackground="#9e64a7", highlightthickness=2, highlightcolor="#5c5c5c")
drag_drop_frame.pack(fill="both", expand=True, padx=20, pady=20)

file_label = tk.Label(drag_drop_frame, text="No se ha seleccionado ningún archivo", wraplength=150, bg="#1e1e1e", fg="white", font=("Helvetica Neue", 10))
file_label.pack(expand=True, pady=(30, 0))

select_button = tk.Button(drag_drop_frame, text="Seleccionar archivo", command=open_file, font=("Helvetica Neue", 10), bg="#592d80", fg="#ffffff", relief="flat")
select_button.pack(side="bottom", pady=10)

file_select_frame.drop_target_register(DND_FILES)
file_select_frame.dnd_bind('<<Drop>>', drop)

# Crear el frame para la vista previa
preview_frame = tk.Frame(main_frame, bg="#1e1e1e", width=250, height=300)
preview_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
preview_frame.pack_propagate(False)

preview_label = tk.Label(preview_frame, text="Vista previa:", font=("Helvetica Neue", 12, "bold"), bg="#1e1e1e", fg="white")
preview_label.pack(pady=10)

tree_container = tk.Frame(preview_frame, bg="#1e1e1e")
tree_container.pack(fill="both", expand=True)

style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview", background="#1e1e1e", foreground="white", fieldbackground="#1e1e1e", rowheight=25)
style.configure("Treeview.Heading", background="#2c2c2c", foreground="white", font=("Helvetica Neue", 10, "bold"))

tree = ttk.Treeview(tree_container, show='headings', height=8, style="Treeview")
scrollbar_vertical = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
scrollbar_horizontal = ttk.Scrollbar(tree_container, orient="horizontal", command=tree.xview)
tree.configure(yscroll=scrollbar_vertical.set, xscroll=scrollbar_horizontal.set)

scrollbar_vertical.pack(side="right", fill="y")
scrollbar_horizontal.pack(side="bottom", fill="x")
tree.pack(side="left", fill="both", expand=True)

style.configure("TScrollbar", troughcolor="#1e1e1e", background="#3b3b3b", gripcount=0, arrowcolor="#ffffff")
style.map("TScrollbar", background=[('active', '#5c5c5c')])

# Crear el frame para la sección derecha
right_frame = tk.Frame(main_frame, bg="#1e1e1e")
right_frame.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="nsew")

right_label = tk.Label(right_frame, text="Selecciona el tipo de conversión", font=("Helvetica Neue", 12, "bold"), bg="#1e1e1e", fg="white")
right_label.pack(pady=(25, 25))  # Aumentar el padding superior e inferior

format_combobox = ttk.Combobox(right_frame, values=["CSV", "ARFF"], state="readonly", font=("Helvetica Neue", 10))
format_combobox.pack(pady=(0, 20))  # Dejar más espacio con la opción inferior

# Crear un frame para la selección de ruta
save_frame = tk.Frame(right_frame, bg="#1e1e1e", highlightbackground="#9e64a7", highlightthickness=1)
save_frame.pack(expand=True, pady=(15, 15), padx=(50,50), fill="x")

# Función para seleccionar la ruta de guardado
def choose_save_location():
    save_directory = filedialog.askdirectory()
    if save_directory:
        save_path_label.config(text=f"Guardar en: {save_directory}")
        convert_button.config(state="normal", bg="#cc66df")

# Etiqueta y botón para seleccionar la ubicación de guardado
save_path_label = tk.Label(save_frame, text="Guardar en: ", bg="#1e1e1e", fg="white", font=("Helvetica Neue", 10))
save_path_label.pack(side="left", padx=(30,30))

select_save_button = tk.Button(save_frame, text="Seleccionar ruta", command=choose_save_location, font=("Helvetica Neue", 10), bg="#592d80", fg="#ffffff", relief="flat")
select_save_button.pack(side="right", padx=(30, 30), pady=10) 

# Función para convertir el archivo al formato seleccionado
def convert():
    file_path = file_label.cget("text")
    
    if not file_path or file_path == "No se ha seleccionado ningún archivo":
        messagebox.showerror("Error", "Debes seleccionar un archivo.")
        return

    format_selected = format_combobox.get()
    
    if not format_selected:
        messagebox.showerror("Error", "Selecciona un formato para guardar.")
        return
    save_directory = save_path_label.cget("text").replace("Guardar en: ", "")
    
    if not save_directory and format_selected == "CSV":
        messagebox.showerror("Error", "Selecciona una ruta para guardar el archivo.")
        return
    
    try:
        file_path_out, df_global = convert_file(file_path, format_selected)  # Obtener la ruta y el DataFrame

        if format_selected == "ARFF":
            messagebox.showinfo("Éxito", f"Archivo convertido a ARFF: {file_path_out}")
            # Aquí puedes cargar el DataFrame en la gráfica
            graphing(df_global)  # Supongamos que tienes una función para cargar la gráfica
        else:
            messagebox.showinfo("Éxito", f"Archivo convertido a CSV: {file_path_out}")

    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error al convertir: {str(e)}")

# Botón para convertir archivo
convert_button = tk.Button(right_frame, text="Convertir archivo", command=convert, font=("Helvetica Neue", 10), bg="#a5a5a5", fg="#ffffff", relief="flat", state="disabled")
convert_button.pack(expand=True) 

# Crear frame para visualizar las gráficas
graphic_preview_frame = tk.Frame(main_frame, bg="#1e1e1e", height=60)
graphic_preview_frame.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")
graphic_preview_frame.columnconfigure(0, weight=0)
graphic_preview_frame.columnconfigure(1, weight=2)
graphic_preview_frame.rowconfigure(0, weight=1)


# Variables globales para almacenar datos y el índice de la gráfica actual
datos = None
indice_actual = 0

# Crear la figura para la gráfica
fig = plt.Figure(figsize=(4, 3))
fig.set_facecolor("#1e1e1e")

# Crear el canvas de tkinter para insertar la figura en el frame
canvas = FigureCanvasTkAgg(fig, master=graphic_preview_frame)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Función para actualizar el gráfico
def actualizar_grafico():
    global indice_actual, datos
    fig.clear()     # Limpiar la figura anterior
    atributo = datos.columns[indice_actual]     # Obtener el nombre del atributo actual
    ax = fig.add_subplot(111)     # Crear un nuevo gráfico para el atributo actual
    ax.set_facecolor("#1e1e1e")  # Color de fondo del gráfico
    
    # Verificar el tipo de dato para decidir qué gráfico usar
    if pd.api.types.is_numeric_dtype(datos[atributo]):
        ax.plot(datos.index, datos[atributo], marker="o", linestyle="-", color="#a044b2")
        ax.set_ylabel(atributo, color="white")
        ax.set_title(f'Gráfico de {atributo}', color="white")
        ax.tick_params(axis='x', colors='white')  # Color de las etiquetas del eje X
        ax.tick_params(axis='y', colors='white')  # Color de las etiquetas del eje Y
    else:
        datos[atributo].value_counts().plot(kind='bar', ax=ax, color="#a044b2")
        ax.set_title(f'{atributo}', color="white")
        ax.tick_params(axis='x', colors='white')  # Color de las etiquetas del eje X
        ax.tick_params(axis='y', colors='white')  # Color de las etiquetas del eje Y

    canvas.draw()    # Redibujar el gráfico en el canvas

# Simulación de datos:
df_global = pd.DataFrame({
    "Atributo1": [1, 2, 3, 4, 5],
    "Atributo2": [5, 4, 3, 2, 1],
    "Atributo3": ["a", "b", "a", "a", "b"]
})

# Función para cargar y graficar el archivo convertido automáticamente
def graphing(df_global):
    global datos, indice_actual

    # Verificar que el DataFrame no esté vacío
    if df_global is None or df_global.empty:
        messagebox.showerror("Error", "No hay datos para graficar.")
        return

    datos = df_global     # Almacenar el DataFrame global en la variable 'datos'
    indice_actual = 0     # Reiniciar el índice al primer atributo
    actualizar_grafico()     # Mostrar el primer gráfico

# Función para retroceder al gráfico anterior
def anterior_atributo():
    global indice_actual, datos

    if datos is not None:
        indice_actual = (indice_actual - 1) % len(datos.columns)
        actualizar_grafico()

# Botón para retroceder entre gráficos
boton_anterior = tk.Button(graphic_preview_frame, text="<", command=anterior_atributo,font=("Helvetica Neue", 10), bg="#592d80", fg="#ffffff", relief="flat")
boton_anterior.grid(row=0, column=0, padx=10, pady=10, sticky="e")

# Función para avanzar al siguiente gráfico
def siguiente_atributo():
    global indice_actual, datos

    if datos is not None:
        indice_actual = (indice_actual + 1) % len(datos.columns)
        actualizar_grafico()

# Botón para avanzar entre gráficos
boton_siguiente = tk.Button(graphic_preview_frame, text=">", command=siguiente_atributo, font=("Helvetica Neue", 10), bg="#592d80", fg="#ffffff", relief="flat")
boton_siguiente.grid(row=0, column=2, padx=10, pady=10, sticky="w")

# Cargar la imagen PNG usando Pillow
ruta_imagen = "assets/images/boton_save_download.png"
imagen = Image.open(ruta_imagen).convert("RGBA")
imagen = imagen.resize((40, 40)) 
imagen_tk = ImageTk.PhotoImage(imagen)

def guardar_grafico():
    # Abrir un cuadro de diálogo para seleccionar la ruta y el nombre del archivo
    ruta_archivo = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        title="Guardar Gráfico"
    )
    if ruta_archivo:  # Si se ha seleccionado una ruta
        # Guardar el gráfico como PNG
        fig.savefig(ruta_archivo, format='png', bbox_inches='tight', dpi=300)
        # Mostrar un mensaje de éxito
        messagebox.showinfo("Éxito", "Gráfico guardado con éxito.")

# Botón de guardado de gráfico
boton_save = tk.Button(graphic_preview_frame, image=imagen_tk, bg="#1e1e1e", borderwidth=0, command=guardar_grafico)
boton_save.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

# Mantener la imagen en memoria
boton_save.image = imagen_tk

graphing(df_global)  # Cargar y graficar los datos simulados

root.mainloop()
