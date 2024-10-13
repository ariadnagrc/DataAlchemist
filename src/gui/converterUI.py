import sys
import os
from tkinter import PhotoImage, messagebox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import filedialog, ttk
from guiLogic import converterDEF
from guiLogic.converterDEF import handle_file_selection
from tkinterdnd2 import DND_FILES

def create_converter_gui(parent_frame, preVisualice_frame, advanced_table_frame):
    # Crear el frame principal dentro del parent_frame
    main_frame = tk.Frame(parent_frame, bg="#2c2c2c")
    main_frame.pack(fill="both", expand=True, padx=0, pady=(0, 20))
    main_frame.grid_rowconfigure(0, weight=1) 
    main_frame.grid_columnconfigure(0, weight=1)  
    main_frame.grid_columnconfigure(1, weight=2)

    # Frame para seleccionar archivo
    file_select_frame = tk.Frame(main_frame, bg="#1e1e1e", width=300, height=250)
    file_select_frame.grid(row=0, column=0, padx=10, pady=0, sticky="nsew")
    file_select_frame.pack_propagate(False)

    file_select_title = tk.Label(file_select_frame, text="Select or drag a file", font=("Helvetica Neue", 18, "bold"), bg="#1e1e1e", fg="white")
    file_select_title.pack(pady=(30, 10))

    # Frame (cuadro) para arrastrar y soltar archivos
    drag_drop_frame = tk.Frame(file_select_frame, bg="#1e1e1e", highlightbackground="#9e64a7", highlightthickness=2)
    drag_drop_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Label para mostrar el archivo seleccionado
    file_label = tk.Label(drag_drop_frame, text="No file selected", wraplength=250, bg="#1e1e1e", fg="white", font=("Helvetica Neue", 10), anchor="center")
    file_label.pack(expand=True, pady=(10, 0), fill="x")

    # Botón para seleccionar archivo
    select_button = tk.Button(drag_drop_frame, text="Select file", padx=20, pady=5, width=10, command=lambda: handle_file_selection(preVisualice_frame, file_label, name_entry, advanced_table_frame), font=("Helvetica Neue", 12), bg="#592d80", fg="#ffffff", relief="flat", cursor="hand2")
    select_button.pack(side="bottom", pady=(0, 20))

    # Permitir arrastrar y soltar archivos en el file_select_frame
    file_select_frame.drop_target_register(DND_FILES)
    file_select_frame.dnd_bind('<<Drop>>', lambda event: converterDEF.drop(event, file_label, name_entry))

    # Frame para convertir archivos
    file_convert_frame = tk.Frame(main_frame, bg="#1e1e1e")
    file_convert_frame.grid(row=0, column=1, padx=10, pady=0, sticky="nsew")
    
    # Centramos las columnas del file_convert_frame
    file_convert_frame.grid_columnconfigure(0, weight=1)
    file_convert_frame.grid_columnconfigure(1, weight=0)
    file_convert_frame.grid_columnconfigure(2, weight=1)

    # Label "Select the conversion type" (centrado)
    file_convert_label = tk.Label(file_convert_frame, text="Select the conversion type", font=("Helvetica Neue", 18, "bold"), bg="#1e1e1e", fg="white")
    file_convert_label.grid(row=0, column=0, columnspan=3, pady=(115, 5), sticky="ew")

    # Combobox para selección de tipo de conversión (centrado)
    format_combobox = ttk.Combobox(file_convert_frame, values=["CSV", "ARFF"], state="readonly", font=("Helvetica Neue", 10))
    format_combobox.grid(row=1, column=1, pady=10, padx=20, sticky="ew")
    format_combobox.bind("<<ComboboxSelected>>", lambda event: converterDEF.on_format_select(event, format_combobox))

    # Frame con borde morado para la selección de ruta de guardado
    save_frame = tk.Frame(file_convert_frame, bg="#1e1e1e", highlightbackground="#9e64a7", highlightthickness=2)
    save_frame.grid(row=2, column=0, columnspan=3, pady=40, padx=20, sticky="ew")

    # Etiqueta "Save in:" (alineado a la izquierda)
    save_in_label = tk.Label(save_frame, text="Save in:", font=("Helvetica Neue", 10), bg="#1e1e1e", fg="white")
    save_in_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="w")

    # Variable para la ruta seleccionada
    save_path_var = tk.StringVar()

    # Botón "Browse" cuadrado sin texto, con un ícono de carpeta
    folder_icon = PhotoImage(file=os.path.join(os.path.dirname(__file__), '..','..', 'assets','icon', 'folder_icon.png'))
    browse_button = tk.Button(save_frame, image=folder_icon, command=lambda: converterDEF.select_path(save_path_var), bg="#1e1e1e", relief="flat", cursor="hand2")
    browse_button.grid(row=0, column=2, padx=(0, 30), sticky="e")
    browse_button.image = folder_icon

    # Label que muestra la ruta seleccionada (centrado en el frame)
    selected_path_label = tk.Label(save_frame, textvariable=save_path_var, font=("Helvetica Neue", 10), bg="#1e1e1e", fg="white")
    selected_path_label.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="w")

    # Configurar el frame para que la ruta se expanda
    save_frame.grid_columnconfigure(2, weight=1)

    # Etiqueta "As:" para el nombre del archivo (alineado a la izquierda)
    as_label = tk.Label(save_frame, text="As:", font=("Helvetica Neue", 10), bg="#1e1e1e", fg="white")
    as_label.grid(row=1, column=0, padx=(30, 0), pady=10, sticky="w")

    # Entry para el nombre de archivo (con el nombre del archivo seleccionado)
    name_entry = tk.Entry(save_frame, font=("Helvetica Neue", 10), bg="#333333", fg="white", insertbackground="white")
    name_entry.grid(row=1, column=1, columnspan=2, padx=(0, 30), pady=10, sticky="ew")

    # Botón "Convert file" para realizar la conversión (centrado)
    convert_button = tk.Button(file_convert_frame, text="Convert file", pady=5, font=("Helvetica Neue", 12), bg="#592d80", fg="white", relief="flat", command=lambda: converterDEF.validate_and_convert(name_entry), cursor="hand2")
    convert_button.grid(row=3, column=1, pady=20, padx=20, sticky="ew")

    # Retorno del frame y otros elementos
    return folder_icon  # Para que el ícono no se pierda en el garbage collector
