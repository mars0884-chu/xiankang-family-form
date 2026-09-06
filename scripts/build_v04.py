import base64
import gzip
from pathlib import Path

paths = [
    'src/form-v05.part1.b64',
    'src/v05-02.b64',
    'src/v05-03.b64',
    'src/v05-04.b64',
    'src/v05-05.b64',
    'src/form-v05.part2.b64',
]
data = ''.join(Path(p).read_text(encoding='utf-8').strip() for p in paths)
raw = gzip.decompress(base64.b64decode(data))
text = raw.decode('utf-8')
assert '第五版測試 v0.5' in text
assert '朝代／時期' in text and '婚配稱謂' in text and '功名／科舉' in text
assert 'baseball-GM' not in text and 'raw.githack' not in text.lower() and 'jotform' not in text.lower()
Path('index.html').write_bytes(raw)
print('generated standalone index.html', len(raw), 'bytes')
