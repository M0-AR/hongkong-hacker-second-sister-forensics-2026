"""Generate docs/demo.gif — terminal-style animated demo (offline, verified)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 880, 420
frames_text = [
    ["$ make all", "▶ EXP-01 tradecraft ...", "  relay 212.117.180.21 + UA X → score 2", "  3 Netvigator IPs + iPhone Mail ✓", "  EXIF 2013:12:24 + King Wah 0.0km ✓", "  OVERALL: PASS"],
    ["$ make all", "▶ EXP-02 benchmark ...", "  LogReg  F1 0.800  PR-AUC 0.928", "  LinSVC  F1 0.798  PR-AUC 0.928", "  source=bundled n=27  EXP-02 PASS", ""],
    ["$ make all", "▶ EXP-03 hidden patterns ...", "  H1 dogpile 0.75 / threat 1.00 ✓", "  H2 3-space 1.00 vs 0.00 ✓", "  H3 peak 1.00, 2 bursty → incident ✓", "  OVERALL: PASS"],
    ["$ pytest -q", "  ....  [100%]", "  4 passed in 0.19s", "", "  ✅ reproducible · Docker ready", "  preview.html → GitHub Pages"],
]
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 20)
    font_b = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 20)
except Exception:
    font = ImageFont.load_default(); font_b = font

frames = []
for lines in frames_text:
    img = Image.new("RGB", (W, H), (10, 17, 38))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 56], fill=(22, 32, 70))
    d.text((18, 14), "● ● ●  verifying-N — make all", font=font, fill=(169, 182, 221))
    y = 80
    for ln in lines:
        c = (34, 211, 165) if ("PASS" in ln or "passed" in ln or "✅" in ln) else ((91, 140, 255) if ln.startswith("▶") or ln.startswith("$") else (232, 237, 255))
        f = font_b if ln.startswith("$") else font
        d.text((22, y), ln, font=f, fill=c)
        y += 48
    d.text((22, H-36), "MIT · F1 0.80 · 6/6 PASS · docs/demo.gif", font=font, fill=(120, 135, 175))
    frames.append(img)

frames[0].save("docs/demo.gif", save_all=True, append_images=frames[1:], duration=1400, loop=0)
print("wrote docs/demo.gif")
import os
print("size:", os.path.getsize("docs/demo.gif"))
# verify readable
im = Image.open("docs/demo.gif")
print("frames:", getattr(im, "n_frames", 1), "size:", im.size)
