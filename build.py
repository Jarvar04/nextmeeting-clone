import csv
import urllib.request

SPREADSHEET_ID = "1UJneS5GKFQSIy_iAfkLE21nRC_E8VzJ8diTT4Z3JnrA"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv"

req = urllib.request.Request(CSV_URL, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req)
csv_data = response.read().decode('utf-8').splitlines()

rows = list(csv.reader(csv_data))
data = rows[1:]  # Skip header row

meetings_html = ""
for row in data:
    if len(row) < 6:
        continue
    # Columns: 0: Day, 1: Start Time, 2: Meeting Name, 3: Meeting ID, 4: Password, 5: Join URL
    day, time, title, meeting_id, pwd, link = row[0], row[1], row[2], row[3], row[4], row[5]
    
    meetings_html += f"""
    <div class="card">
        <h3>{title}</h3>
        <p><strong>When:</strong> {day}s at {time} (Eastern)</p>
        <p><strong>Meeting ID:</strong> {meeting_id}</p>
        <a href="{link}" target="_blank" class="btn">Join Meeting ›</a>
    </div>
    """

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NextMeeting S-Anon List</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #0f172a; color: #f8fafc; padding: 2rem; margin: 0; }}
        h1 {{ text-align: center; color: #38bdf8; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; max-width: 1000px; margin: 2rem auto; }}
        .card {{ background: #1e293b; border-radius: 12px; padding: 1.5rem; border: 1px solid #334155; }}
        .btn {{ display: inline-block; margin-top: 1rem; background: #0284c7; color: white; padding: 0.5rem 1rem; text-decoration: none; border-radius: 6px; }}
    </style>
</head>
<body>
    <h1>S-Anon Worldwide Zoom Meetings</h1>
    <div class="grid">
        {meetings_html}
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Generated index.html successfully!")
