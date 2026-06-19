"""Generate original AAC symbol PNGs per age-band style. Run: python scripts/generate_word_pictures.py"""
from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FLUTTER = ROOT.parent / "calyndra-mobile-flutter"
OUT = ROOT / "symbols" / "images"
FLUTTER_SYM = FLUTTER / "assets" / "symbols"

STYLES = {
    "sprout": {"bg": (210, 240, 220, 255), "primary": (80, 170, 130), "accent": (255, 210, 120), "line": 6},
    "quest": {"bg": (190, 210, 150, 255), "primary": (70, 120, 80), "accent": (255, 200, 80), "line": 5},
    "spark": {"bg": (22, 28, 48, 255), "primary": (0, 255, 200), "accent": (255, 60, 160), "line": 4},
    "core": {"bg": (248, 250, 252, 255), "primary": (60, 80, 110), "accent": (90, 140, 200), "line": 3},
}

BAND_STYLE = {"toddler": "sprout", "child": "quest", "teen": "spark", "adult": "core", "caregiver": "core"}


def draw_round_rect(d: ImageDraw.ImageDraw, xy, r, fill, outline=None, w=2):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)


def draw_hand(d, cx, cy, s, color):
    d.ellipse((cx - s, cy - s, cx + s, cy + s), fill=color)
    for i, ox in enumerate([-s * 0.6, 0, s * 0.6]):
        d.rounded_rectangle((cx + ox - s * 0.2, cy - s * 1.8, cx + ox + s * 0.2, cy - s * 0.5), radius=8, fill=color)


def draw_house(d, cx, cy, s, color, roof):
    d.polygon([(cx, cy - s), (cx - s, cy), (cx + s, cy)], fill=roof)
    draw_round_rect(d, (cx - s * 0.8, cy, cx + s * 0.8, cy + s * 1.2), 8, color)


