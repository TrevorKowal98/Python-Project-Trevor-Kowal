### I could not get this to work I think it has something to do with the port forwarding I have set up on my home network. Not sure though. So I Set up a graphical interface in a different file. ###
### I tried following the grafana documentation as the main idea for this attempt. ###
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

#load data
dataPath = r'C:/Users/nottr/OneDrive/Desktop/Python Project/combined_data/combined_data.csv'
df = pd.read_csv(dataPath)

#database connection
databaseUrl = "postgresql://admin:admin@localhost:3306/grafana"
engine = create_engine(databaseUrl)

def uploadData():
    try:
        #upload data
        df.to_sql('sensor_data', engine, if_exists='replace', index=False)

        #create summary
        statsDf = pd.DataFrame({
            'metric': ['count', 'mean', 'std', 'min', 'max'],
            'value': [len(df), df.mean().mean(), df.std().mean(), df.min().min(), df.max().max()],
            'timestamp': [datetime.now()] * 5})
        
        #upload summary
        statsDf.to_sql('sensor_stats', engine, if_exists='replace', index=False)

        print("Upload successful")
        
    except Exception as e:
        print("Error:", e)
    finally:
        engine.dispose()

if __name__ == "__main__":
    uploadData()

    