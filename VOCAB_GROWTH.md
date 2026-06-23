# Age-band vocabulary growth

Vocabulary and phrases **grow with each age band**. Rebuild with:

`python calyndra-content/scripts/build_band_vocabulary.py`

Outputs per band: combined `{band}-vocab.json`, split `{band}-words.json`, `{band}-phrases.json`.

| Band | Ages | Words | Phrases | Mascot | File |
|------|------|-------|---------|--------|------|
| Baby | 0-23 mo | 40 | 10 nursery | Seed | `baby-vocab.json` |
| Toddler | 2-4 | 70 | 18 short | Sprout | `toddler-core.json` |
| Child | 5-8 | 100 | 20 | Bud | `child-vocab.json` |
| Tween | 9-12 | 160 | 15 | Sprig | `tween-vocab.json` |
| Teen | 13-17 | 200 | 15 | Vine | `teen-vocab.json` |
| Adult | 18+ | 200 | 12 | Bloom | `adult-vocab.json` |
| Caregiver | all ages | 40 model words | 12 coaching | Canopy | caregiver-vocab.json |

## JSON shape

```json
{
  "symbols": [ { "id", "label", "category", "imageAsset" } ],
  "phrases": [ { "id", "label", "category", "speakText" } ]
}
```

`imageAsset` uses the band folder (`seed`, `sprout`, `bud`, `sprig`, `vine`, `bloom`, `canopy`). Runtime routing also applies via `caly-band-art.js`.

## App tabs

The web app loads split files via **Words** and **Phrases** top-level tabs (`baby-words.json`, `toddler-phrases.json`, etc.).

## Phrases

- Baby: nursery (`peek-a-boo`, `night night`)
- Toddler: 1-3 words (`more please`, `help me`)
- Child: short sentences (`Can I have more?`)
- Tween: school/social (`I need help with homework`)
- Teen: autonomy/boundaries (`I'm not comfortable with that`)
- Adult: work/health (`I'd like to schedule a meeting`)
- Caregiver: coaching (`Take your time. I'm listening.`)
