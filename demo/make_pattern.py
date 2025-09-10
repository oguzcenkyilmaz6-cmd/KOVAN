# demo/make_pattern.py
# Basit patern üretici: satır/sütun ve aralıklara göre IREDES-benzeri XML yazar.
from pathlib import Path

def make_xml(cols=3, rows=3, sx=1.2, sy=1.0, depth_start=2.8, dip=-1.5, name="SampleRound"):
    holes = []
    for r in range(rows):
        for c in range(cols):
            x = c * sx
            y = r * sy
            depth = round(depth_start + (0.2 if r == 0 else 0.0), 2)
            holes.append((f"H{r*cols+c+1}", x, y, depth, dip))
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<Plan name="{name}" unit="meter">',
        '  <Origin x="0.0" y="0.0" azimuth_deg="0.0"/>',
        '  <Holes>'
    ]
    for hid,x,y,depth,d in holes:
        parts.append(f'    <Hole id="{hid}" x="{x}" y="{y}" depth="{depth}" dip_deg="{d}"/>')
    parts += [
        '  </Holes>',
        '  <Measured>',  # örnek 3 deliğe kıl payı sapma
        '    <Entry id="H1" dx="0.02" dy="-0.01"/>',
        '    <Entry id="H2" dx="-0.03" dy="0.01"/>',
        '    <Entry id="H3" dx="0.01" dy="-0.02"/>',
        '  </Measured>',
        '</Plan>'
    ]
    Path("demo").mkdir(exist_ok=True)
    Path("demo/sample_iredes.xml").write_text("\n".join(parts), encoding="utf-8")
    print("[✓] demo/sample_iredes.xml üretildi.")

if __name__ == "__main__":
    make_xml(cols=3, rows=3, sx=1.2, sy=1.0)
