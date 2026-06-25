# -*- coding: utf-8 -*-
"""Animation specialist: eased motion curves and caption compositing."""
from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def smoothstep(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def ease_out_back(t: float) -> float:
    t = max(0.0, min(1.0, t))
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def motion_params(motion: str, t: float, scale_fn) -> tuple[float, int, float]:
    """Return zoom, vertical offset, eased time for motion type."""
    et = smoothstep(t)
    if motion == "bounce":
        wave = math.sin(et * math.pi * 2)
        return 1.0 + 0.035 * wave, int(scale_fn(10) * wave), et
    if motion == "zoom":
        return 1.0 + 0.08 * ease_out_back(et), 0, et
    if motion == "pan":
        return 1.1, int(scale_fn(16) * math.sin(et * math.pi)), et
    if motion == "pulse":
        return 1.0 + 0.06 * math.sin(et * math.pi * 4), 0, et
    if motion == "celebrate":
        return 1.0 + 0.05 * math.sin(et * math.pi * 3), int(scale_fn(8) * math.sin(et * math.pi * 6)), et
    return 1.025, 0, et


def draw_caption_bar(
    canvas: Image.Image,
    caption: str,
    *,
    t: float,
    scale_fn,
    font_loader,
) -> None:
    w, h = canvas.size
    d = ImageDraw.Draw(canvas)
    bar_h = scale_fn(92)
    pad = scale_fn(48)
    gap = scale_fn(28)
    radius = scale_fn(24)
    alpha = int(255 * min(1.0, smoothstep(t * 4)))
    if alpha <= 0:
        return

    bar = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bar)
    fill = (255, 255, 255, int(alpha * 0.94))
    outline = (255, 200, 100, alpha)
    bd.rounded_rectangle((pad, h - bar_h - gap, w - pad, h - gap), radius=radius, fill=fill, outline=outline, width=max(scale_fn(4), 2))
    bar = bar.filter(ImageFilter.GaussianBlur(radius=max(1, scale_fn(1) // 2)))
    canvas.paste(bar, (0, 0), bar)

    d = ImageDraw.Draw(canvas)
    font = font_loader(scale_fn(34))
    tw = d.textlength(caption, font=font)
    tx = (w - tw) / 2
    ty = h - bar_h - scale_fn(2)
    shadow = max(scale_fn(2), 1)
    d.text((tx + shadow, ty + shadow), caption, fill=(30, 40, 50), font=font)
    d.text((tx, ty), caption, fill=(45, 55, 65), font=font)


def draw_celebration_particles(d: ImageDraw.ImageDraw, w: int, h: int, t: float, scale_fn) -> None:
    for i in range(12):
        cx = int(scale_fn(180) + (w - scale_fn(360)) * ((i * 0.11 + t * 0.35) % 1))
        cy = int(scale_fn(70) + scale_fn(50) * math.sin(t * 8 + i * 0.7))
        colors = ["#ff6b6b", "#ffd93d", "#6bcb77", "#74b9ff", "#c084fc"]
        r = scale_fn(5 + (i % 3))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=colors[i % len(colors)])
