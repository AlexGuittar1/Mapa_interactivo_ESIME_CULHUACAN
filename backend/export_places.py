
import sqlite3
import json
import os

# Connect to the database
db_path = 'backend/instance/campus.db'
if not os.path.exists(db_path):
    db_path = 'instance/campus.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fetch NEW saved places from DB
cursor.execute("SELECT id, name, lat, lon FROM saved_places")
rows = cursor.fetchall()
conn.close()

# Load EXISTING key points
json_path = 'frontend/src/data/key_points.json'
existing_places = []
if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            existing_places = json.load(f)
        except json.JSONDecodeError:
            pass

# Determine starting ID for new places to avoid collisions
# (Though we might just re-index everything to be clean)
max_id = 0
for p in existing_places:
    if p.get('id', 0) > max_id:
        max_id = p.get('id', 0)

new_places = []
current_id = max_id + 1

    # Check if this place already exists (by name/location)
    # If it exists, UPDATE it with new coordinates
    name = row[1]
    existing = next((p for p in existing_places if p['name'] == name), None)
    
    if existing:
        print(f"Updating existing point: {name}")
        existing['lat'] = row[2]
        existing['lon'] = row[3]
        # Keep original ID and Type
        continue

    new_places.append({
        "id": current_id,
        "name": name,
        "lat": row[2],
        "lon": row[3],
        "type": "static"
    })
    current_id += 1

# Merge
all_places = existing_places + new_places

# Write back
os.makedirs(os.path.dirname(json_path), exist_ok=True)
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(all_places, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_places)} new places. Total: {len(all_places)}")

