import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from guiLogic import visualiceGraphDEF

def create_visualiceGraph_gui(parent_frame):
    # Crear el frame principal dentro del parent_frame
    main_frame = tk.Frame(parent_frame, bg="#2c2c2c")
    main_frame.pack(fill="both", expand=True, padx=10, pady=0)
    main_frame.grid_rowconfigure(0, weight=10)
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)

    show_graph_frame = tk.Frame(main_frame, bg="#1e1e1e")
    show_graph_frame.grid(row=0, column=0, padx=00, pady=0, sticky="nsew")
    
    # Crear un gráfico simple usando matplotlib
    figure = plt.Figure(figsize=(6, 4), dpi=100)
    figure.set_facecolor("#1e1e1e")
    ax = figure.add_subplot(111)
    ax.plot([1, 2, 3, 4], [10, 20, 25, 30], marker="o")  # Un gráfico simple
    ax.set_title('Simple Graph')

    # Colocar el gráfico dentro del frame
    canvas = FigureCanvasTkAgg(figure, show_graph_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

    # Frame para los botones del grafico
    graphic_buttons_frame = tk.Frame(main_frame, bg="#1e1e1e")
    graphic_buttons_frame.grid(row=1, column=0, sticky="ew")
    graphic_buttons_frame.grid_rowconfigure(0, weight=1)
    graphic_buttons_frame.grid_columnconfigure(0, weight=1)
    graphic_buttons_frame.grid_columnconfigure(1, weight=10)
    graphic_buttons_frame.grid_columnconfigure(2, weight=10)

    # Botón de avanzar
    next_graphic_button = tk.Button(graphic_buttons_frame, text=">", command=lambda: visualiceGraphDEF.next_attribute, relief="flat", bg="#952184", cursor="hand2")
    next_graphic_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    # Botón de retroceder
    previus_graphic_button = tk.Button(graphic_buttons_frame, text="<", command=lambda: visualiceGraphDEF.previous_attribute, relief="flat", cursor="hand2")
    previus_graphic_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    # Guardar gráfico
    save_graphic_button = tk.Button(graphic_buttons_frame, text="Save", command=lambda: visualiceGraphDEF.save_graph, relief="flat", cursor="hand2")
    save_graphic_button.grid(row=0, column=0, padx=10, pady=10)
