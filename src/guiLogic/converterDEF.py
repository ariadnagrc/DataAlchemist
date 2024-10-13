import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tkinter import filedialog, messagebox, ttk, Canvas, END
import pandas as pd
from gui.preVisualiceUI import create_preVisualice_gui
from .preVisualiceDEF import load_preview
from gui.advancedOptionsUI import create_advancedOptions_gui

# Función para abrir archivo y actualizar el Treeview
def open_file(file_label, name_entry):
    # Abrir el diálogo de selección de archivo
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel and CSV files", "*.xlsx;*.xls;*.csv"), 
                   ("Excel files", "*.xlsx;*.xls"), 
                   ("CSV files", "*.csv")])
    
    if file_path:
        # Actualizar la etiqueta con la ruta del archivo seleccionado
        file_label.config(text=file_path)

        # Extraer el nombre del archivo y actualizar el cuadro de texto name_entry
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        name_entry.delete(0, END)  # Borrar cualquier contenido previo en el Entry
        name_entry.insert(0, file_name)  # Insertar el nombre del archivo en el Entry

        # Cargar el archivo en un DataFrame
        file_extension = file_path.split('.')[-1].lower()
        try:
            if file_extension == 'csv':
                data = pd.read_csv(file_path)
            elif file_extension in ['xls', 'xlsx']:
                data = pd.read_excel(file_path)
            else:
                raise ValueError("Formato de archivo no soportado.")
            
            # Devolver los datos cargados
            return data
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
            return None
    else:
        messagebox.showwarning("Warning", "No se seleccionó ningún archivo.")
        return None

# Función para seleccionar la ruta
def select_path(save_path_var):
    selected_path = filedialog.askdirectory()
    if selected_path:
        save_path_var.set(selected_path)

# Function to drag and drop files
def drop(event, file_label):
    file_path = event.data
    file_label.config(text=file_path)
    load_preview(file_path)

# Function to get the selected value from the combobox
def on_format_select(event, format_combobox):
    format_selected = format_combobox.get()

# Función para manejar la selección de archivo
from guiLogic import advancedOptionsDEF

# Función para manejar la selección de archivo
def handle_file_selection(parent_frame, file_label, name_entry, advanced_table_frame):
    # Obtener los datos del archivo seleccionado
    data = open_file(file_label, name_entry)
    
    if data is not None:
        # Llamar a la función para crear el Treeview de previsualización
        create_preVisualice_gui(parent_frame, data)
        
        # Cargar los atributos y tipos de datos en la tabla avanzada
        create_advancedOptions_gui(advanced_table_frame, data)



# Función personalizada para crear un rectángulo redondeado en el Canvas
def create_rounded_rect(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)


# Función para crear el interruptor personalizado
def create_modern_toggle_switch(frame, toggle_var, command):
    switch_canvas = Canvas(frame, width=50, height=25, bg="#1e1e1e", highlightthickness=0)
    switch_canvas.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Fondo del switch
    switch_bg = create_rounded_rect(switch_canvas, 0, 0, 50, 25, radius=12, outline="#cccccc", fill="#cccccc", width=2)
    # Círculo del switch
    switch_circle = switch_canvas.create_oval(2, 2, 23, 23, outline="#ffffff", fill="#ffffff", width=2)

    def toggle_switch():
        if toggle_var.get() == 1:
            switch_canvas.itemconfig(switch_bg, fill="#592d80")
            switch_canvas.coords(switch_circle, 27, 2, 48, 23)
            toggle_var.set(0)
        else:
            switch_canvas.itemconfig(switch_bg, fill="#cccccc")
            switch_canvas.coords(switch_circle, 2, 2, 23, 23)
            toggle_var.set(1)
        command()

    switch_canvas.bind("<Button-1>", lambda event: toggle_switch())

# Función para habilitar/deshabilitar el cuadro de texto
def toggle_name_entry(toggle_var, name_entry):
    if toggle_var.get() == 1:
        name_entry.config(state="normal")  # Habilitar el cuadro de texto
    else:
        name_entry.config(state="disabled")  # Deshabilitar el cuadro de texto


# Función para validar el campo "Save As" al convertir
def validate_and_convert(name_entry):
    if not name_entry.get().strip():
        messagebox.showerror("Error", "Please provide a valid file name.")
        name_entry.config(highlightbackground="red", highlightthickness=2)
    else:
        name_entry.config(highlightbackground="#9e64a7", highlightthickness=2)  # Restablecer el borde
        # Aquí se agregaría la lógica de conversión