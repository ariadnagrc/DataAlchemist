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

def create_gui():
    # Create main window
    root = TkinterDnD.Tk()
    root.title("Data Alchemist")
    root.geometry("800x600")
    root.configure(bg="#2c2c2c")

    # Set icon
    root.iconbitmap('assets/icon/DataAlchemistIcon.ico')

    # Create main frame 
    main_frame = tk.Frame(root, bg="#2c2c2c")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Configure main frame columns and rows
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=2) 
    main_frame.columnconfigure(2, weight=3)
    main_frame.columnconfigure(3, weight=4)
    main_frame.rowconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=2)

    # Function to receive a file (Only Excel or CSV)
    def open_file(event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Excel and CSV files", "*.xlsx;*.xls;*.csv"), ("Excel files", "*.xlsx;*.xls"), ("CSV files", "*.csv")])
        if file_path:
            file_label.config(text=file_path)
            load_preview(file_path)

    # Frame to select file
    file_select_frame = tk.Frame(main_frame, bg="#1e1e1e", width=250, height=300)
    file_select_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    file_select_frame.pack_propagate(False)

    file_select_title = tk.Label(file_select_frame, text="Select or drag a file", font=("Helvetica Neue", 12, "bold"), bg="#1e1e1e", fg="white")
    file_select_title.pack(pady=(30, 10))

    # Function to drag and drop files
    def drop(event):
        file_path = event.data
        file_label.config(text=file_path)
        load_preview(file_path)

    # Frame (square) to drag and drop files
    drag_drop_frame = tk.Frame(file_select_frame, bg="#1e1e1e", highlightbackground="#9e64a7", highlightthickness=2, highlightcolor="#5c5c5c")
    drag_drop_frame.pack(fill="both", expand=True, padx=20, pady=20)

    file_label = tk.Label(drag_drop_frame, text="No file selected", wraplength=150, bg="#1e1e1e", fg="white", font=("Helvetica Neue", 10))
    file_label.pack(expand=True, pady=(30, 0))

    select_button = tk.Button(drag_drop_frame, text="Select file", command=open_file, font=("Helvetica Neue", 10), bg="#592d80", fg="#ffffff", relief="flat")
    select_button.pack(side="bottom", pady=10)

    file_select_frame.drop_target_register(DND_FILES)
    file_select_frame.dnd_bind('<<Drop>>', drop)

    # Function to preview the file
    def load_preview(file_path):
        try:
            # Detect file type
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension == '.csv':
                df = pd.read_csv(file_path, encoding='ISO-8859-1', header='infer')
                format_combobox.set("ARFF")   # Select ARFF by default
                format_combobox['values'] = ["ARFF"]   # Only allow ARFF
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
                format_combobox['values'] = ["CSV", "ARFF"]  # Allow both conversions
            else:
                raise Exception("Unsupported file format.")

            # Clear table
            tree.delete(*tree.get_children())

            # Configure tree columns
            tree["columns"] = list(df.columns)
            for col in tree["columns"]:
                tree.heading(col, text=col, anchor="center")
                tree.column(col, width=100, minwidth=100, stretch=tk.NO, anchor="center")

            # Insert rows in preview
            for index, row in df.iterrows():
                tree.insert("", "end", values=list(row))

            tree["show"] = "headings"

        except Exception as e:
            messagebox.showerror("Error", f"Error loading preview: {str(e)}")

    # Frame para la vista previa
    preview_frame = tk.Frame(main_frame, bg="#1e1e1e", width=250, height=300)
    preview_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    preview_frame.pack_propagate(False)

    preview_label = tk.Label(preview_frame, text="Preview", font=("Helvetica Neue", 12, "bold"), bg="#1e1e1e", fg="white")
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

    # Frame for the right section
    right_frame = tk.Frame(main_frame, bg="#1e1e1e")
    right_frame.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="nsew")

    right_label = tk.Label(right_frame, text="Select the conversion type", font=("Helvetica Neue", 12, "bold"), bg="#1e1e1e", fg="white")
    right_label.pack(pady=(25, 5)) 

    # Frame to select a file
    select_options_frame = tk.Frame(right_frame, bg="#1e1e1e")
    select_options_frame.pack(expand=True, padx=(50,50), fill="none")

    # Function to get the selected value from the combobox
    def on_format_select(event):
        format_selected = format_combobox.get()

    # List for selecting file to convert
    format_combobox = ttk.Combobox(select_options_frame, values=["CSV", "ARFF"], state="readonly", font=("Helvetica Neue", 10))
    format_combobox.pack(padx=(0, 10), side="left")  
    format_combobox.bind("<<ComboboxSelected>>", on_format_select)

    # Frame to choose the save path
    save_frame = tk.Frame(right_frame, bg="#1e1e1e", highlightbackground="#9e64a7", highlightthickness=1)
    save_frame.pack(expand=True, pady=(15, 15), padx=(50,50), fill="x")

    # Function to select the save path
    def choose_save_location():
        save_directory = filedialog.askdirectory()
        if save_directory:
            save_path_label.config(text=f"Save to: {save_directory}")
            convert_button.config(state="normal", bg="#cc66df")

    # Label and button to select save location
    save_path_label = tk.Label(save_frame, text="Save to: ", bg="#1e1e1e", fg="white", font=("Helvetica Neue", 10))
    save_path_label.pack(side="left", padx=(30,30))

    select_save_button = tk.Button(save_frame, text="Select path", command=choose_save_location, font=("Helvetica Neue", 10), bg="#592d80", fg="#ffffff", relief="flat")
    select_save_button.pack(side="right", padx=(30, 30), pady=10) 

    # Function to convert the file to the selected format
    def convert():
        file_path = file_label.cget("text")

        if not file_path or file_path == "No file selected":
            messagebox.showerror("Error", "You must select a file.")
            return

        format_selected = format_combobox.get()
        
        if not format_selected:
            messagebox.showerror("Error", "Select a format to save.")
            return
        
        save_directory = save_path_label.cget("text").replace("Save to: ", "")
        
        if not save_directory and format_selected == "CSV":
            messagebox.showerror("Error", "Select a path to save the file.")
            return
        
        try:
            file_path_out, df_global = convert_file(file_path, format_selected)

            if format_selected == "ARFF":
                messagebox.showinfo("Success", f"File converted to ARFF: {file_path_out}")
                graphing(df_global)
            else:
                messagebox.showinfo("Success", f"File converted to CSV: {file_path_out}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while converting: {str(e)}")

    # Convert file button
    convert_button = tk.Button(right_frame, text="Convert file", command=convert, font=("Helvetica Neue", 10), bg="#a5a5a5", fg="#ffffff", relief="flat", state="disabled")
    convert_button.pack(expand=True) 

    # Frame to view the graphs
    graphic_preview_frame = tk.Frame(main_frame, bg="#1e1e1e", height=60)
    graphic_preview_frame.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")
    graphic_preview_frame.columnconfigure(0, weight=0)
    graphic_preview_frame.columnconfigure(1, weight=2)
    graphic_preview_frame.rowconfigure(0, weight=1)

    # Create the figure for the graph
    fig = plt.Figure(figsize=(4, 3))
    fig.set_facecolor("#1e1e1e")

    # Create the tkinter canvas to insert the figure into the frame
    canvas = FigureCanvasTkAgg(fig, master=graphic_preview_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Function to update the graph based on the attribute
    def update_graph():
        global current_index, data
        fig.clear()                             # Clear the previous figure
        atributo = data.columns[current_index]  # Get the name of the current attribute
        ax = fig.add_subplot(111)               # Create a new graph for the current attribute
        ax.set_facecolor("#1e1e1e") 
        
        # Check the data type to decide which graph to use
        if pd.api.types.is_numeric_dtype(data[atributo]):
            # Check if there is enough data to graph
            if not data[atributo].isnull().all():
                ax.plot(data.index, data[atributo], marker="o", linestyle="-", color="#a044b2")
                ax.set_ylabel(atributo, color="white")
                ax.set_title(f'{atributo} graph', color="white")
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
            else:
                ax.text(0.5, 0.5, 'There is no numerical data to graph.', 
                        ha='center', va='center', color='white', fontsize=12)
        else:
            # Check that it is not empty before graphing
            counts = data[atributo].value_counts()
            if counts.empty:
                ax.text(0.5, 0.5, 'There is no categorical data to graph.', 
                        ha='center', va='center', color='white', fontsize=12)
            else:
                counts.plot(kind='bar', ax=ax, color="#a044b2")
                ax.set_title(f'{atributo}', color="white")
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')  

        canvas.draw()  

    # Function to load and graph the converted file automatically
    def graphing(df):
        global data, current_index

        # Verify that the DataFrame is not empty
        if df is None or df.empty:
            messagebox.showerror("Error", "There is no data to graph.")
            return

        data = df             # Store the global DataFrame in the 'data' variable
        current_index = 0     # Reset index to first attribute
        update_graph()        # Show first graph

    # Simulation of example data:
    df_global = pd.DataFrame({
        "No data": [""],
    })

    # Load and plot simulated data
    graphing(df_global)  

    # Function to go back to the previous graph
    def previous_attribute():
        global current_index, data

        if data is not None:
            current_index = (current_index - 1) % len(data.columns)
            update_graph()

    # Button to go back between graphs
    previous_button = tk.Button(graphic_preview_frame, text="<", command=previous_attribute,font=("Helvetica Neue", 10), bg="#592d80", fg="#ffffff", relief="flat")
    previous_button.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    # Function to advance to the next graph
    def next_attribute():
        global current_index, data

        if data is not None:
            current_index = (current_index + 1) % len(data.columns)
            update_graph()

    # Button to advance between graphs
    next_button = tk.Button(graphic_preview_frame, text=">", command=next_attribute, font=("Helvetica Neue", 10), bg="#592d80", fg="#ffffff", relief="flat")
    next_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    # Function to save the graph
    def save_graph():
        file_path = filedialog.asksaveasfilename(   # Open a dialog box to select the file path and name
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save graph"
        )
        if file_path: 
            fig.savefig(file_path, format='png', bbox_inches='tight', dpi=300)
            messagebox.showinfo("Success", "Graph saved successfully.")

    # Graph save button
    save_button = tk.Button(graphic_preview_frame, text="Save", bg="#592d80", fg="#ffffff", relief="flat", borderwidth=0, command=save_graph)
    save_button.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

    root.mainloop()
