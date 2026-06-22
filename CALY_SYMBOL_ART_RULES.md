# Caly symbol art rules (all bands)

Locked standards for every AAC symbol, portrait, game sprite, and animation frame featuring Caly.

## Expression — default is happy

**Caly is warm and smiling in almost every image.** Match the band portrait energy: bright eyes, open friendly mouth, rosy cheeks where the band uses them.

| Rule | Detail |
|------|--------|
| Default | Happy, welcoming, confident — same baseline across Sprout ? Canopy |
| Exceptions only | Symbol id is explicitly an emotion or negative state (see list below) |
| Even “help” / “stop” / “wait” | Caly stays **happy** while acting out the word — never worried, crying, or upset unless the word is about that feeling |
| “hurt” / “sick” | Gentle care face is OK; still kind and hopeful, not grim or scary |

**Non-happy symbol ids (only these may show other expressions):**

`sad`, `mad`, `scared`, `anxious`, `frustrated`, `overwhelmed`, `uncomfortable`, `pain`, `nausea`, `dont-like`, `hurt` (soft concern only — no horror)

All other symbols ? **happy Caly**.

## Hands — always five fingers

| Rule | Detail |
|------|--------|
| Finger count | **Exactly five fingers** on each visible hand, like a typical person |
| Consistency | Same across toddler, child, tween, teen, adult, and caregiver art |
| No shortcuts | No mitten hands, three-finger cartoon hands, or missing digits |
| Gestures | Waving, reaching, palms open, stop palm — all show five distinct fingers when hand is visible |
| Toes | Not required in symbol tiles; if feet are detailed, five toes is fine |

## Band mascot

Each symbol uses **that band’s Caly** (Sprout, Bud, Sprig, Vine, Bloom, Canopy) — see `BAND_ART_MANDATE.md`. Match the band portrait for face, leaves, outfit, and maturity.

## Master prompt suffix (append to every generation)

```
Square 1:1 AAC symbol tile. Caly [NICKNAME] plant girl — match band portrait reference.
Modest clothing per CALY_CHARACTER_DRESS_STANDARDS.md.
Warm HAPPY smile and bright friendly eyes (unless symbol id is a listed emotion exception).
Exactly FIVE fingers on each visible hand, human-like, never three-finger or blob hands.
Chunky #2d6a4f outlines, pastel mint-to-sky gradient background, preschool cartoon polish.
No text, no letters. Original Calyndra IP only.
```

## Per-word notes (updated)

| id | Caly expression / pose |
|----|-------------------------|
| help | Happy Caly reaching one open hand toward viewer (five fingers spread) |
| more | Happy Caly, open palms asking for more |
| play | Happy Caly jumping or holding toy |
| yes | Happy nod, thumbs up |
| no | Caly still **gentle and calm** — soft smile, respectful boundary (not angry) |
| stop | Happy Caly, flat stop palm (five fingers), friendly firmness |
| wait | Happy patient smile, pause gesture |
| sad | Only symbol where tearful/sad face is allowed |
| mad | Frustrated but not scary; still appropriate for kids |
| scared | Worried but safe; never horror |

## QA checklist before shipping a symbol

- [ ] Correct band mascot (folder + outfit + leaf count)
- [ ] Happy face unless symbol id is in the exception list
- [ ] Five fingers on every visible hand
- [ ] Modest clothing, Christian family-safe pose
- [ ] No text in image
- [ ] Copied to `symbols/images/{band}/` and synced to `calyndra-app/assets/symbols/{band}/`

## Regeneration queue

Draft `help-*` and `play-*` assets generated before this rule was locked used “concerned/caring” prompts — **regenerate with happy expression** before installing to production.
