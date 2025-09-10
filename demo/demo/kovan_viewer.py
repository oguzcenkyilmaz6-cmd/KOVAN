# Basit KOVAN görselleştirici: XML patern okur, PNG üretir
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from pathlib import Path

XML_PATH = "demo/sample_iredes.xml"
OUT_PATH = "demo/out_pattern.png"

def load_plan(xml_path):
    root = ET.parse(xml_path).getroot()
    holes = [{
        "id": h.attrib["id"],
        "x": float(h.attrib["x"]),
        "y": float(h.attrib["y"])
    } for h in root.find('Holes')]
    measured = {m.attrib["id"]: (float(m.attrib["dx"]), float(m.attrib["dy"]))
                for m in (root.find('Measured') or [])}
    return holes, measured

def plot_pattern(holes, measured, out_path):
    xs = [h["x"] for h in holes]; ys = [h["y"] for h in holes]
    plt.figure(figsize=(8,6))
    # Plan delikleri (altın sarısı noktalar)
    plt.scatter(xs, ys, s=120, edgecolor="black", facecolor="#D4AF37", linewidth=1.2, label="Plan Delik")
    # Ölçülen giriş sapmaları (kırmızı oklar)
    for h in holes:
        if h["id"] in measured:
            dx, dy = measured[h["id"]]
            plt.arrow(h["x"], h["y"], dx, dy, head_width=0.08, head_length=0.12,
                      length_includes_head=True, color="crimson")
            plt.text(h["x"], h["y"]+0.12, h["id"], fontsize=9)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.grid(True, linestyle="--", alpha=0.25)
    plt.xlabel("X (m)"); plt.ylabel("Y (m)")
    plt.title("KOVAN • Patern Görüntüleyici (Plan vs. Ölçülen Giriş Sapması)")
    plt.legend(loc="upper right")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout(); plt.savefig(out_path, dpi=180)
    print(f"[✓] {out_path} kaydedildi.")

if __name__ == "__main__":
    holes, measured = load_plan(XML_PATH)
    plot_pattern(holes, measured, OUT_PATH)
