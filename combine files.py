import pandas as pd
import os
from datetime import datetime
import zipfile

#Unzip the files
zipFile = r'C:/Users/nottr/OneDrive/Desktop/Python Project/archive.zip'
folder = r'C:/Users/nottr/OneDrive/Desktop/Python Project/combined_data'

#file setup/manipulation 
zipRef = zipfile.ZipFile(zipFile, 'r')
zipRef.extractall(folder)
zipRef.close()
allFiles = []

#Walk through the folder to find CSV files
for root, dirs, files in os.walk(folder):
    for file in files:
        #Check if the file is a CSV
        if file.endswith('.csv'):
            #Get the full path of the file
            fullPath = os.path.join(root, file)
            #Add the file path to the list
            allFiles.append(fullPath)

#function to get date from filename
def getDateFromFilename(filename):
    #Get just the filename without path
    name = os.path.basename(filename)
    print(f"Processing filename: {name}")  
    datePart = name.split('_')[0]
    print(f"Date part: {datePart}")  


    ### BEGIN AI ASSISTANCE ### 
    #error in the data where there is a feb 30th and this seems to break the datetime function. 
    if datePart.startswith('02-'):  
        dateWithYear = "2024-" + datePart
    else:
        dateWithYear = "2023-" + datePart
    print(f"Date with year: {dateWithYear}")  
    
    try:
        #Convert to datetime
        date = datetime.strptime(dateWithYear, "%Y-%m-%dT%H%M%S")
        return date
    except ValueError as e:
        print(f"Error with file {name}: {e}")  #Error print
        #Return a default date for files that cant be parsed
        return datetime(2000, 1, 1)  #Default date
    ### END AI ASSISTANCE ###

#sort the files by date
allFiles.sort(key=getDateFromFilename)

#List to store all data
allData = []

#Read and combine all files
for file in allFiles:
    #Read each CSV file
    data = pd.read_csv(file)
    #Add it to list
    allData.append(data)

#Combine all the data
finalData = pd.concat(allData)

#save the combined data
outputFile = r'C:/Users/nottr/OneDrive/Desktop/Python Project/combined_data/combined_data.csv'
finalData.to_csv(outputFile, index=False)

print(f"All files combined! Saved to: {outputFile}")
