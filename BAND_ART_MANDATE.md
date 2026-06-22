# Caly band art mandate

**One Caly character** matures across age bands. Every visual in a band must use that band's nickname and mascot portrait style.

| Audience | Nickname | Symbol folder | Portrait |
|----------|----------|---------------|----------|
| Toddler (2–4) | Caly Sprout | `assets/symbols/sprout/` | `caly-bands/sprout.png` |
| Child (5–8) | Caly Bud | `assets/symbols/bud/` | `caly-bands/bud.png` |
| Tween (9–12) | Caly Sprig | `assets/symbols/sprig/` | `caly-bands/sprig.png` |
| Teen (13–17) | Caly Vine | `assets/symbols/vine/` | `caly-bands/vine.png` |
| Adult (18+) | Caly Bloom | `assets/symbols/bloom/` | `caly-bands/bloom.png` |
| Caregiver | Caly Canopy | `assets/symbols/canopy/` | `caly-bands/canopy.png` |

## Applies to

- AAC symbol tiles
- Chat bubble visuals
- Play games, Caly Show, video tap-along words
- Routines, sensory boards, therapy modalities
- Cartoons, animations, and games (portrait + symbol paths)

## Implementation

- Runtime routing: `calyndra-app/js/caly-band-art.js` (`applyBandToSymbolSet`, `bandFor`)
- Symbol folders: run `calyndra-content/scripts/sync_band_symbol_dirs.py` to bootstrap missing folders
- **Each band's symbols must be regenerated** with that band's Caly mascot — copied sprout art is wiring only, not final

## Character consistency (all bands)

- **Expression:** Caly is **happy by default** in every picture, video, and game frame unless the content explicitly calls for another emotion (sad, mad, scared, etc.). Functional words like help, more, play, stop, and wait still show a warm smile.
- **Hands:** **Five fingers** on each visible hand at every age band — same anatomy as a typical person. No three-finger cartoon hands.

Full rules: `CALY_SYMBOL_ART_RULES.md`

## Legacy folders (do not use in new content)

- `quest/` ? use `bud/` or `sprig/` by audience
- `spark/` ? use `vine/` (teen) or `bloom/` (adult)
- `core/` ? band-specific folder per audience
