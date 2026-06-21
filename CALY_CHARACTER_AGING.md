# Caly character aging — one friend, every life stage

**Status:** locked — Caly is **one character** who ages. Sprout/Quest/Spark/Core/Guide are legacy filenames only.

## Core principle

- **Name in UI:** always **Caly**.
- **Age bands** change voice, text tone, and art variant of the **same** character.
- **Palette:** mint `#b8f0d8`, sky `#7ec8ff`, chunky `#2d6a4f` outlines, pastel cream backgrounds.

## Pose evolution by band

| Band | Pose feel | Art source | Voice arc |
|------|-----------|------------|-----------|
| Toddler | Smaller, rounder | Sprout poses @ CSS scale 0.92 | AriaNeural, slowest, sing-song |
| Child | Taller, bouncy | Sprout poses @ scale 1.0 | AnaNeural, cheerful |
| Teen | Taller, direct gaze | **`assets/caly-teen/portrait.png`** (Caly teen) | JennyNeural, respectful |
| Adult | Calm guide look | **`assets/caly-adult/portrait.png`** | GuyNeural, calm |
| Caregiver | Same as adult | **`assets/caly-adult/portrait.png`** | GuyNeural, friendly professional |

Caregiver and adult share the **same portrait** and **same voice base** (GuyNeural). Caregiver SSML uses slower rate and friendly style for warm professional tone.

## Implementation

- `caly-mascot.js` — `AGE_BANDS` + `headerPortrait()`
- `speech_tts.py` — band labels `Caly-toddler` … `Caly-caregiver` (internal)
- `caly_character_registry.json` — machine-readable asset list

## Deprecated naming

Do **not** use in user-facing copy: Caly Sprout, Caly Quest, Caly Spark, Caly Core as separate characters.
