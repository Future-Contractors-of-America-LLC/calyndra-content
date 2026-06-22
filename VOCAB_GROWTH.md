# Age-band vocabulary growth

Vocabulary and phrases **grow with each age band**. Rebuild with:

`python calyndra-content/scripts/build_band_vocabulary.py`

| Band | Ages | Words | Phrases | Mascot | File |
|------|------|-------|---------|--------|------|
| Toddler | 2-4 | 53 | 12 short | Sprout | `toddler-core.json` |
| Child | 5-8 | 76 | 15 | Bud | `child-vocab.json` |
| Tween | 9-12 | 142 | 12 | Sprig | `tween-vocab.json` |
| Teen | 13-17 | 179 | 12 | Vine | `teen-vocab.json` |
| Adult | 18+ | 179+ | 10 | Bloom | `adult-vocab.json` |
| Caregiver | — | 26 model words | 10 coaching | Canopy | `caregiver-vocab.json` |

## JSON shape

```json
{
  "symbols": [ { "id", "label", "category", "imageAsset" } ],
  "phrases": [ { "id", "label", "category", "speakText" } ]
}
```

`imageAsset` uses the band folder (`sprout`, `bud`, `sprig`, `vine`, `bloom`, `canopy`). Runtime routing also applies via `caly-band-art.js`.

## Phrases

- Toddler: 1-3 words (`more please`, `help me`)
- Child: short sentences (`Can I have more?`)
- Tween: school/social (`I need help with homework`)
- Teen: autonomy/boundaries (`I'm not comfortable with that`)
- Adult: work/health (`I'd like to schedule a meeting`)
- Caregiver: coaching (`Take your time. I'm listening.`)
