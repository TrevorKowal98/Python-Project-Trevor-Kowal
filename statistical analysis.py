import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tabulate import tabulate

class MachineChecker:
    #create window for application
    def __init__(self, window):
        self.window = window
        self.window.title("Machine Checker")
        self.window.geometry("600x400")
        
        #initialize data and parameters
        self.myData = None
        self.parameters = [
            "pCut::Motor_Torque",
            "pCut::CTRL_Position_controller::Lag_error",
            "pCut::CTRL_Position_controller::Actual_position",
            "pCut::CTRL_Position_controller::Actual_speed",
            "pSvolFilm::CTRL_Position_controller::Lag_error",
            "pSpintor::VAX_speed"
        ]
        
        #set up the user interface
        self.createUI()
    
    def createUI(self):
        #create a frame for buttons
        buttonFrame = ttk.Frame(self.window)
        buttonFrame.pack(fill=tk.X, pady=10)
        
        #add buttons for loading data, showing stats, and plotting
        ttk.Button(buttonFrame, text="Load Data", command=self.loadData).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttonFrame, text="Show Stats", command=self.showStats).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttonFrame, text="Plot", command=self.plotData).pack(side=tk.LEFT, padx=5)
        
        #dropdown for selecting parameters to plot
        self.parameterSelection = tk.StringVar()
        self.parameterDropdown = ttk.Combobox(buttonFrame, textvariable=self.parameterSelection, values=self.parameters)
        self.parameterDropdown.pack(side=tk.LEFT, padx=5)
        
        #text area to display statistics
        self.textDisplay = tk.Text(self.window, height=10, font=("Courier", 10))
        self.textDisplay.pack(fill=tk.BOTH, expand=True)
    
    def loadData(self):
        #load data from a CSV file
        file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file:
            self.myData = pd.read_csv(file)
            self.myData.set_index('timestamp', inplace=True)
            messagebox.showinfo("Success", "File loaded successfully!")
    
    def showStats(self):
        #display statistics of the selected parameters
        if self.myData is None:
            messagebox.showwarning("Warning", "Please load data first")
            return
        
        #calculate and display statistics
        stats = self.myData[self.parameters].describe()
        table = tabulate(stats, headers='keys', tablefmt='fancy_grid')
        self.textDisplay.delete(1.0, tk.END)
        self.textDisplay.insert(tk.END, table)
    
    def plotData(self):
        #plot the selected parameter
        if self.myData is None:
            messagebox.showwarning("Warning", "Please load data first")
            return
        
        selectedParameter = self.parameterSelection.get()
        if not selectedParameter:
            messagebox.showwarning("Warning", "Please select a parameter to plot")
            return
        
        #drop empty values and plot the data
        data = self.myData[selectedParameter].dropna()
        if data.empty:
            messagebox.showerror("Error", f"No valid data for '{selectedParameter}'")
            return
        
        plt.figure(figsize=(8, 5))
        plt.plot(data, label='Data')
        plt.title(f"Plot of {selectedParameter}")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    #create the main application window and run the app
    window = tk.Tk()
    app = MachineChecker(window)
    window.mainloop()