def draw_symbol(d: ImageDraw.ImageDraw, sym_id: str, style: dict, w: int, h: int):
    cx, cy = w // 2, h // 2 - 10
    s = min(w, h) // 5
    p, a, lw = style["primary"], style["accent"], style["line"]
    sid = sym_id.replace("-", "_")

    if sid == "help":
        draw_hand(d, cx, cy, s, p)
    elif sid == "more":
        d.line((cx - s, cy, cx + s, cy), fill=p, width=lw + 2)
        d.line((cx, cy - s, cx, cy + s), fill=p, width=lw + 2)
    elif sid == "stop":
        d.regular_polygon((cx, cy, s * 1.2), 8, fill=a, outline=p, width=lw)
    elif sid == "yes":
        d.line((cx - s, cy, cx - s * 0.2, cy + s * 0.8), fill=p, width=lw + 2)
        d.line((cx - s * 0.2, cy + s * 0.8, cx + s, cy - s * 0.6), fill=p, width=lw + 2)
    elif sid == "no":
        d.line((cx - s, cy - s, cx + s, cy + s), fill=a, width=lw + 2)
        d.line((cx + s, cy - s, cx - s, cy + s), fill=a, width=lw + 2)
    elif sid == "bathroom":
        draw_round_rect(d, (cx - s, cy - s * 0.3, cx + s, cy + s), 12, (240, 240, 245), p, lw)
        d.ellipse((cx - s * 0.7, cy - s * 0.8, cx + s * 0.7, cy + s * 0.2), outline=p, width=lw)
    elif sid == "eat":
        d.polygon([(cx - s * 0.2, cy - s), (cx + s * 0.2, cy - s), (cx, cy + s)], fill=p)
        d.rectangle((cx + s * 0.5, cy - s * 1.2, cx + s * 0.7, cy + s * 0.5), fill=a)
    elif sid == "drink":
        d.polygon([(cx - s * 0.8, cy - s), (cx + s * 0.8, cy - s), (cx + s * 0.5, cy + s), (cx - s * 0.5, cy + s)], fill=p)
        d.line((cx + s, cy - s * 1.2, cx + s * 1.3, cy - s * 1.8), fill=a, width=lw)
    elif sid in ("happy",):
        d.arc((cx - s, cy - s, cx + s, cy + s), 200, 340, fill=p, width=lw + 2)
        d.ellipse((cx - s * 0.4, cy - s * 0.2, cx - s * 0.1, cy + s * 0.1), fill=p)
        d.ellipse((cx + s * 0.1, cy - s * 0.2, cx + s * 0.4, cy + s * 0.1), fill=p)
    elif sid in ("sad",):
        d.arc((cx - s, cy, cx + s, cy + s * 1.5), 20, 160, fill=p, width=lw + 2)
        d.ellipse((cx - s * 0.4, cy - s * 0.2, cx - s * 0.1, cy + s * 0.1), fill=p)
        d.ellipse((cx + s * 0.1, cy - s * 0.2, cx + s * 0.4, cy + s * 0.1), fill=p)
    elif sid == "all_done":
        d.line((cx - s, cy, cx - s * 0.1, cy + s * 0.7), fill=p, width=lw + 2)
        d.line((cx - s * 0.1, cy + s * 0.7, cx + s, cy - s * 0.5), fill=p, width=lw + 2)
    elif sid == "go":
        d.polygon([(cx - s * 0.5, cy - s), (cx + s, cy), (cx - s * 0.5, cy + s)], fill=a)
    elif sid == "wait":
        d.polygon([(cx, cy - s), (cx + s * 0.6, cy + s), (cx - s * 0.6, cy + s)], outline=p, width=lw)
        d.line((cx, cy - s * 0.3, cx, cy + s * 0.5), fill=p, width=lw)
    elif sid == "home":
        draw_house(d, cx, cy, s, p, a)
    elif sid == "play":
        d.ellipse((cx - s, cy - s * 0.5, cx + s, cy + s * 0.8), fill=a, outline=p, width=lw)
    elif sid == "hug":
        d.arc((cx - s * 1.2, cy - s, cx, cy + s), 270, 90, fill=p, width=lw + 2)
        d.arc((cx, cy - s, cx + s * 1.2, cy + s), 90, 270, fill=p, width=lw + 2)
    elif sid == "hurt":
        draw_round_rect(d, (cx - s * 0.3, cy - s * 0.8, cx + s * 0.3, cy + s * 0.8), 6, (255, 255, 255), p, lw)
        d.line((cx - s * 0.15, cy - s * 0.3, cx + s * 0.15, cy + s * 0.3), fill=a, width=lw)
    elif sid == "sleep":
        d.polygon([(cx - s, cy + s * 0.5), (cx + s, cy + s * 0.5), (cx + s * 0.5, cy - s)], fill=p)
        d.ellipse((cx + s * 0.5, cy - s * 1.5, cx + s * 1.3, cy - s * 0.5), fill=a)
    elif sid == "up":
        d.polygon([(cx, cy - s * 1.2), (cx - s * 0.7, cy), (cx + s * 0.7, cy)], fill=p)
    elif sid == "down":
        d.polygon([(cx, cy + s * 1.2), (cx - s * 0.7, cy), (cx + s * 0.7, cy)], fill=p)
    elif sid == "school":
        draw_round_rect(d, (cx - s, cy - s * 0.5, cx + s, cy + s), 4, p)
        d.polygon([(cx - s * 1.1, cy - s * 0.5), (cx, cy - s * 1.3), (cx + s * 1.1, cy - s * 0.5)], fill=a)
    elif sid == "friend":
        d.ellipse((cx - s * 0.9, cy - s * 0.2, cx - s * 0.1, cy + s * 0.6), fill=p)
        d.ellipse((cx + s * 0.1, cy - s * 0.2, cx + s * 0.9, cy + s * 0.6), fill=a)
    elif sid == "read":
        draw_round_rect(d, (cx - s, cy - s * 0.8, cx + s, cy + s * 0.8), 4, (255, 255, 255), p, lw)
        d.line((cx, cy - s * 0.8, cx, cy + s * 0.8), fill=p, width=lw)
    elif sid == "music":
        d.ellipse((cx - s * 0.8, cy, cx - s * 0.2, cy + s * 0.6), fill=p)
        d.rectangle((cx - s * 0.2, cy - s, cx + s * 0.2, cy + s * 0.3), fill=p)
    elif sid == "break":
        d.rectangle((cx - s * 0.8, cy - s, cx - s * 0.3, cy + s), fill=p)
        d.rectangle((cx + s * 0.3, cy - s, cx + s * 0.8, cy + s), fill=p)
    elif sid == "quiet":
        d.ellipse((cx - s, cy - s * 0.5, cx + s, cy + s), fill=p)
        d.line((cx - s * 0.5, cy + s * 0.2, cx + s * 0.5, cy + s * 0.2), fill=(255, 255, 255), width=lw)
    elif sid == "hot":
        d.polygon([(cx, cy - s), (cx + s * 0.3, cy), (cx + s * 0.8, cy - s * 0.3),
                   (cx + s * 0.5, cy + s * 0.5), (cx + s, cy + s), (cx, cy + s * 0.6),
                   (cx - s, cy + s), (cx - s * 0.5, cy + s * 0.5), (cx - s * 0.8, cy - s * 0.3),
                   (cx - s * 0.3, cy)], fill=a)
    elif sid == "cold":
        for i in range(6):
            ang = i * math.pi / 3
            x2 = cx + math.cos(ang) * s
            y2 = cy + math.sin(ang) * s
            d.line((cx, cy, x2, y2), fill=p, width=lw)
    elif sid in ("want", "need"):
        d.polygon([(cx, cy - s), (cx + s * 0.3, cy - s * 0.2), (cx + s, cy),
                   (cx + s * 0.2, cy + s * 0.3), (cx + s * 0.4, cy + s),
                   (cx, cy + s * 0.5), (cx - s * 0.4, cy + s), (cx - s * 0.2, cy + s * 0.3),
                   (cx - s, cy), (cx - s * 0.3, cy - s * 0.2)], fill=a if sid == "want" else p)
    elif sid in ("where", "what", "who", "when", "why"):
        d.ellipse((cx - s, cy - s, cx + s, cy + s), outline=p, width=lw + 2)
        d.text((cx - 8, cy - 14), "?", fill=p)
    else:
        # Generic labeled circle for remaining words
        d.ellipse((cx - s, cy - s, cx + s, cy + s), fill=a, outline=p, width=lw)
        label = sym_id.replace("-", " ")[:8]
        d.text((cx - s * 0.6, cy - 8), label, fill=p)


