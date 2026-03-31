import json
from pathlib import Path

path = Path("data/demo_patients.json")
print(json.loads(path.read_text(encoding="utf-8")))
