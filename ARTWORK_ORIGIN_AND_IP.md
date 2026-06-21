# Calyndra artwork origin and IP

**Status:** locked — all mascot and symbol art is **original Calyndra IP**, generated via the in-house GenerateImage pipeline and symbol scripts. No third-party stock mascots.

## Character bible

One character: **Caly**. Age bands are derivative variants of the same face, palette, and outline style (see `CALY_CHARACTER_AGING.md`, `ILLUSTRATION_STYLE.md`).

| Asset / path | Role | Origin |
|--------------|------|--------|
| `assets/caly_sprout.png` | Toddler portrait + Sprout pose set basis | GenerateImage, June 2026 |
| `assets/caly-sprout/poses/*.webp` | Toddler/child animated poses | GenerateImage pose batch |
| `assets/caly-teen/portrait.png` | Teen-aged Caly (internal: Caly teen) | GenerateImage, same bible as Sprout, June 2026 |
| `assets/caly-adult/portrait.png` | Adult Caly | GenerateImage, same bible as Sprout, June 2026 |
| `assets/caly_quest.png` | Legacy child-band alias | Early GenerateImage variant; superseded by Sprout poses + CSS |
| `assets/caly_spark.png` | Legacy teen alias | Regenerated from teen portrait lineage, June 2026 |
| `assets/caly_core.png` | Legacy adult alias | Copy of adult portrait, June 2026 |
| `assets/caly_guide.png` | Legacy caregiver alias | Same as adult portrait (caregiver = adult visually), June 2026 |
| `assets/symbols/sprout/*.png` | Toddler symbol grid | `generate_caly_content_v2.py` + optimize pipeline |
| `assets/symbols/quest/*.png` | Child symbol grid | Same pipeline, child styling |
| `assets/scenes/*.webp` | Play backgrounds | GenerateImage scene batch |
| `assets/brand/calyndra_logo_mark.png` | Product mark | Original FCA/Calyndra design |

## Trademark posture

- **Calyndra™** and **Caly™** are product/character marks used consistently in UI and marketing.
- Legacy filenames (Quest, Spark, Core, Guide) remain on disk for backward compatibility but are **not** separate characters in user-facing copy.
- All new art must append the master prompt suffix from `ILLUSTRATION_STYLE.md`.

## WebP siblings

Run `scripts/optimize_symbol_assets.py` after adding PNGs. Frontend loads WebP with PNG fallback via `caly-assets.js`.

## Registry

Machine-readable list: `caly_character_registry.json` (replaces `sprout_theme_registry.json`).
