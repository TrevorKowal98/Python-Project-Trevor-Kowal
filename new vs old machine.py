import os
import pandas as pd
import matplotlib.pyplot as plt

#data files
dataFolder = os.path.join(os.path.dirname(__file__), "new vs worn machine data")

#save csv files
outputFolder = os.path.join(os.path.dirname(__file__), "graph_data")

def loadData(folder, prefix):
    #List all csv files in the folder with the given prefix
    dataFiles = [os.path.join(folder, file) for file in os.listdir(folder) if file.startswith(prefix) and file.endswith(".csv")]
    #Read each csv file into a Dataframe and concatenate them into a single Dataframe
    allData = [pd.read_csv(file) for file in dataFiles]
    return pd.concat(allData, ignore_index=True)

def printColumnNames(data, label):
    #Print the column names of the Dataframe with a label
    print("\n" + label + " columns:")
    for column in data.columns:
        print("  - " + column)

#Load data for new and worn blades
print("Loading new blade data...")
newBladeData = loadData(dataFolder, "NewBlade")
print("Loading worn blade data...")
wornBladeData = loadData(dataFolder, "WornBlade")

#Columns to compare between new and worn blade data
columnsToCompare = ["pCut Motor: Torque",
    " pCut CTRL Position controller: Lag error",
    " pCut CTRL Position controller: Actual speed",
    " pSvolFilm CTRL Position controller: Actual speed"]

def plotTimeSeriesComparison(newData, wornData, column, ax):
    #Plot time series data for both new and worn blades
    ax.plot(newData["Timestamp"], newData[column], label="New Blade", alpha=0.5)
    ax.plot(wornData["Timestamp"], wornData[column], label="Worn Blade", alpha=0.5)
    ax.set_title("Time Series Comparison: " + column)
    ax.set_xlabel("Timestamp")
    ax.set_ylabel(column)
    ax.legend()

def plotBoxComparison(newData, wornData, column, ax):
    #Create a box plot comparison for the specified column
    dataPlot = [newData[column].dropna(), wornData[column].dropna()]
    ax.boxplot(dataPlot, labels=["New Blade", "Worn Blade"])
    ax.set_title("Box Plot Comparison: " + column)
    ax.set_ylabel(column)

#Set up the figure and axes for plots 
figure, axes = plt.subplots(len(columnsToCompare), 2, figsize=(15, len(columnsToCompare) * 5))

#Iterate over each column to compare
for i, column in enumerate(columnsToCompare):
    print("Making line plot for: " + column)
    #Plot time series comparison
    plotTimeSeriesComparison(newBladeData, wornBladeData, column, axes[i, 0])
    print("Making box plot for: " + column)
    #Plot box plot comparison
    plotBoxComparison(newBladeData, wornBladeData, column, axes[i, 1])

#Adjust layout and display plots
plt.tight_layout()
print("Showing all plots...")
plt.show()


