import pandas as pd
from time import gmtime, strftime
from d3blocks import D3Blocks
import os
import re

def convert_time(minute):
    return strftime("%d-%m-%Y %H:%M:%S", gmtime(int(minute) * 60))

def get_activity(code):
    try:
        code = int(code)
    except:
        return "Others"
    mapping = {
        (101, 102, 199, 201, 202, 299, 301, 302, 399, 401, 402, 499, 502): "Work",
        (198, 298, 498, 598, 698, 798, 898, 998, 1098, 1198, 1298, 1398, 1498, 1598): "Travelling",
        (501,): "Sell food",
        (504, 505, 506, 507, 508): "Provide services",
        (601,): "Housework",
        (602,): "Shopping",
        (701, 702): "Caring",
        (901, 902, 903): "Education",
        (1201, 1202, 1203, 1299): "Entertainment",
        (1301, 1302, 1399): "Sport",
        (1402,): "TV/Youtube",
        (1404,): "Surf web",
        (1501,): "Sleeping",
        (1502,): "Eating",
        (1503,): "Personal hygiene",
        (1506,): "Relaxing"
    }
    for codes, name in mapping.items():
        if code in codes: return name
    return "Others"

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "4_diary_main.csv")
output_path = os.path.join(base_dir, "movingpoints.html")

print(f"🚀 Loading full dataset from: {csv_path}")
data = pd.read_csv(csv_path, encoding='latin-1', usecols=['ID', 'BEGIN', 'Q401'])

print("🧹 Preprocessing data...")
data['state'] = data['Q401'].apply(get_activity)
data['date_time'] = data['BEGIN'].apply(convert_time)
data = data.rename(columns=({"ID": "sample_id"}))
data = data.sort_values(["sample_id", "BEGIN"])

print(f"✅ Loaded {len(data['sample_id'].unique())} unique individuals.")

print("📊 Initializing D3Blocks...")
d3 = D3Blocks()
d3.movingbubbles(data.head(100000), 
                 datetime="date_time", 
                 sample_id="sample_id", 
                 state="state", 
                 filepath=output_path,
                 note="Vietnam Time-use Survey 2022", 
                 cmap="hsv", 
                 figsize=(780, 800), 
                 size=2)

# UI Patching to maintain custom "Liquid Glass" theme
print("🎨 Patching custom UI theme...")

CUSTOM_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); 
    color: #e2e8f0;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 2rem;
}
#main-wrapper {
    display: flex;
    gap: 40px;
    width: 100%;
    max-width: 1200px;
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}
#sidebar { width: 280px; display: flex; flex-direction: column; gap: 30px; }
.time-container { text-align: center; padding-bottom: 25px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
#current_day { font-size: 1.1rem; color: #94a3b8; font-weight: 300; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px; }
#current_time { font-family: 'JetBrains Mono', monospace; font-size: 3.5rem; color: #38bdf8; font-weight: 700; text-shadow: 0 0 20px rgba(56, 189, 248, 0.3); }
#speed { display: flex; background: rgba(0, 0, 0, 0.2); border-radius: 12px; padding: 4px; border: 1px solid rgba(255, 255, 255, 0.05); }
#speed .togglebutton { flex: 1; text-align: center; padding: 10px 0; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #64748b; cursor: pointer; border-radius: 8px; transition: all 0.3s ease; }
#speed .togglebutton.current { background: #38bdf8; color: #0f172a; box-shadow: 0 0 15px rgba(56, 189, 248, 0.4); }
.control-group { display: flex; flex-direction: column; gap: 10px; }
.control-group b { font-size: 0.85rem; color: #94a3b8; font-weight: 400; text-transform: uppercase; letter-spacing: 1px; }
select, button { width: 100%; padding: 14px 16px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; color: #f8fafc; font-family: 'Inter', sans-serif; font-size: 0.95rem; cursor: pointer; outline: none; transition: all 0.2s ease; }
select { appearance: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2394a3b8'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 12px center; background-size: 16px; }
button#saveButton { background: rgba(56, 189, 248, 0.1); color: #38bdf8; border-color: rgba(56, 189, 248, 0.3); font-weight: 600; }
#chart { flex: 1; display: flex; justify-content: center; align-items: center; }
.actlabel { fill: #94a3b8 !important; font-family: 'Inter', sans-serif; font-size: 13px; }
.actpct { fill: #f8fafc !important; font-weight: 600; font-size: 15px; }
circle { stroke: rgba(255, 255, 255, 0.15); stroke-width: 0.5px; }
#cite { margin-top: auto; font-size: 0.75rem; color: #64748b; text-align: center; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.05); }
</style>
"""

CUSTOM_BODY = """
    <div id="main-wrapper">
        <div id="sidebar">
            <div class="time-container">
                <div id="current_day">&nbsp;</div>
                <div id="current_time">04:00</div>
            </div>
            <div id="speed">
                <div class="togglebutton pause" data-val="pause">Pause</div>
                <div class="togglebutton slow current" data-val="slow">Slow</div>
                <div class="togglebutton medium" data-val="medium">Med</div>
                <div class="togglebutton fast" data-val="fast">Fast</div>
            </div>
            <div class="control-group">
                <b>Color Palette</b>
                <select id="ColorOptions" onchange="link_color_changed(this.value)">
                  <option value="STATE" selected="selected">By State</option>
                  <option value="NODE">By Sample ID</option>
                </select>
            </div>
            <div class="control-group">
                <b>Export</b>
                <button id="saveButton">Save Chart to SVG</button>
            </div>
            <div id="note"></div>
            <div id="cite">Vietnam Time-use Survey 2022 (Full Data)</div>
        </div>
        <div id="chart"></div>
    </div>
"""

with open(output_path, 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'<style>.*?</style>', CUSTOM_CSS, html, flags=re.DOTALL)
html = re.sub(r'<body>.*?<script>', f'<body>{CUSTOM_BODY}<script>', html, flags=re.DOTALL)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✨ SUCCESS: View generated at {output_path}")
