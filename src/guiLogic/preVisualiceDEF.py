import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Entry

#################################################################################
##### FUNCIONES PARA CARGAR Y VISUALIZAR ARCHIVOS ###############################
#################################################################################

rows_loaded = 0

# Función para previsualizar el archivo #########################################
def load_preview(format_combobox, file_path, tree):
    try:
        # Detectar el tipo de archivo
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.csv':
            df = pd.read_csv(file_path, encoding='ISO-8859-1', header='infer')
            format_combobox.set("ARFF")  # Seleccionar ARFF por defecto
            format_combobox['values'] = ["ARFF"]  
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
            format_combobox['values'] = ["CSV", "ARFF"]  # Permitir ambas conversiones
        else:
            raise Exception("Unsupported file format.")

        tree.delete(*tree.get_children())  # Limpiar la tabla

        # Configurar las columnas del Treeview
        tree["columns"] = list(df.columns)
        for col in tree["columns"]:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=100, minwidth=100, stretch=tk.NO, anchor="center")

        # Insertar filas en la previsualización
        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        tree["show"] = "headings"

    except Exception as e:
        messagebox.showerror("Error", f"Error loading preview: {str(e)}")

# Función para cargar más registros en el Treeview ##############################
def load_rows(tree, data, rows_per_load):
    global rows_loaded
    max_rows = len(data)

    # Insertar los registros adicionales
    for index, row in data.iloc[rows_loaded:rows_loaded+rows_per_load].iterrows():
        tree.insert("", "end", values=list(row))
    
    # Actualizar cuántos registros se han cargado
    rows_loaded += rows_per_load

    # No cargar más si ya llegamos al final de los datos
    if rows_loaded >= max_rows:
        rows_loaded = max_rows

# Función para cargar las últimas filas del archivo #############################
def load_last_rows(tree, data, num_rows):
    tree.delete(*tree.get_children())      # Limpiar el Treeview actual
    last_rows = data.tail(num_rows)        # Obtener las últimas num_rows filas del DataFrame
    
    for _, row in last_rows.iterrows():    # Insertar las filas en el Treeview
        tree.insert("", "end", values=list(row))

##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ###

#################################################################################
##### FUNCIONES PARA ELIMINAR DATOS, COLUMNAS Y FILAS ###########################
#################################################################################

# Función de botón del delete_row_mode
def toggle_delete_row_mode(tree, delete_button, edit_button, delete_column_button, add_row_button):
    global delete_mode, edit_mode
    delete_mode = not delete_mode

    # Desactivar el resto de botones si está pulsado el delete row
    if delete_mode:
        delete_button.config(bg="#952184", text="Delete row") 
        tree.bind("<ButtonRelease-1>", lambda event: delete_row(tree, event))  
        edit_button.config(state="disabled") 
        delete_column_button.config(state="disabled")  
        add_row_button.config(state="disabled")
    # Reactivar botones al dejar de pulsar el delete row
    else:
        delete_button.config(bg="#1e1e1e", text="Delete row") 
        tree.unbind("<ButtonRelease-1>") 
        edit_button.config(state="normal")  
        delete_column_button.config(state="normal")  
        add_row_button.config(state="normal")  

# 
def delete_row(tree, event):
    selected_item = tree.selection()
    if selected_item:
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this row?")
        if confirm:
            # Guardar la fila eliminada antes de eliminarla
            item_data = {
                "iid": selected_item[0],
                "index": tree.index(selected_item[0]),
                "values": tree.item(selected_item[0], "values")
            }
            register_action("delete_row", tree, item=item_data)
            tree.delete(selected_item)  # Eliminar la fila seleccionada

#
delete_mode = False  # Variable de estado para el modo de eliminación

def toggle_delete_column_mode(tree, delete_column_button, edit_button, add_row_button, delete_row_button):
    global delete_mode, edit_mode, add_row_mode
    delete_mode = not delete_mode

    if delete_mode:
        delete_column_button.config(bg="#952184", text="Delete column")  # Cambiar el color y texto del botón
        tree.bind("<Button-1>", lambda event: delete_column(tree, event))  # Vincular clic izquierdo para eliminar
        edit_button.config(state="disabled")  # Desactivar el botón de edición mientras se elimina
        add_row_button.config(state="disabled")  # Desactivar el botón de añadir fila mientras se elimina
        delete_row_button.config(state="disabled")  # Desactivar el botón de eliminación de filas
    else:
        delete_column_button.config(bg="#1e1e1e", text="Delete column")  # Restaurar el color y texto original del botón
        tree.unbind("<Button-1>")  # Desvincular el clic izquierdo para eliminar
        edit_button.config(state="normal")  # Reactivar el botón de edición
        add_row_button.config(state="normal")  # Reactivar el botón de añadir fila
        delete_row_button.config(state="normal")  # Reactivar el botón de eliminación de filas

    # Si el modo de eliminación está activado, desactivar otros modos
    if delete_mode and (edit_mode or add_row_mode):
        edit_mode = False
        add_row_mode = False
        edit_button.config(state="normal")  # Asegurarse de que se reactiva el botón de edición
        add_row_button.config(state="normal")  # Reactivar el botón de añadir fila
        delete_row_button.config(state="normal")  # Reactivar el botón de eliminación de filas

