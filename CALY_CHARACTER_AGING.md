# Caly character aging ù one growing plant friend

**Status:** locked ù **Caly** is one animated plant character who matures across age bands. Band nicknames are optional growth-stage labels, not separate mascots.

## Core principle

- **Primary name in UI:** always **Caly**.
- **Gender:** Caly is **female** at every age band ù feminine features, voice, and presence throughout.
- **Values:** Calyndra reflects **Christian family values** ù modest dress, wholesome poses, no sexualized design.
- **Clothing:** Every band portrait shows Caly **fully clothed** (romper/overalls ? tee & shorts ? tee & patterned shorts ? hoodie & pants ? cardigan & trousers ? modest dress & cardigan).
- **Nicknames (optional subtitle):** plant-themed growth labels per band ù see table below.
- **Art:** Distinct band portraits in `assets/caly-bands/` ù each stage is **progressively leaner, taller, and more mature** (Sprout ? Canopy) while staying fun. **Leaf count increases** from Bud (2 leaves) through Sprig (3ù4 leaves + tendrils) to Vine (full vine growth).
- **Palette:** mint `#b8f0d8`, sky `#7ec8ff`, soft rose-pink accents per band, chunky `#2d6a4f` outlines, pastel cream backgrounds.

## Nicknames by band

| Band | Ages | Nickname | Meaning | Default pose |
|------|------|----------|---------|--------------|
| Baby | 0ù23 mo | **Seed** | First planted seed ù nursery & landing | wave |
| Toddler | 2ù4 | **Sprout** | First green shoot | wave |
| Child | 5ù8 | **Bud** | Opening leaf bud | jump-celebrate |
| Tween | 9ù12 | **Sprig** | Small stem with more leaves | jump-celebrate |
| Teen | 13ù17 | **Vine** | Climbing growth, taller | listen-ear |
| Adult | 18+ | **Bloom** | Mature flowering plant | sleepy |
| Caregiver | ù | **Canopy** | Shelter shade for others | wave |

Display pattern: **Caly (Sprout)**, **Caly (Bud)**, etc. ù or title **Caly** with nickname in subtitle.

## Pose evolution by band

| Band | CSS scale | Filter | Voice arc |
|------|-----------|--------|-----------|
| Baby | 0.85 | brightness(1.03) saturate(1.08) | AnaNeural, slowest nursery sing-song |
| Toddler | 0.92 | none | AriaNeural, sing-song |
| Child | 1.0 | saturate(1.05) | AnaNeural, cheerful |
| Tween | 1.03 | saturate(1.03) brightness(1.01) | AnaNeural, bridging pace |
| Teen | 1.06 | saturate(0.95) brightness(1.02) | JennyNeural, respectful |
| Adult | 1.1 | saturate(0.9) brightness(1.04) | GuyNeural, calm |
| Caregiver | 1.08 | saturate(0.92) brightness(1.03) | GuyNeural, friendly professional |

Caregiver and adult share the **same voice base** (GuyNeural). Caregiver SSML uses slower rate and friendly style for warm professional tone.

## Seed portrait bootstrap

`assets/caly-bands/seed.png` is the **Caly Seed** band portrait (baby 0ñ23 mo). Until dedicated Seed art is generated, the file may bootstrap from `sprout.png` with a distinct filename for pipeline and CI (`test -f assets/caly-bands/seed.png`). Symbol art for the `seed/` folder bootstraps from `sprout/` via `scripts/sync_band_symbol_dirs.py`.

## Deprecated (do not use in UI)

- Human portrait assets under `assets/caly-teen/` and `assets/caly-adult/` (June 2026 experiment ù reverted).
- Treating Quest / Spark / Core / Guide as separate characters (legacy filenames only).

## Implementation

- `caly-mascot.js` ù `AGE_BANDS`, `displayTitle()`, `headerPortrait()`
- `speech_tts.py` ù band labels `Caly-toddler` ù `Caly-caregiver` (internal)
- `caly_character_registry.json` ù machine-readable asset list + nicknames
