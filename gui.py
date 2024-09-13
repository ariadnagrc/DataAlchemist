import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from dataAlchemist import convert_file
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

def choose_save_location():
    save_directory = filedialog.askdirectory()
    if save_directory:
        save_path_label.config(text=f"Guardar en: {save_directory}")
        convert_button.config(state="normal", bg="#007bff")

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
    
    if not save_directory:
        messagebox.showerror("Error", "Selecciona una ruta para guardar el archivo.")
        return
    
    try:
        converted_file_path = convert_file(file_path, format_selected)
        messagebox.showinfo("Éxito", f"Archivo convertido a {format_selected}: {converted_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error al convertir: {str(e)}")

# Crear ventana principal
root = TkinterDnD.Tk()
root.title("Data Alchemist")
root.geometry("800x600")
root.configure(bg="#2c2c2c")

# Título
title_label = tk.Label(root, text="Data Alchemist", font=("Helvetica Neue", 24, "bold"), bg="#2c2c2c", fg="white")
title_label.pack(pady=(45, 20))

# Marco principal
main_frame = tk.Frame(root, bg="#2c2c2c")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Crear dos frames: uno para selección de archivo y otro para vista previa
file_select_frame = tk.Frame(main_frame, bg="#1e1e1e", width=250, height=300)
file_select_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
file_select_frame.pack_propagate(False)

file_select_title = tk.Label(file_select_frame, text="Selecciona o arrastra un archivo", font=("Helvetica Neue", 12, "bold"), bg="#1e1e1e", fg="white")
file_select_title.pack(pady=(30, 10))

drag_drop_frame = tk.Frame(file_select_frame, bg="#1e1e1e", highlightbackground="#5c5c5c", highlightthickness=2, highlightcolor="#5c5c5c")
drag_drop_frame.pack(fill="both", expand=True, padx=20, pady=20)

file_label = tk.Label(drag_drop_frame, text="No se ha seleccionado ningún archivo", wraplength=150, bg="#1e1e1e", fg="white", font=("Helvetica Neue", 10))
file_label.pack(expand=True, pady=(20, 0))

select_button = tk.Button(drag_drop_frame, text="Seleccionar archivo", command=open_file, font=("Helvetica Neue", 10), bg="#592d80", fg="#ffffff", relief="flat")
select_button.pack(side="bottom", pady=10)

file_select_frame.drop_target_register(DND_FILES)
file_select_frame.dnd_bind('<<Drop>>', drop)

# Crear el frame para la vista previa
preview_frame = tk.Frame(main_frame, bg="#1e1e1e", width=250, height=300)
preview_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
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
right_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

# Añadir un marco superior para el espaciado
top_padding_frame = tk.Frame(right_frame, bg="#1e1e1e", height=60)  
top_padding_frame.pack()

right_label = tk.Label(right_frame, text="Selecciona el tipo de conversión", font=("Helvetica Neue", 12, "bold"), bg="#1e1e1e", fg="white")
right_label.pack(pady=(40, 20))  # Aumentar el padding superior e inferior

format_combobox = ttk.Combobox(right_frame, values=["CSV", "ARFF"], state="readonly", font=("Helvetica Neue", 10))
format_combobox.pack(pady=(0, 20))  # Dejar más espacio con la opción inferior

# Crear un frame para la selección de ruta
save_frame = tk.Frame(right_frame, bg="#1e1e1e", highlightbackground="#5c5c5c", highlightthickness=1)
save_frame.pack(pady=(20, 20), padx=10, fill="x")

# Etiqueta y botón para seleccionar la ubicación de guardado
save_path_label = tk.Label(save_frame, text="Guardar en: ", bg="#1e1e1e", fg="white", font=("Helvetica Neue", 10))
save_path_label.pack(pady=(10, 5))

select_save_button = tk.Button(save_frame, text="Seleccionar ruta de guardado", command=choose_save_location, font=("Helvetica Neue", 10), bg="#592d80", fg="#ffffff", relief="flat")
select_save_button.pack(pady=(0, 10))

convert_button = tk.Button(right_frame, text="Convertir archivo", command=convert, font=("Helvetica Neue", 10), bg="#a5a5a5", fg="#ffffff", relief="flat", state="disabled")
convert_button.pack(pady=40)  # Más espacio debajo

# Configurar columnas y filas del marco principal
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=2)
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=2)

root.mainloop()