# Función para eliminar una columna y registrar la acción
def delete_column(tree, event):
    column_id = tree.identify_column(event.x)
    if column_id:
        col_num = int(column_id.replace('#', '')) - 1  # Obtener el índice de la columna
        col_name = tree.heading(column_id)["text"]  # Obtener el nombre de la columna

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the column '{col_name}'?")
        if confirm:
            columns = list(tree["columns"])
            if 0 <= col_num < len(columns):
                deleted_column = {
                    "col_name": col_name,
                    "values": {}
                }
                for item in tree.get_children():
                    deleted_column["values"][item] = tree.item(item, "values")[col_num]

                # Registrar la acción antes de eliminar
                register_action("delete_column", tree, col_num=col_num, item=deleted_column)

                # Eliminar la columna
                del columns[col_num]
                tree["columns"] = columns

                # Eliminar los valores correspondientes en cada fila
                for item in tree.get_children():
                    values = list(tree.item(item, "values"))
                    if col_num < len(values):
                        del values[col_num]
                    tree.item(item, values=values)

##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ###

#################################################################################
##### FUNCIONES DE EDICIÓN Y AGREGACIÓN #########################################
#################################################################################

edit_mode = False  # Variable global para el estado de edición

#
def toggle_edit_mode(tree, edit_button, delete_column_button, add_row_button, delete_row_button):
    global edit_mode, delete_mode
    edit_mode = not edit_mode

    if edit_mode:
        edit_button.config(bg="#952184", text="Edit cell")  # Cambiar color y texto al activarse el modo edición
        tree.bind("<Double-1>", lambda event: edit_cell(tree, event))  # Permitir edición con doble clic
        delete_column_button.config(state="disabled")
        delete_row_button.config(state="disabled")  
        add_row_button.config(state="disabled")
    else:
        edit_button.config(bg="#1e1e1e", text="Edit cell")  # Restaurar botón a su estado original
        tree.unbind("<Double-1>")  # Desvincular el doble clic para edición
        delete_column_button.config(state="normal")  # Reactivar el botón de eliminación de columnas
        delete_row_button.config(state="normal")  # Reactivar el botón de eliminación de filas
        add_row_button.config(state="normal")  # Reactivar el botón de añadir fila

    # Si el modo de edición está activado, desactivar el modo de eliminación
    if edit_mode and delete_mode:
        toggle_delete_column_mode(tree, delete_column_button, edit_button, add_row_button)  # Desactivar el modo de eliminación si está activado

# Función para editar una celda y registrar la acción
def edit_cell(tree, event):
    row_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)

    if row_id and column_id:
        col_num = int(column_id.replace('#', '')) - 1  # Obtener el índice de la columna
        current_value = tree.item(row_id)["values"][col_num]  # Obtener el valor actual de la celda

        # Crear un cuadro de diálogo para permitir la edición
        new_value = simpledialog.askstring("Edit Cell", f"Edit value for column {col_num+1}:", initialvalue=current_value)
        
        if new_value is not None:
            # Registrar la acción antes de editar
            register_action("edit_cell", tree, item=row_id, col_num=col_num, values=current_value)

            # Actualizar la celda con el nuevo valor
            values = list(tree.item(row_id, 'values'))
            values[col_num] = new_value
            tree.item(row_id, values=values)

add_row_mode = False  

#
def toggle_add_row_mode(tree, add_row_button, edit_button, delete_column_button, delete_row_button):
    global add_row_mode, edit_mode, delete_mode
    add_row_mode = not add_row_mode

    if add_row_mode:
        add_row_button.config(bg="#952184", text="Add row below")  # Cambiar color y texto al activarse el modo
        tree.bind("<Button-1>", lambda event: add_row_below_selected(tree, event))  # Vincular clic izquierdo para seleccionar la fila donde añadir
        edit_button.config(state="disabled")  # Desactivar el botón de edición mientras se añade una fila
        delete_column_button.config(state="disabled")  # Desactivar el botón de eliminación de columnas
        delete_row_button.config(state="disabled")  # Desactivar el botón de eliminación de filas
    else:
        add_row_button.config(bg="#1e1e1e", text="Add row below")  # Restaurar el color y texto del botón
        tree.unbind("<Button-1>")  # Desvincular el clic para añadir filas
        edit_button.config(state="normal")  # Reactivar el botón de edición
        delete_column_button.config(state="normal")  # Reactivar el botón de eliminación de columnas
        delete_row_button.config(state="normal")  # Reactivar el botón de eliminación de filas

