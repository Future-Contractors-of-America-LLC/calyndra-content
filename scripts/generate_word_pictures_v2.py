# -*- coding: utf-8 -*-
"""Age-accurate AAC symbol art v2. See ART_DIRECTION.md."""
from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FLUTTER = ROOT.parent / "calyndra-mobile-flutter"
WEB = ROOT.parent / "calyndra-app"

STYLES = {
    "sprout": {
        "bg1": (180, 230, 200), "bg2": (140, 210, 180),
        "primary": (40, 120, 90), "accent": (255, 200, 100),
        "outline": 8, "frame": "round",
    },
    "quest": {
        "bg1": (220, 190, 120), "bg2": (180, 140, 80),
        "primary": (60, 90, 50), "accent": (255, 220, 80),
        "outline": 6, "frame": "storybook",
    },
    "spark": {
        "bg1": (30, 35, 45), "bg2": (20, 22, 30),
        "primary": (124, 252, 0), "accent": (255, 60, 180),
        "outline": 5, "frame": "neon",
    },
    "core": {
        "bg1": (240, 244, 248), "bg2": (220, 226, 234),
        "primary": (50, 65, 85), "accent": (70, 130, 200),
        "outline": 3, "frame": "hud",
    },
}

TODDLER_EXTRA = [
    ("water", "core", "water drop"), ("milk", "routine", "milk carton"), ("juice", "routine", "juice box"),
    ("apple", "routine", "red apple"), ("cookie", "routine", "cookie"), ("dog", "animals", "friendly dog"),
    ("cat", "animals", "friendly cat"), ("ball", "activities", "play ball"), ("book", "activities", "picture book"),
    ("car", "places", "small car"), ("bus", "places", "school bus"), ("shoe", "routine", "sneaker"),
    ("wash", "routine", "soap bubbles"), ("open", "core", "open door"), ("close", "core", "closed door"),
    ("again", "core", "repeat arrow"), ("please", "social", "please hands"), ("love", "feelings", "heart"),
    ("mommy", "social", "mother figure"), ("daddy", "social", "father figure"), ("look", "core", "eyes looking"),
    ("listen", "core", "ear"), ("big", "core", "large shape"), ("little", "core", "small shape"),
    ("wet", "sensory", "water splash"), ("dry", "sensory", "towel"), ("hot", "sensory", "steam"),
    ("cold", "sensory", "snowflake"), ("clean", "routine", "sparkle clean"), ("dirty", "routine", "mud spot"),
    ("friend", "social", "two kids"), ("blanket", "routine", "soft blanket"), ("toy", "activities", "teddy"),
]

CHILD_EXTRA = [
    ("water", "core"), ("computer", "activities"), ("phone", "activities"), ("email", "activities"),
    ("work", "places"), ("store", "places"), ("park", "places"), ("doctor", "places"),
    ("nurse", "people"), ("teacher", "people"), ("grandma", "social"), ("grandpa", "social"),
    ("baby", "social"), ("brother", "social"), ("sister", "social"), ("pet", "social"),
    ("walk", "activities"), ("run", "activities"), ("swim", "activities"), ("dance", "activities"),
    ("sing", "activities"), ("write", "activities"), ("think", "feelings"), ("remember", "core"),
    ("forget", "core"), ("try", "core"), ("win", "social"), ("lose", "social"),
    ("win", "social"), ("team", "social"), ("alone", "social"), ("together", "social"),
    ("fast", "sensory"), ("slow", "sensory"), ("first", "core"), ("last", "core"),
    ("morning", "routine"), ("night", "routine"), ("today", "core"), ("tomorrow", "core"),
    ("yesterday", "core"), ("money", "functional"), ("pay", "functional"), ("buy", "functional"),
    ("sell", "functional"), ("job", "functional"), ("meeting", "functional"), ("schedule", "functional"),
    ("calendar", "functional"), ("alarm", "routine"), ("message", "functional"), ("call", "functional"),
    ("video", "activities"), ("photo", "activities"), ("map", "functional"), ("directions", "functional"),
    ("left", "core"), ("right", "core"), ("forward", "core"), ("backward", "core"),
]


def gradient_bg(size: int, c1, c2) -> Image.Image:
    img = Image.new("RGB", (size, size), c1)
    d = ImageDraw.Draw(img)
    for y in range(size):
        t = y / size
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        d.line([(0, y), (size, y)], fill=(r, g, b))
    return img.convert("RGBA")


