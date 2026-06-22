# Calyndra artwork origin and IP

**Honest status (June 2026):** Canonical band portraits are **original plant Caly** art in `assets/caly-bands/`. Legacy files listed under quarantine must not ship in UI.

## Canonical band portraits (trademark-ready)

| Band | Nickname | File | Origin |
|------|----------|------|--------|
| Toddler | Sprout | `assets/caly-bands/sprout.png` | GenerateImage, in-house, name art on image |
| Child | Bud | `assets/caly-bands/bud.png` | GenerateImage, in-house, name art on image |
| Teen | Vine | `assets/caly-bands/vine.png` | GenerateImage, in-house, name art on image |
| Adult | Bloom | `assets/caly-bands/bloom.png` | GenerateImage, in-house, name art on image |
| Caregiver | Canopy | `assets/caly-bands/canopy.png` | GenerateImage, in-house, name art on image |

One character **Caly** — a growing plant. Nicknames are growth-stage labels baked into each portrait.

## Animation poses (toddler base)

| Path | Role |
|------|------|
| `assets/caly-sprout/poses/*.webp` | Interactive poses for games/show (toddler band; band-specific pose sets TBD) |
| `assets/caly_sprout.png` | Early toddler reference still used as fallback |

## Symbols and scenes

| Path | Origin |
|------|--------|
| `assets/symbols/sprout/*.png` | `generate_caly_content_v2.py` + optimize pipeline |
| `assets/symbols/quest/*.png` | Same pipeline, child styling |
| `assets/scenes/*.webp` | GenerateImage scene batch |

## Quarantined — never use in UI

See `calyndra-app/assets/_quarantined/README.md`:

- `caly_quest.png` (fox — wrong species)
- `caly_spark.png`, `caly_core.png`, `caly_guide.png` (placeholders)
- `caly-teen/portrait.png`, `caly-adult/portrait.png` (human experiment)

## Trademark posture

- **Calyndra™** and **Caly™** — product/character marks
- Band nicknames on portraits: Sprout, Bud, Vine, Bloom, Canopy
- All new art: append master prompt suffix from `ILLUSTRATION_STYLE.md`

Registry: `caly_character_registry.json`
