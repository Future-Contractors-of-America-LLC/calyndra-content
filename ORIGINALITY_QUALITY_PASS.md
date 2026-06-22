# Calyndra originality and quality pass

**Purpose:** Every visual, audio, and motion asset in Calyndra must be **original IP** suitable for copyright and trademark registration. No stock photos, scraped web images, or third-party character art.

## Caly mascot (plant Caly)

| Band | Nickname | Pose | Name on art |
|------|----------|------|-------------|
| Toddler | Sprout | `wave` | Caly Sprout |
| Child | Bud | `jump-celebrate` | Caly Bud |
| Teen | Vine | `listen-ear` | Caly Vine |
| Adult | Bloom | `drum-dance` | Caly Bloom |
| Caregiver | Canopy | `listen-ear` + caregiver CSS filter | Caly Canopy |

**Source of truth:** `assets/caly-sprout/poses/*.webp` (generated in-house; see `ARTWORK_ORIGIN_AND_IP.md`).

**Deprecated (do not use in UI):** `assets/caly-teen/`, `assets/caly-adult/` human portraits; legacy `caly_core.png`, `caly_spark.png`, `caly_guide.png` as mascots.

## Symbols

- Path: `assets/symbols/sprout/` and `assets/symbols/quest/`
- Generated via `calyndra-content/scripts/` — not downloaded from the web
- QC: 512px max, PNG + WebP, consistent mint/sky palette

## Videos

- Path: `videos/*.webm`
- Generated via `generate_videos_v5_cartoon.py` with original Caly TTS narration
- QC: 2–5 min target, no stock footage, plant Caly poses only

## Voice

- Azure Neural TTS via `speech_tts.py` personas
- Pre-cache: `pregenerate_caly_voice.py` ? `content/voice/manifest.json`
- No celebrity voice clones; no licensed song lyrics

## Songs and games

- Original lyrics in `content/caly-voice-scripts.json`
- Games use in-repo symbols and mascot poses only
- Age vibe: preschool-show energy (toddler/child), respectful teen, functional adult

## Pre-ship checklist

- [ ] Landing growth cards show correct nickname badge per band
- [ ] No duplicate Sprout pose for Canopy (use `listen-ear`, not `wave`)
- [ ] Bloom uses `drum-dance`, not sleepy/Bud-like pose
- [ ] Demo uses symbol PNGs, not emoji placeholders
- [ ] No `?` mojibake in user-facing strings
- [ ] No broken JS ternaries (`?` corrupted to `-`)
