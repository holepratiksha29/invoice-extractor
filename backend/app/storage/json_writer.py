import json
import os
from datetime import datetime
from app.core.config import OUTPUT_DIR

def save_json(data):
    name = f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = os.path.join(OUTPUT_DIR, name)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        print(f"Saved JSON: {path}")
    return path
