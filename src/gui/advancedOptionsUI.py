import tkinter as tk
from tkinter import ttk
from guiLogic import advancedOptionsDEF

def create_advancedOptions_gui(parent_frame, data=None):

    # Limpiar los widgets anteriores en el parent_frame (preVisualice_frame)
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Crear el frame principal dentro del parent_frame
    main_frame = tk.Frame(parent_frame, bg="#2c2c2c")
    main_frame.pack(fill="both", expand=True, padx=0, pady=(0, 20))
    main_frame.grid_columnconfigure(0, weight=0)  # Fijo para la columna izquierda
    main_frame.grid_columnconfigure(1, weight=1)  # Columna derecha más grande
    main_frame.grid_rowconfigure(0, weight=1)

    # Frame de opciones (a la izquierda, tamaño fijo)
    format_options_frame = tk.Frame(main_frame, bg="#2c2c2c", width=400)  # Ancho fijo
    format_options_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    format_options_frame.grid_propagate(False)  # Fijar tamaño sin propagación
    format_options_frame.grid_columnconfigure(0, weight=1)
    format_options_frame.grid_rowconfigure(0, weight=1)
    format_options_frame.grid_rowconfigure(1, weight=1)
    format_options_frame.grid_rowconfigure(2, weight=0)  # Reducimos el espacio de nominal
    format_options_frame.grid_rowconfigure(3, weight=1)  # Nueva fila vacía al final

    # ================== NULL OPTIONS ==================
    null_options_frame = tk.Frame(format_options_frame, bg="#1e1e1e", highlightbackground="#9e64a7", highlightthickness=2)
    null_options_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    null_options_frame.grid_columnconfigure(0, weight=1)
    null_options_frame.grid_columnconfigure(1, weight=3)
    null_options_frame.grid_columnconfigure(2, weight=3)
    null_options_frame.grid_rowconfigure(0, weight=1)
    null_options_frame.grid_rowconfigure(1, weight=1)
    null_options_frame.grid_rowconfigure(2, weight=1)

    # Título en negrita y botón on/off
    null_title_label = tk.Label(null_options_frame, text="Personalize null values", font=("Helvetica Neue", 12, "bold"), bg="#1e1e1e", fg="white")
    null_title_label.grid(row=0, column=1, columnspan=2, padx=10, pady=(10, 10), sticky="w")
    
    null_toggle_var = tk.IntVar(value=0)
    create_modern_toggle_switch(null_options_frame, null_toggle_var)

    # Espacio debajo y label + entry para nulos
    null_label = tk.Label(null_options_frame, text="Set nulls as:", bg="#1e1e1e", fg="white", font=("Helvetica Neue", 10))
    null_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")

    null_entry = tk.Entry(null_options_frame, bg="#333333", fg="white", insertbackground="white", font=("Helvetica Neue", 10))
    null_entry.grid(row=1, column=1, columnspan=2, padx=(10, 20), pady=10, sticky="ew")

    null_information = tk.Label(null_options_frame, bg="#1e1e1e", fg="#ffffff", text="Information about null treatment")
    null_information.grid(row=2, column=0, columnspan=3, padx=20, pady=(10, 10), sticky="ew")

    # ================== DATE OPTIONS ==================
    date_options_frame = tk.Frame(format_options_frame, bg="#1e1e1e", highlightbackground="#9e64a7", highlightthickness=2)
    date_options_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    date_options_frame.grid_columnconfigure(0, weight=1)
    date_options_frame.grid_columnconfigure(1, weight=3)
    date_options_frame.grid_columnconfigure(2, weight=3)
    date_options_frame.grid_rowconfigure(0, weight=1)
    date_options_frame.grid_rowconfigure(1, weight=1)
    date_options_frame.grid_rowconfigure(2, weight=1)

    # Título en negrita y botón on/off para fechas
    date_title_label = tk.Label(date_options_frame, text="Date type treatment", font=("Helvetica Neue", 12, "bold"), bg="#1e1e1e", fg="white")
    date_title_label.grid(row=0, column=0, columnspan=3, padx=(58, 10), pady=(10, 10), sticky="ew")

    date_toggle_var = tk.IntVar(value=0)
    create_modern_toggle_switch(date_options_frame, date_toggle_var)

    # Espacio debajo y combobox para formatos de fecha
    date_label = tk.Label(date_options_frame, text="Set date type as:", bg="#1e1e1e", fg="white", font=("Helvetica Neue", 10))
    date_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")

    date_formats = ["yyyy-MM-dd", "yyyy/MM/dd", "dd-MM-yyyy", "MM/dd/yyyy"]
    date_combobox = ttk.Combobox(date_options_frame, values=date_formats, state="readonly", font=("Helvetica Neue", 10))
    date_combobox.grid(row=1, column=1, columnspan=2, padx=(10, 20), pady=10, sticky="ew")

    date_information = tk.Label(date_options_frame, bg="#1e1e1e", fg="#ffffff", text="Information about date treatment")
    date_information.grid(row=2, column=0, columnspan=3, padx=20, pady=(10, 10), sticky="ew")

    # ================== NOMINAL OPTIONS (Reducido) ==================
    nominal_options_frame = tk.Frame(format_options_frame, bg="#1e1e1e", highlightbackground="#9e64a7", highlightthickness=2)
    nominal_options_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
    nominal_options_frame.grid_columnconfigure(0, weight=1)
    nominal_options_frame.grid_columnconfigure(1, weight=3)
    nominal_options_frame.grid_columnconfigure(2, weight=3)
    nominal_options_frame.grid_rowconfigure(0, weight=1)

    # Título en negrita y botón on/off para strings nominales
    nominal_title_label = tk.Label(nominal_options_frame, text="Set all Strings to Nominal", font=("Helvetica Neue", 12, "bold"), bg="#1e1e1e", fg="white")
    nominal_title_label.grid(row=0, column=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="ew")

    nominal_toggle_var = tk.IntVar(value=0)
    create_modern_toggle_switch(nominal_options_frame, nominal_toggle_var)

    # Solo información (sin la label de "Set strings to nominal")
    nominal_information = tk.Label(nominal_options_frame, bg="#1e1e1e", fg="#ffffff", text="Information about nominal strings")
    nominal_information.grid(row=1, column=0, columnspan=3, padx=20, pady=(10, 10), sticky="ew")

    # Nueva fila vacía al final (para espacio adicional)
    tk.Label(format_options_frame, bg="#2c2c2c").grid(row=3, column=0, pady=20)

    # Frame de datos (a la derecha, ocupará más espacio)
    data_options_frame = tk.Frame(main_frame, bg="#1e1e1e")
    data_options_frame.grid(row=0, column=1, padx=10, pady=0, sticky="nsew")
    data_options_frame.grid_columnconfigure(0, weight=1)
    data_options_frame.grid_rowconfigure(0, weight=1)

    # Contenedor para el Treeview
    tree_container = tk.Frame(data_options_frame, bg="#1e1e1e", width=500, height=300)
    tree_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    tree_container.grid_propagate(False)  # Desactivar propagación para evitar que cambie el tamaño

    # Llamar a la función del archivo attributeEditor.py para crear el Treeview
    advancedOptionsDEF.load_attributes_to_table(tree_container, data)  # Pasa el contenedor

    return data_options_frame








# Función para crear un interruptor on/off moderno (similar al usado en converter UI)
def create_modern_toggle_switch(parent, toggle_var):
    switch_canvas = tk.Canvas(parent, width=50, height=25, bg="#1e1e1e", highlightthickness=0)
    switch_canvas.grid(row=0, column=0, padx=(20, 5), pady=10, sticky="ew")

    # Crear el fondo del interruptor
    switch_bg = switch_canvas.create_rectangle(0, 0, 50, 25, outline="#cccccc", fill="#cccccc", width=2)
    
    # Crear el círculo del interruptor
    switch_circle = switch_canvas.create_oval(3, 3, 23, 23, outline="#333333", fill="#333333")

    # Función para cambiar el estado del interruptor
    def toggle_switch():
        if toggle_var.get() == 0:
            switch_canvas.move(switch_circle, 25, 0)
            switch_canvas.itemconfig(switch_bg, fill="#4caf50")
            toggle_var.set(1)
        else:
            switch_canvas.move(switch_circle, -25, 0)
            switch_canvas.itemconfig(switch_bg, fill="#cccccc")
            toggle_var.set(0)

    # Asignar el evento de clic al interruptor
    switch_canvas.bind("<Button-1>", lambda event: toggle_switch())
