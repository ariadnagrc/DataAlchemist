import tkinter as tk
from tkinter import ttk
import pandas as pd

def load_attributes_to_table(tree_container, data):
    # Limpiar el contenido actual del frame de la tabla
    for widget in tree_container.winfo_children():
        widget.destroy()

    # Fijar el tamaño del contenedor del Treeview
    tree_container.config(width=500, height=300)
    tree_container.grid_propagate(False)  # Desactiva la propagación del tamaño del contenedor

    # Crear el Treeview para mostrar los atributos y sus tipos de datos
    tree = ttk.Treeview(tree_container, columns=("Attribute", "Type"), show="headings", height=10)
    tree.heading("Attribute", text="Attribute")
    tree.heading("Type", text="Type")
    tree.column("Attribute", width=200, anchor="center")
    tree.column("Type", width=150, anchor="center")

    # Si hay datos, cargar los atributos y tipos de datos
    if data is not None:
        for col in data.columns:
            col_type = pd.api.types.infer_dtype(data[col])
            tree.insert("", "end", values=(col, col_type))

    # Añadir scrollbars
    scrollbar_vertical = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar_vertical.set)

    # Usamos grid en lugar de pack
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar_vertical.grid(row=0, column=1, sticky="ns")

    # Configurar la expansión del Treeview
    tree_container.grid_columnconfigure(0, weight=1)
    tree_container.grid_rowconfigure(0, weight=1)

    # Hacer que el tipo de dato sea editable
    tree.bind("<Double-1>", lambda event: edit_type(tree, event, data))


# Función para editar el tipo de dato (con ventana emergente)
def edit_type(tree, event, data):
    # Obtener el ítem seleccionado
    selected_item = tree.selection()
    if selected_item:
        # Obtener los valores de la fila seleccionada
        item_values = tree.item(selected_item, 'values')
        attribute = item_values[0]  # Nombre del atributo
        current_type = item_values[1]  # Tipo actual

        # Mostrar una ventana emergente para editar el tipo
        top = tk.Toplevel(tree)
        top.title(f"Edit Type for {attribute}")
        top.geometry("300x100")

        label = tk.Label(top, text=f"Current type: {current_type}")
        label.pack(pady=10)

        new_type_var = tk.StringVar(top)
        new_type_entry = ttk.Combobox(top, textvariable=new_type_var)
        new_type_entry['values'] = ["string", "int", "float", "datetime"]  # Tipos de datos comunes
        new_type_entry.pack(pady=10)

        # Guardar el nuevo tipo de dato
        def save_new_type():
            new_type = new_type_var.get()
            if new_type:
                # Actualizar la tabla con el nuevo tipo
                tree.item(selected_item, values=(attribute, new_type))
            top.destroy()

        save_button = tk.Button(top, text="Save", command=save_new_type)
        save_button.pack(pady=5)

