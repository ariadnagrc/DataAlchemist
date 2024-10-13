import tkinter as tk
from tkinterdnd2 import TkinterDnD
from .converterUI import create_converter_gui
from .preVisualiceUI import create_preVisualice_gui
from .advancedOptionsUI import create_advancedOptions_gui
from .visualiceGraphUI import create_visualiceGraph_gui

# Función para cambiar entre pantallas y ajustar la fila separadora
def show_frame(frame, active_button, buttons, separator_frames):
    # Mostrar el frame deseado
    frame.tkraise()

    # Ajustar el color de los botones y los separadores
    for i, button in enumerate(buttons):
        if button == active_button:
            button.config(bg="#2c2c2c")  # Botón activo con color verde
            separator_frames[i].config(bg="#1e1e1e")  # Conectar la columna seleccionada con gris oscuro
        else:
            button.config(bg="#592d80")  # Botones no seleccionados con el color original
            separator_frames[i].config(bg="#2c2c2c")  # Separadores de las columnas no seleccionadas en gris claro

def create_gui():
    # Crear la ventana principal
    root = TkinterDnD.Tk()
    root.title("Data Alchemist")
    root.geometry("800x600")
    root.configure(bg="#2c2c2c")

    # Crear el frame principal 
    main_frame = tk.Frame(root, bg="#2c2c2c")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_rowconfigure(1, weight=0)
    main_frame.grid_rowconfigure(2, weight=20)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=2)

    # Frame para el menú principal
    main_menu_frame = tk.Frame(main_frame, bg="#1e1e1e")
    main_menu_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=0, sticky="nsew")
    main_menu_frame.grid_rowconfigure(0, weight=1)
    main_menu_frame.grid_columnconfigure(0, weight=1)
    main_menu_frame.grid_columnconfigure(1, weight=1)
    main_menu_frame.grid_columnconfigure(2, weight=1)
    main_menu_frame.grid_columnconfigure(3, weight=1)

    # Fila separadora justo debajo del menú (dividida en 4 columnas)
    separator_frame1 = tk.Frame(main_menu_frame, bg="#1e1e1e", height=20)
    separator_frame2 = tk.Frame(main_menu_frame, bg="#1e1e1e", height=20)
    separator_frame3 = tk.Frame(main_menu_frame, bg="#1e1e1e", height=20)
    separator_frame4 = tk.Frame(main_menu_frame, bg="#1e1e1e", height=20)

    separator_frames = [separator_frame1, separator_frame2, separator_frame3, separator_frame4]

    # Colocar los separadores en la fila 1 (debajo del menú)
    separator_frame1.grid(row=1, column=0, sticky="nsew")
    separator_frame2.grid(row=1, column=1, sticky="nsew")
    separator_frame3.grid(row=1, column=2, sticky="nsew")
    separator_frame4.grid(row=1, column=3, sticky="nsew")

    # Contenedor para las pantallas
    container = tk.Frame(main_frame, bg="#2c2c2c")
    container.grid(row=2, column=0, columnspan=2, padx=10, pady=0, sticky="nsew")
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    # Crear los frames de cada pantalla
    converter_frame = tk.Frame(container, bg="#2c2c2c")
    preVisualice_frame = tk.Frame(container, bg="#2c2c2c")
    advancedOptions_frame = tk.Frame(container, bg="#2c2c2c")
    visualiceGraph_frame = tk.Frame(container, bg="#2c2c2c")

    # Posicionar los frames (para que estén en el mismo lugar)
    for frame in (converter_frame, preVisualice_frame, advancedOptions_frame, visualiceGraph_frame):
        frame.grid(row=0, column=0, sticky="nsew")

    # Añadir el contenido a cada pantalla llamando a las funciones que crean las GUIs específicas
    create_converter_gui(converter_frame, preVisualice_frame, advancedOptions_frame)
    create_preVisualice_gui(preVisualice_frame)
    create_advancedOptions_gui(advancedOptions_frame)
    create_visualiceGraph_gui(visualiceGraph_frame)

    # Crear los botones del menú principal
    menu_convert_button = tk.Button(main_menu_frame, text="Converter", font=("Helvetica Neue", 10), bg="#592d80", fg="#ffffff", relief="flat")
    visualice_predata_button = tk.Button(main_menu_frame, text="Visualice pre-data", font=("Helvetica Neue", 10), bg="#592d80", fg="#ffffff", relief="flat")
    advanced_settings_button = tk.Button(main_menu_frame, text="Advanced settings", font=("Helvetica Neue", 10), bg="#592d80", fg="#ffffff", relief="flat")
    visualice_graph_button = tk.Button(main_menu_frame, text="Visualice graph", font=("Helvetica Neue", 10), bg="#592d80", fg="#ffffff", relief="flat")

    # Listado de botones para gestionar el cambio de color y espaciado
    buttons = [menu_convert_button, visualice_predata_button, advanced_settings_button, visualice_graph_button]

    # Configurar las acciones de cada botón con lambda
    menu_convert_button.config(command=lambda: show_frame(converter_frame, menu_convert_button, buttons, separator_frames))
    visualice_predata_button.config(command=lambda: show_frame(preVisualice_frame, visualice_predata_button, buttons, separator_frames))
    advanced_settings_button.config(command=lambda: show_frame(advancedOptions_frame, advanced_settings_button, buttons, separator_frames))
    visualice_graph_button.config(command=lambda: show_frame(visualiceGraph_frame, visualice_graph_button, buttons, separator_frames))

    # Colocar los botones en el menú
    menu_convert_button.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsew")
    visualice_predata_button.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")
    advanced_settings_button.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="nsew")
    visualice_graph_button.grid(row=0, column=3, padx=10, pady=(10, 10), sticky="nsew")

    # Mostrar el frame inicial y resaltar el botón inicial
    show_frame(converter_frame, menu_convert_button, buttons, separator_frames)

    # Iniciar la aplicación
    root.mainloop()

if __name__ == "__main__":
    create_gui()
