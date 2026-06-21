# Caly character aging — one friend, every life stage

**Status:** locked — Caly Sprout/Quest/Spark/Core are **not separate characters**. One Caly, same art basis, maturing like a person ages.

## Core principle

- **Name in UI:** always **Caly** (caregiver mode may use professional tone but same persona).
- **Age bands** change voice, text tone, and a slightly matured art variant of the **same** character.
- **Palette stays constant:** mint `#b8f0d8`, sky `#7ec8ff`, chunky `#2d6a4f` outlines, pastel cream backgrounds.
- **Never** market or label separate mascots (Quest, Spark, etc.) as different people.

## Pose evolution by band

| Band | Pose feel | Art source (current) | Voice arc |
|------|-----------|----------------------|-----------|
| Toddler | Smaller, rounder | Sprout poses @ CSS scale 0.92 | AriaNeural, slowest, sing-song |
| Child | Taller, bouncy | Sprout poses @ scale 1.0 | AnaNeural, cheerful |
| Teen | Taller, direct gaze | Sprout poses @ scale 1.06 + filter | JennyNeural, respectful |
| Adult | Calm guide look | Sprout poses @ scale 1.1 + filter | GuyNeural, steady |
| Caregiver | Professional portrait | `caly_guide.png` | JaneNeural, empathetic |

Until band-specific illustrated pose sets ship, use existing Sprout poses with CSS `transform: scale()` and subtle `filter` per band. Document interim styling in `sprout_theme_registry.json` under `agingBands`.

## Visual rules (unchanged from Sprout bible)

- Chunky rounded shapes, big friendly eyes, soft gradients, warm storybook lighting.
- Thick dark-green outlines on all Caly art.
- Lucas & Friends / Super Simple Songs *energy* — **original Calyndra IP only**.

## Master prompt suffix

Append to every Caly generation (from `ILLUSTRATION_STYLE.md`):

> Preschool-to-adult educational cartoon illustration for an AAC app. Same recurring character "Caly" at different life stages — recognizably the same person. Chunky rounded shapes, pastel mint and sky-blue palette, thick dark-green outlines, friendly big-eyed cartoon style, soft gradients, warm storybook lighting. Square 1:1, soft mint-to-sky gradient background. Original Calyndra art only.

## Pose inventory (base set)

| Pose | Path | Used in |
|------|------|---------|
| wave | `assets/caly-sprout/poses/wave.webp` | Landing, Play intro, default |
| jump-celebrate | `assets/caly-sprout/poses/jump-celebrate.webp` | Wins, celebrate |
| peek-hide | `assets/caly-sprout/poses/peek-hide.webp` | Peek-a-Caly |
| listen-ear | `assets/caly-sprout/poses/listen-ear.webp` | Bubble Pop, landing |
| drum-dance | `assets/caly-sprout/poses/drum-dance.webp` | Song Circle |
| sleepy | `assets/caly-sprout/poses/sleepy.webp` | Bedtime routines |

PNG fallbacks: same paths with `.png` extension.

## Scene backgrounds

| Scene | Path | Used in |
|-------|------|---------|
| sunny meadow | `assets/scenes/sunny-meadow-stage.webp` | Toddler/child play |
| colorful playroom | `assets/scenes/colorful-playroom-stage.webp` | Teen play surfaces |

## Implementation

- `caly-mascot.js` — `AGE_BANDS` + `headerPortrait()` for app shell.
- `speech_tts.py` — band labels `Caly-toddler`, `Caly-child`, etc. (internal only).
- `CALY_INSTRUCTIONS.md` — one character arc in chat/voice copy.
- Marketing `index.html` — "Caly grows with you" section uses aged CSS variants.

## Registry

Machine-readable asset list: `sprout_theme_registry.json` (includes `agingBands`).

## Deprecated naming

Do **not** use in user-facing copy: Caly Sprout, Caly Quest, Caly Spark, Caly Core as separate characters. Legacy asset filenames (`caly_quest.png`, etc.) remain on disk but are not primary UI sources.
