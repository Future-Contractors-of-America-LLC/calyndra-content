# Calyndra content

AAC vocabulary, symbol art, videos, boards, onboarding, and lessons.

## Symbol pictures

Original PNG illustrations per age-band style (trademark-safe, generated in-repo):

| Style | Age band | Path |
|-------|----------|------|
| **sprout** | Toddler (2–4) | `symbols/images/sprout/{id}.png` |
| **quest** | Child (5–12) | `symbols/images/quest/{id}.png` |
| **spark** | Teen (13–17) | `symbols/images/spark/{id}.png` |
| **core** | Adult / caregiver | `symbols/images/core/{id}.png` |

Each vocabulary JSON entry includes `imageAsset` (Flutter bundle path), e.g. `"imageAsset": "assets/symbols/sprout/help.png"`.

### Regenerate word pictures

```powershell
pip install pillow
python scripts/generate_word_pictures.py
```

Generates **20 toddler-core** + **30 child-expanded** unique PNGs and updates `vocabulary/*.json`. Also copies to `calyndra-mobile-flutter/assets/symbols/`.

## Videos

Short AAC intro clips (5–15 sec WebM) in `videos/`:

| File | Audience |
|------|----------|
| `welcome_aac.webm` | All |
| `toddler_wave.webm` | Toddler |
| `child_quest.webm` | Child |
| `caregiver_assent.webm` | Caregiver |
| `teen_spark.webm` | Teen |

```powershell
pip install pillow imageio imageio-ffmpeg
python scripts/generate_videos.py
```

If WebM encode fails, frame PNG sequences are written as fallback (see script output).

## Governance

- Original artwork only — see [calyndra-ip/IP_ORIGINALITY.md](https://github.com/Future-Contractors-of-America-LLC/calyndra-ip)
- No placeholders in production UI — symbols without `imageAsset` are omitted from picture tiles
