# Calyndra artwork origin and IP

**Status:** locked — all mascot and symbol art is **original Calyndra IP**, generated via the in-house GenerateImage pipeline and symbol scripts. No third-party stock mascots.

## Character bible

One character: **Caly** — an animated growing plant. Age bands use the Sprout pose set with CSS scale/filter; nicknames (Sprout, Bud, Vine, Bloom, Canopy) are growth-stage labels only (see `CALY_CHARACTER_AGING.md`, `ILLUSTRATION_STYLE.md`).

| Asset / path | Role | Origin |
|--------------|------|--------|
| `assets/caly_sprout.png` | Toddler portrait + Sprout pose set basis | GenerateImage, June 2026 |
| `assets/caly-sprout/poses/*.webp` | Animated poses for **all** age bands | GenerateImage pose batch |
| `assets/caly_quest.png` | Legacy child-band alias (plant art) | Early GenerateImage variant |
| `assets/caly_spark.png` | Legacy teen alias (plant art) | Early GenerateImage variant |
| `assets/caly_core.png` | Legacy adult alias (plant art) | Early GenerateImage variant |
| `assets/caly_guide.png` | Legacy caregiver alias (plant art) | Early GenerateImage variant |
| `assets/caly-teen/portrait.png` | **Deprecated** — human portrait experiment, not used in UI | Reverted June 2026 |
| `assets/caly-adult/portrait.png` | **Deprecated** — human portrait experiment, not used in UI | Reverted June 2026 |
| `assets/symbols/sprout/*.png` | Toddler symbol grid | `generate_caly_content_v2.py` + optimize pipeline |
| `assets/symbols/quest/*.png` | Child symbol grid | Same pipeline, child styling |
| `assets/scenes/*.webp` | Play backgrounds | GenerateImage scene batch |
| `assets/brand/calyndra_logo_mark.png` | Product mark | Original FCA/Calyndra design |

## Trademark posture

- **Calyndra™** and **Caly™** are product/character marks used consistently in UI and marketing.
- Band nicknames (Sprout, Bud, Vine, Bloom, Canopy) are optional subtitles under Caly — not separate characters.
- Legacy filenames (Quest, Spark, Core, Guide) remain on disk for backward compatibility.
- All new art must append the master prompt suffix from `ILLUSTRATION_STYLE.md`.

## WebP siblings

Run `scripts/optimize_symbol_assets.py` after adding PNGs. Frontend loads WebP with PNG fallback via `caly-assets.js`.

## Registry

Machine-readable list: `caly_character_registry.json`.
