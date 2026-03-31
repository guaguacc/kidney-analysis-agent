import json
from pathlib import Path

path = Path("app/knowledge/reference_ranges.json")
print(json.loads(path.read_text(encoding="utf-8")))
