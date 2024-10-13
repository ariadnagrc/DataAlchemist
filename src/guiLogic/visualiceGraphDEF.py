import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import pandas as pd 
from tkinter import messagebox  
from tkinter import filedialog  

# Function to update the graph based on the attribute
def update_graph(figure,canvas):
    global current_index, data
    figure.clear()                             # Clear the previous figure
    atributo = data.columns[current_index]  # Get the name of the current attribute
    ax = figure.add_subplot(111)               # Create a new graph for the current attribute
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

# Function to advance to the next graph
def next_attribute():
    global current_index, data

    if data is not None:
        current_index = (current_index + 1) % len(data.columns)
        update_graph()

# Function to go back to the previous graph
def previous_attribute():
    global current_index, data

    if data is not None:
        current_index = (current_index - 1) % len(data.columns)
        update_graph()

# Function to save the graph
def save_graph(figure):
    file_path = filedialog.asksaveasfilename(   # Open a dialog box to select the file path and name
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        title="Save graph"
    )
    if file_path: 
        figure.savefig(file_path, format='png', bbox_inches='tight', dpi=300)
        messagebox.showinfo("Success", "Graph saved successfully.")