def render_symbol(sym_id: str, style_name: str, size: int = 256) -> Image.Image:
    style = STYLES[style_name]
    img = Image.new("RGBA", (size, size), style["bg"])
    d = ImageDraw.Draw(img)
    draw_round_rect(d, (8, 8, size - 8, size - 8), 24, (255, 255, 255, 40))
    draw_symbol(d, sym_id, style, size, size)
    return img


def asset_path(style: str, sym_id: str, for_flutter: bool = False) -> str:
    if for_flutter:
        return f"assets/symbols/{style}/{sym_id}.png"
    return f"symbols/images/{style}/{sym_id}.png"


def generate_for_vocab(vocab_file: Path, style: str, limit: int | None = None) -> int:
    data = json.loads(vocab_file.read_text(encoding="utf-8"))
    count = 0
    for i, sym in enumerate(data["symbols"]):
        if limit is not None and i >= limit:
            break
        sid = sym["id"]
        img = render_symbol(sid, style)
        rel = asset_path(style, sid, False)
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out, "PNG")
        flutter_out = FLUTTER_SYM / style / f"{sid}.png"
        flutter_out.parent.mkdir(parents=True, exist_ok=True)
        img.save(flutter_out, "PNG")
        sym["imageAsset"] = asset_path(style, sid, True)
        count += 1
        print(f"  {rel}")
    vocab_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    flutter_vocab = FLUTTER / "assets" / "vocabulary" / vocab_file.name
    flutter_vocab.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(vocab_file, flutter_vocab)
    return count


def main() -> None:
    print("Generating AAC word pictures...")
    n1 = generate_for_vocab(ROOT / "vocabulary" / "toddler-core.json", "sprout", limit=20)
    n2 = generate_for_vocab(ROOT / "vocabulary" / "child-expanded.json", "quest", limit=30)
    print(f"Done: {n1} toddler + {n2} child = {n1 + n2} PNGs")


if __name__ == "__main__":
    main()
