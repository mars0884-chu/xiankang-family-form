import base64
import gzip
from pathlib import Path

parts = [Path(f"src/form-v05.part{i}.b64").read_text(encoding="utf-8").strip() for i in (1, 2, 3)]
data = "".join(parts)
raw = gzip.decompress(base64.b64decode(data))
text = raw.decode("utf-8")

assert "第五版測試 v0.5" in text
assert "朝代／時期" in text
assert "婚配稱謂" in text
assert "功名／科舉" in text
assert "baseball-GM" not in text
assert "raw.githack" not in text.lower()
assert "jotform" not in text.lower()

Path("index.html").write_bytes(raw)
print("generated standalone index.html", len(raw), "bytes")