def draw_frame(d: ImageDraw.ImageDraw, style: dict, size: int):
    frame = style["frame"]
    p, a = style["primary"], style["accent"]
    margin = 16
    if frame == "round":
        d.rounded_rectangle((margin, margin, size - margin, size - margin), radius=48, outline=p, width=style["outline"])
        d.ellipse((size - 70, 20, size - 30, 60), fill=a)
    elif frame == "storybook":
        d.rounded_rectangle((margin, margin, size - margin, size - margin), radius=12, outline=p, width=style["outline"])
        for x, y in [(margin + 10, margin + 10), (size - margin - 30, margin + 10)]:
            d.polygon([(x, y), (x + 20, y), (x + 10, y + 18)], fill=a)
    elif frame == "neon":
        d.rectangle((margin, margin, size - margin, size - margin), outline=p, width=style["outline"])
        d.line((margin, margin, size - margin, size - margin), fill=a, width=3)
        d.line((size - margin, margin, margin, size - margin), fill=a, width=2)
    else:
        d.rectangle((margin, margin, size - margin, size - margin), outline=p, width=style["outline"])


def draw_icon(d: ImageDraw.ImageDraw, sym_id: str, style: dict, cx: int, cy: int, s: int):
    p, a, lw = style["primary"], style["accent"], style["outline"]
    sid = sym_id.replace("-", "_")

    def hand():
        d.ellipse((cx - s, cy - s // 2, cx + s, cy + s), fill=a, outline=p, width=lw)
        for ox in (-s // 2, 0, s // 2):
            d.rounded_rectangle((cx + ox - s // 6, cy - s, cx + ox + s // 6, cy - s // 3), radius=6, fill=a, outline=p, width=2)

    def face_happy():
        d.ellipse((cx - s, cy - s, cx + s, cy + s), fill=a, outline=p, width=lw)
        d.arc((cx - s // 2, cy - s // 4, cx + s // 2, cy + s // 2), 200, 340, fill=p, width=lw)
        d.ellipse((cx - s // 3, cy - s // 4, cx - s // 6, cy - s // 8), fill=p)
        d.ellipse((cx + s // 6, cy - s // 4, cx + s // 3, cy - s // 8), fill=p)

    icons = {
        "help": hand, "happy": face_happy, "love": lambda: d.polygon(
            [(cx, cy + s // 2), (cx - s, cy - s // 4), (cx, cy - s // 2), (cx + s, cy - s // 4)], fill=a, outline=p, width=lw),
        "heart": lambda: d.polygon(
            [(cx, cy + s // 2), (cx - s, cy - s // 4), (cx, cy - s // 2), (cx + s, cy - s // 4)], fill=a, outline=p, width=lw),
        "water": lambda: d.polygon([(cx, cy - s), (cx + s // 2, cy), (cx, cy + s), (cx - s // 2, cy)], fill=a, outline=p, width=lw),
        "dog": lambda: (d.ellipse((cx - s, cy - s // 2, cx + s, cy + s), fill=a, outline=p, width=lw),
                        d.polygon([(cx + s // 2, cy - s // 2), (cx + s, cy - s), (cx + s // 3, cy - s // 3)], fill=a)),
        "school": lambda: (d.rectangle((cx - s, cy - s // 4, cx + s, cy + s), fill=p),
                           d.polygon([(cx - s - 10, cy - s // 4), (cx, cy - s), (cx + s + 10, cy - s // 4)], fill=a)),
    }
    if sid in icons:
        icons[sid]()
    elif sid in ("yes",):
        d.line((cx - s, cy, cx - s // 4, cy + s // 2), fill=p, width=lw + 2)
        d.line((cx - s // 4, cy + s // 2, cx + s, cy - s // 2), fill=p, width=lw + 2)
    elif sid in ("no",):
        d.line((cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2), fill=a, width=lw + 2)
        d.line((cx + s // 2, cy - s // 2, cx - s // 2, cy + s // 2), fill=a, width=lw + 2)
    elif sid in ("more",):
        d.line((cx - s // 2, cy, cx + s // 2, cy), fill=p, width=lw + 3)
        d.line((cx, cy - s // 2, cx, cy + s // 2), fill=p, width=lw + 3)
    elif sid in ("stop",):
        d.regular_polygon((cx, cy, s), 8, fill=a, outline=p, width=lw)
    elif sid in ("go",):
        d.polygon([(cx - s // 2, cy - s // 2), (cx + s // 2, cy), (cx - s // 2, cy + s // 2)], fill=a, outline=p, width=lw)
    elif sid in ("home",):
        d.polygon([(cx, cy - s), (cx - s, cy), (cx + s, cy)], fill=a, outline=p, width=lw)
        d.rectangle((cx - s // 2, cy, cx + s // 2, cy + s), fill=p)
    else:
        d.ellipse((cx - s, cy - s, cx + s, cy + s), fill=a, outline=p, width=lw)
        label = sym_id.replace("-", " ")[:6]
        try:
            d.text((cx - s // 2, cy - 8), label, fill=p)
        except Exception:
            pass


def render(sym_id: str, style_name: str, size: int = 512) -> Image.Image:
    st = STYLES[style_name]
    img = gradient_bg(size, st["bg1"], st["bg2"])
    d = ImageDraw.Draw(img)
    draw_frame(d, st, size)
    draw_icon(d, sym_id, st, size // 2, size // 2 + 10, size // 5)
    if style_name == "sprout":
        img = img.filter(ImageFilter.SMOOTH_MORE)
    return img


def ensure_vocab_extensions():
    toddler_path = ROOT / "vocabulary" / "toddler-core.json"
    child_path = ROOT / "vocabulary" / "child-expanded.json"
    toddler = json.loads(toddler_path.read_text(encoding="utf-8"))
    child = json.loads(child_path.read_text(encoding="utf-8"))
    existing_t = {s["id"] for s in toddler["symbols"]}
    for wid, cat, hint in TODDLER_EXTRA:
        if wid not in existing_t:
            toddler["symbols"].append({"id": wid, "label": wid.replace("-", " "), "category": cat, "symbolHint": hint})
    existing_c = {s["id"] for s in child["symbols"]}
    for wid, cat in CHILD_EXTRA:
        if wid not in existing_c:
            child["symbols"].append({"id": wid, "label": wid.replace("-", " "), "category": cat})
    toddler["description"] = f"{len(toddler['symbols'])} toddler AAC symbols with Sprout-style original art."
    child["description"] = f"{len(child['symbols'])} child AAC symbols with Quest-style original art."
    toddler_path.write_text(json.dumps(toddler, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    child_path.write_text(json.dumps(child, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return toddler, child


def generate_set(vocab: dict, style: str) -> int:
    count = 0
    for sym in vocab["symbols"]:
        sid = sym["id"]
        img = render(sid, style)
        rel_content = f"symbols/images/{style}/{sid}.png"
        rel_bundle = f"assets/symbols/{style}/{sid}.png"
        for base, rel in [(ROOT, rel_content), (FLUTTER, rel_bundle), (WEB, rel_bundle)]:
            out = base / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            img.save(out, "PNG")
        sym["imageAsset"] = rel_bundle
        count += 1
    return count


def main():
    print("Calyndra symbol art v2...")
    toddler_path = ROOT / "vocabulary" / "toddler-core.json"
    child_path = ROOT / "vocabulary" / "child-expanded.json"
    toddler, child = ensure_vocab_extensions()
    n1 = generate_set(toddler, "sprout")
    n2 = generate_set(child, "quest")
    # spark/core copies for teen/adult paths
    for style in ("spark", "core"):
        for sym in child["symbols"][:40]:
            img = render(sym["id"], style)
            for base in (FLUTTER, WEB):
                out = base / f"assets/symbols/{style}/{sym['id']}.png"
                out.parent.mkdir(parents=True, exist_ok=True)
                img.save(out, "PNG")
    toddler_path.write_text(json.dumps(toddler, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    child_path.write_text(json.dumps(child, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for name in ("toddler-core.json", "child-expanded.json"):
        src = ROOT / "vocabulary" / name
        shutil.copy(src, FLUTTER / "assets" / "vocabulary" / name)
        shutil.copy(src, WEB / "content" / name)
    print(f"Done: {n1} sprout + {n2} quest symbols. Toddler total={len(toddler['symbols'])}, Child total={len(child['symbols'])}")


if __name__ == "__main__":
    main()
