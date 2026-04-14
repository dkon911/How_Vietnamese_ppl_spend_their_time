import pandas as pd
import json
import os

# Configuration
CSV_PATH = "VN-timeUsage/4_diary_main.csv"
JSON_OUTPUT = "insights.json"

def get_activity_group(code):
    try:
        code = int(code)
    except:
        return "Others"
    # Grouping activities for the business dashboard
    if code in [1404]: return "Social Media/Web"
    if code == 1402: return "TV/Youtube"
    if code in [1502, 1506]: return "Eating/Leisure"
    if code in [1201, 1202, 1203, 1299]: return "Entertainment"
    return "Others"

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    print("🚀 Loading data for aggregation...")
    # Read only necessary columns
    df = pd.read_csv(CSV_PATH, encoding='latin-1', 
                     usecols=['gender', 'MATINH', 'age', 'Q401', 'BEGIN', 'Duration'])

    print("🧹 Processing...")
    df['activity_group'] = df['Q401'].apply(get_activity_group)
    
    # Filter only relevant activities for the dashboard to keep JSON small
    df = df[df['activity_group'] != "Others"]

    # Aggregation logic: Group by Gender, Province, and Activity
    # We calculate the total duration and average start time for each slot
    
    # Pre-calculate time slots
    df['time_slot'] = pd.cut(df['BEGIN'], 
                             bins=[0, 360, 720, 1080, 1440], 
                             labels=['Night', 'Morning', 'Afternoon', 'Evening'],
                             include_lowest=True)

    print("📊 Aggregating business insights...")
    summary = df.groupby(['gender', 'MATINH', 'activity_group', 'time_slot']).agg({
        'Duration': 'sum',
        'BEGIN': 'mean'
    }).reset_index()

    # Convert to a dictionary for JSON
    # Structure: { "gender_province_activity": [ {slot, duration, avg_start}, ... ] }
    insights_dict = {}
    for _, row in summary.iterrows():
        key = f"{row['gender']}_{row['MATINH']}_{row['activity_group']}"
        if key not in insights_dict:
            insights_dict[key] = []
        
        if row['Duration'] > 0:
            insights_dict[key].append({
                "slot": row['time_slot'],
                "duration": int(row['Duration']),
                "avg_start": int(row['BEGIN']) if not pd.isna(row['BEGIN']) else 0
            })

    print(f"💾 Saving aggregated data to {JSON_OUTPUT}...")
    with open(JSON_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(insights_dict, f, ensure_ascii=False, indent=2)

    print(f"✨ SUCCESS: Processed {len(df)} records into a compact JSON file.")

if __name__ == "__main__":
    main()
