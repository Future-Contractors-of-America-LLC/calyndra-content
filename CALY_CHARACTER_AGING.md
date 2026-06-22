# Caly character aging — one growing plant friend

**Status:** locked — **Caly** is one animated plant character who matures across age bands. Band nicknames are optional growth-stage labels, not separate mascots.

## Core principle

- **Primary name in UI:** always **Caly**.
- **Gender:** Caly is **female** at every age band — feminine features, voice, and presence throughout.
- **Nicknames (optional subtitle):** plant-themed growth labels per band — see table below.
- **Art:** Distinct band portraits in `assets/caly-bands/` — each stage is **progressively leaner, taller, and more mature** (Sprout ? Canopy) while staying fun.
- **Palette:** mint `#b8f0d8`, sky `#7ec8ff`, chunky `#2d6a4f` outlines, pastel cream backgrounds.

## Nicknames by band

| Band | Nickname | Meaning | Default pose |
|------|----------|---------|--------------|
| Toddler | **Sprout** | First green shoot | wave |
| Child | **Bud** | Opening leaf bud | jump-celebrate |
| Teen | **Vine** | Climbing growth, slightly taller | listen-ear |
| Adult | **Bloom** | Mature flowering plant | sleepy |
| Caregiver | **Canopy** | Shelter shade for others | wave |

Display pattern: **Caly (Sprout)**, **Caly (Bud)**, etc. — or title **Caly** with nickname in subtitle.

## Pose evolution by band

| Band | CSS scale | Filter | Voice arc |
|------|-----------|--------|-----------|
| Toddler | 0.92 | none | AriaNeural, slowest, sing-song |
| Child | 1.0 | saturate(1.05) | AnaNeural, cheerful |
| Teen | 1.06 | saturate(0.95) brightness(1.02) | JennyNeural, respectful |
| Adult | 1.1 | saturate(0.9) brightness(1.04) | GuyNeural, calm |
| Caregiver | 1.08 | saturate(0.92) brightness(1.03) | GuyNeural, friendly professional |

Caregiver and adult share the **same voice base** (GuyNeural). Caregiver SSML uses slower rate and friendly style for warm professional tone.

## Deprecated (do not use in UI)

- Human portrait assets under `assets/caly-teen/` and `assets/caly-adult/` (June 2026 experiment — reverted).
- Treating Quest / Spark / Core / Guide as separate characters (legacy filenames only).

## Implementation

- `caly-mascot.js` — `AGE_BANDS`, `displayTitle()`, `headerPortrait()`
- `speech_tts.py` — band labels `Caly-toddler` … `Caly-caregiver` (internal)
- `caly_character_registry.json` — machine-readable asset list + nicknames
