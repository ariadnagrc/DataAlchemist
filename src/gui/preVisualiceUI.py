import tkinter as tk
from tkinter import ttk
from guiLogic import preVisualiceDEF

rows_loaded = 0

def create_preVisualice_gui(parent_frame, data=None, rows_per_load=10):
    global rows_loaded  

    # Limpiar los widgets anteriores en el parent_frame (preVisualice_frame)
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Crear el frame principal para el Treeview
    main_frame = tk.Frame(parent_frame, bg="#2c2c2c")
    main_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))

    # Configurar grid para mantener un tamaño fijo
    main_frame.grid_rowconfigure(0, weight=1, minsize=300)
    main_frame.grid_rowconfigure(1, weight=0)
    main_frame.grid_columnconfigure(0, weight=1, minsize=500)
    main_frame.grid_columnconfigure(1, weight=0, minsize=170)

    # Estilo oscuro para el Treeview y las scrollbars
    style = ttk.Style()
    style.theme_use('clam')

    # Configurar estilo oscuro para el Treeview
    style.configure("Treeview",
                    background="#1e1e1e",
                    foreground="white",
                    fieldbackground="#1e1e1e",
                    rowheight=25,
                    font=("Helvetica Neue", 10))
    style.configure("Treeview.Heading", background="#333333", foreground="white", font=("Helvetica Neue", 10, "bold"))

    # Configurar estilo oscuro para las scrollbars
    style.configure("TScrollbar", troughcolor="#1e1e1e", background="#3b3b3b", gripcount=0, arrowcolor="#ffffff")
    style.map("TScrollbar", background=[('active', '#5c5c5c')])

    # Contenedor para el Treeview con un tamaño fijo
    tree_container = tk.Frame(main_frame, bg="#1e1e1e", width=500, height=300)  # Fijar tamaño
    tree_container.grid(row=0, column=0, padx=(0, 0), pady=0, sticky="nsew")
    tree_container.grid_propagate(False)  # Desactivar propagación para evitar que cambie el tamaño

    # Crear el Treeview con scrollbars, manteniendo el margen y el espacio
    tree = ttk.Treeview(tree_container, show='headings', height=8, style="Treeview", selectmode="browse")
    scrollbar_vertical = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview, style="TScrollbar")
    scrollbar_horizontal = ttk.Scrollbar(tree_container, orient="horizontal", command=tree.xview, style="TScrollbar")
    tree.configure(yscroll=scrollbar_vertical.set, xscroll=scrollbar_horizontal.set)

    # Vincular los eventos de clic para edición y eliminación de columnas
    tree.bind("<Double-1>", lambda event: preVisualiceDEF.edit_cell(tree, event))  # Doble clic para editar la celda
    tree.bind("<Button-3>", lambda event: preVisualiceDEF.delete_column(tree, event))  # Clic derecho para eliminar columna

    # Añadir scrollbars al Treeview
    scrollbar_vertical.pack(side="right", fill="y", padx=(0, 40), pady=(40, 40))  # Espacio alrededor del scrollbar vertical
    scrollbar_horizontal.pack(side="bottom", fill="x", padx=(40, 0), pady=(0, 40))  # Espacio alrededor del scrollbar horizontal
    tree.pack(side="left", fill="both", expand=True, padx=(40, 0), pady=(40, 0))  # Espacio alrededor del Treeview

    # Configurar las columnas del Treeview con los datos
    if data is not None:
        tree["columns"] = list(data.columns)
        for col in tree["columns"]:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=100, minwidth=100, stretch=tk.NO, anchor="center")

        # Mostrar los primeros registros (o la cantidad indicada por rows_per_load)
        rows_loaded = 0  # Resetear cuando se cargue un nuevo archivo
        preVisualiceDEF.load_rows(tree, data, rows_per_load)

    # Contenedor para el more_data_frame, que ocupará ambas filas
    edit_data_frame = tk.Frame(main_frame, bg="#2c2c2c", width=170, height=300)  # Ajustar tamaño de altura
    edit_data_frame.grid(row=0, column=1, rowspan=2, padx=(10, 0), pady=(0, 60), sticky="nsew")  # Ocupar dos filas (Treeview + botones)

    # Configurar el número de filas y columnas para que los botones se expandan por igual
    for i in range(5):
        edit_data_frame.grid_rowconfigure(i, weight=1)
    edit_data_frame.grid_columnconfigure(0, weight=1)

    # Botón para eliminar una fila
    delete_row_button = tk.Button(edit_data_frame, text="Delete Row", command=lambda: preVisualiceDEF.toggle_delete_row_mode(tree, delete_row_button, edit_cell_button, delete_column_button, add_row_button), fg="#ffffff", bg="#1e1e1e", relief="flat", height=2)
    delete_row_button.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

    # Botón para eliminar una columna
    delete_column_button = tk.Button(edit_data_frame, text="Delete Column", command=lambda: preVisualiceDEF.toggle_delete_column_mode(tree, delete_column_button, edit_cell_button, add_row_button, delete_row_button), fg="#ffffff", bg="#1e1e1e", relief="flat", height=2)
    delete_column_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

    # Botón para editar la celda seleccionada
    edit_cell_button = tk.Button(edit_data_frame, text="Edit Cell", command=lambda: preVisualiceDEF.toggle_edit_mode(tree, edit_cell_button, delete_column_button, add_row_button, delete_row_button), fg="#ffffff", bg="#1e1e1e", relief="flat", height=2)
    edit_cell_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    # Botón para añadir una fila debajo de la seleccionada
    add_row_button = tk.Button(edit_data_frame, text="Add Row Below", command=lambda: preVisualiceDEF.toggle_add_row_mode(tree, add_row_button, edit_cell_button, delete_column_button, delete_row_button), fg="#ffffff", bg="#1e1e1e", relief="flat", height=2)
    add_row_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

    # Botón para deshacer acción (Undo)
    undo_button = tk.Button(edit_data_frame, text="Undo", command=lambda: preVisualiceDEF.undo_last_action(tree), fg="#ffffff", bg="#1e1e1e", relief="flat", height=2)
    undo_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    # Sección para botones debajo del Treeview, solo ocupará el ancho del Treeview
    more_data_frame = tk.Frame(main_frame, bg="#1e1e1e", width=500, height=50)
    more_data_frame.grid(row=1, column=0, padx=0, pady=(0, 0), sticky="ew")  # Alineado solo al Treeview

    # Configurar las columnas para los botones en fila única (horizontal)
    more_data_frame.grid_columnconfigure(0, weight=1)
    more_data_frame.grid_columnconfigure(1, weight=1)
    more_data_frame.grid_columnconfigure(2, weight=1)
    more_data_frame.grid_columnconfigure(3, weight=1)

    # Botón para cargar 50 filas adicionales
    fifty_more_button = tk.Button(more_data_frame, text="Show 50 more rows", command=lambda: preVisualiceDEF.load_rows(tree, data, 50), fg="#ffffff", bg="#952184", relief="flat")
    fifty_more_button.grid(row=0, column=0, padx=(40, 10), pady=10, sticky="ew")

    # Botón para cargar 500 filas adicionales
    fivehundred_more_button = tk.Button(more_data_frame, text="Show 500 more rows", command=lambda: preVisualiceDEF.load_rows(tree, data, 500), fg="#ffffff", bg="#952184", relief="flat")
    fivehundred_more_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    # Botón para cargar todos los registros restantes
    all_more_button = tk.Button(more_data_frame, text="Show all rows", command=lambda: preVisualiceDEF.load_rows(tree, data, len(data) - rows_loaded), fg="#ffffff", bg="#952184", relief="flat")
    all_more_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    # Botón para cargar las últimas 50 filas
    last_rows_button = tk.Button(more_data_frame, text="Show last rows", command=lambda: preVisualiceDEF.load_last_rows(tree, data, 50), fg="#ffffff", bg="#952184", relief="flat")
    last_rows_button.grid(row=0, column=3, padx=(10, 40), pady=10, sticky="ew")

    return tree  # Devolver el Treeview creado
