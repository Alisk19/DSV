import zipfile
import os
import pandas as pd

zip_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../archive (3).zip'))

print("=== IPL 2025 DATASET FROM ARCHIVE ===")
print("Archive file:", zip_path)

if os.path.exists(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as z:
        print("\nFiles in archive:")
        for name in z.namelist():
            info = z.getinfo(name)
            print(f" - {name} ({info.file_size} bytes)")
            
        print("\nDataset Summary:")
        with z.open('IPL2025Batters.csv') as f:
            df_batters = pd.read_csv(f)
            print(f"Batters: {len(df_batters)} players, Total Runs: {df_batters['Runs'].sum():,}, Total Balls Faced: {df_batters['BF'].sum():,}")
            print(f"Top 3 Batters:\n{df_batters[['Player Name', 'Team', 'Runs', 'SR']].head(3).to_string(index=False)}")
            
        print()
        with z.open('IPL2025Bowlers.csv') as f:
            df_bowlers = pd.read_csv(f)
            print(f"Bowlers: {len(df_bowlers)} players, Total Wickets: {df_bowlers['WKT'].sum():,}")
            print(f"Top 3 Bowlers:\n{df_bowlers[['Player Name', 'Team', 'WKT', 'ECO']].head(3).to_string(index=False)}")
else:
    print(f"Archive not found at {zip_path}")
