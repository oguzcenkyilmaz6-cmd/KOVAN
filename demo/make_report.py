# demo/make_report.py
import xml.etree.ElementTree as ET
from pathlib import Path
from math import hypot
XML = "demo/sample_iredes.xml"

def load():
    r = ET.parse(XML).getroot()
    holes = [{"id":h.attrib["id"],"x":float(h.attrib["x"]),"y":float(h.attrib["y"])} for h in r.find("Holes")]
    meas = {m.attrib["id"]:(float(m.attrib["dx"]),float(m.attrib["dy"])) for m in (r.find("Measured") or [])}
    return holes, meas

def stats(holes, meas):
    n = len(holes)
    xs=[h["x"] for h in holes]; ys=[h["y"] for h in holes]
    minx,maxx,miny,maxy = min(xs),max(xs),min(ys),max(ys)
    # basit komşu mesafe tahmini (x ve y aralıklarından)
    sx = round(min([abs(holes[i+1]["x"]-holes[i]["x"]) for i in range(n-1) if holes[i+1]["y"]==holes[i]["y"]] or [0]),3)
    sy = round(min([abs(h["y"]-miny) for h in holes if h["y"]!=miny] or [0]),3)
    # sapmalar
    mags = [hypot(dx,dy) for hid,(dx,dy) in meas.items()]
    avg_off = round(sum(mags)/len(mags),3) if mags else 0.0
    max_off = round(max(mags),3) if mags else 0.0
    return {
        "hole_count": n,
        "grid_width_m": round(maxx-minx,3),
        "grid_height_m": round(maxy-miny,3),
        "spacing_x_m": sx, "spacing_y_m": sy,
        "avg_entry_offset_m": avg_off, "max_entry_offset_m": max_off
    }

def write_outputs(s):
    Path("docs").mkdir(exist_ok=True)
    Path("docs/round_report.csv").write_text(
        "metric,value\n" + "\n".join(f"{k},{v}" for k,v in s.items()), encoding="utf-8"
    )
    md = [
        "# KOVAN Round Raporu",
        "",
        "| Metrik | Değer |",
        "|---|---:|",
    ] + [f"| {k} | {v} |" for k,v in s.items()]
    Path("docs/round_report.md").write_text("\n".join(md), encoding="utf-8")
    print("[✓] docs/round_report.csv ve docs/round_report.md üretildi.")

if __name__ == "__main__":
    holes, meas = load()
    s = stats(holes, meas)
    write_outputs(s)