def add_row_below_selected(tree, event):
    # Obtener la fila seleccionada
    row_id = tree.identify_row(event.y)

    if row_id:
        # Crear ventana emergente para introducir los datos
        new_row_window = Toplevel()
        new_row_window.title("Add New Row")

        # Obtener las columnas del treeview
        columns = tree["columns"]
        
        # Crear una lista para almacenar los widgets de entrada
        entry_widgets = []

        # Crear un Entry para cada columna
        for i, col in enumerate(columns):
            label = tk.Label(new_row_window, text=f"{col}:", font=("Helvetica Neue", 10))
            label.grid(row=i, column=0, padx=10, pady=5)

            entry = Entry(new_row_window, font=("Helvetica Neue", 10))
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry_widgets.append(entry)

        # Función que añade la nueva fila con los valores ingresados
        def confirm_new_row():
            new_row_values = [entry.get() for entry in entry_widgets]

            # Verificar si todos los campos están completos
            if all(new_row_values):  # Solo si todos los campos están completos
                # Obtener la posición de la fila seleccionada
                selected_index = tree.index(row_id)

                # Insertar la nueva fila debajo de la fila seleccionada
                tree.insert("", selected_index + 1, values=new_row_values)

                # Registrar la acción
                register_action("add_row", tree, item=tree.get_children()[-1])  # Registrar la última fila añadida
                
                # Cerrar la ventana emergente solo si todo está completo
                new_row_window.destroy()
            else:
                # Mostrar advertencia sin cerrar la ventana
                messagebox.showwarning("Incomplete Data", "Please fill in all fields before confirming.")
                new_row_window.lift()  # Asegurarse de que la ventana quede al frente

        # Botón para confirmar la adición de la nueva fila
        confirm_button = tk.Button(new_row_window, text="Add Row", command=confirm_new_row, bg="#4caf50", fg="#ffffff")
        confirm_button.grid(row=len(columns), column=0, columnspan=2, pady=10)

        # Evitar que se cierre la ventana accidentalmente con "X" si los datos no están completos
        def on_closing():
            if messagebox.askokcancel("Quit", "Are you sure you want to quit without saving?"):
                new_row_window.destroy()

        new_row_window.protocol("WM_DELETE_WINDOW", on_closing)

    else:
        messagebox.showinfo("No Row Selected", "Please select a row in the table to add a new row below.")


##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ###

#################################################################################
##### FUNCIONES DE DESHACER #####################################################
#################################################################################

action_history = []  # Historial de acciones para deshacer

# Función para deshacer la última acción
def undo_last_action(tree):
    if not action_history:
        messagebox.showinfo("Undo", "No actions to undo.")
        return

    last_action = action_history.pop()  # Obtener la última acción

    if last_action["type"] == "delete_row":
        # Restaurar la fila eliminada
        tree.insert("", last_action["item"]["index"], iid=last_action["item"]["iid"], values=last_action["item"]["values"])

    elif last_action["type"] == "delete_column":
        col_num = last_action["col_num"]
        columns = list(tree["columns"])
        columns.insert(col_num, last_action["item"]["col_name"])
        tree["columns"] = columns

        # Restaurar los valores de las filas en esa columna
        for item in tree.get_children():
            values = list(tree.item(item, "values"))
            values.insert(col_num, last_action["item"]["values"][item])
            tree.item(item, values=values)

    elif last_action["type"] == "edit_cell":
        # Restaurar el valor original de la celda
        item = last_action["item"]
        values = list(tree.item(item, "values"))
        values[last_action["col_num"]] = last_action["values"]  # Restaurar el valor original
        tree.item(item, values=values)

    elif last_action["type"] == "add_row":
        # Eliminar la fila añadida
        tree.delete(last_action["item"])  # Eliminar la fila recientemente añadida

    messagebox.showinfo("Undo", "Last action undone successfully.")

# Función para registrar una acción en el historial
def register_action(action_type, tree, item=None, col_num=None, values=None):
    action = {
        "type": action_type,  # Puede ser 'add_row', 'delete_row', 'edit_cell', 'delete_column'
        "item": item,         # Fila o columna afectada
        "col_num": col_num,   # Índice de columna (si aplica)
        "values": values      # Valores originales (para deshacer ediciones o eliminaciones)
    }
    action_history.append(action)
