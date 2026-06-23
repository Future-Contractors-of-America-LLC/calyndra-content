# Caly voice growth arc

**One Caly maturing over time** — not random voice swaps. Caly is **female at every band**. Each audience maps to a growth nickname, neural voice, express-as style, styledegree, and SSML prosody. Primary character name is always **Caly**.

## Character × voice matrix

| Band | Nickname | Azure voice | Style | Rate | Pitch | Delivery |
|------|----------|-------------|-------|------|-------|----------|
| baby | **Seedling** | en-US-AriaNeural | affectionate (0.95) | ?28% | +8% | Lullaby-slow, cartoon-warm nursery host |
| toddler | **Sprout** | en-US-AriaNeural | affectionate (0.90) | ?22% | +7% | Sing-song preschool host — gentle and human |
| child | **Bud** | en-US-AnaNeural | cheerful (0.85) | ?8% | +5% | Natural kid energy, light phrase breaks (120 ms) |
| tween | **Sprig** | en-US-AvaNeural | friendly (0.78) | 0% | +2% | Curious, clear, bridging child and teen |
| teen | **Vine** | en-US-JennyNeural | friendly (0.72) | +2% | 0% | Respectful, direct, sounds like a real teen |
| adult | **Bloom** | en-US-AvaNeural | calm (0.68) | ?2% | ?2% | Warm adult guide — grounded, not robotic |
| caregiver | **Canopy** | en-US-JennyNeural | friendly (0.70) | ?8% | ?1% | Calm professional support tone |

## Humanization (June 2026 tuning)

`humanize_for_speech()` in `speech_tts.py`:

- Strips parenthetical nicknames before TTS ("I'm Caly (Sprout)" ? "I'm Caly")
- Uses contractions from child band upward; baby/toddler get gentle "don't" only
- Baby and toddler: slower clause breaks (180 ms / 160 ms) for sing-song, cartoonish delivery
- Child: 120 ms phrase breaks — conversational bounce without staccato
- Higher `styledegree` on baby (0.95) and toddler (0.90) for affectionate neural express-as

Phrase breaks for baby/toddler/child are **longer than before** so delivery feels like a real person reading to a child, not a script.

## SSML

Implemented in `calyndra-central/speech_tts.py`:

- Baby/toddler/child: clause splits + audience-tuned breaks + caps emphasis where needed
- Tween through caregiver: steady prosody; emotional tone from `mstts:express-as` style + styledegree

## API headers

`POST /api/caly/speak` returns MP3 with:

- `X-Caly-Voice` — neural voice name
- `X-Caly-Character` — Caly-baby | Caly-toddler | Caly-child | …
- `X-Caly-Audience` — baby | toddler | child | tween | teen | adult | caregiver

## Frontend mirror

`calyndra-app/js/caly-voice.js` `BROWSER_VOICE_PREFER` mirrors the arc:

| Band | Browser rate | Browser pitch |
|------|--------------|-----------------|
| baby | 0.72 | 1.08 |
| toddler | 0.78 | 1.07 |
| child | 0.92 | 1.05 |

Female voices only for browser fallback (Aria/Ana preferred).

## Agent prompts

`calyndra-central/caly_prompts.py` includes a **baby (Seedling)** band block and warmer toddler/child prosody guidance so chat text matches TTS delivery.

## Cached voice clips

Stale MP3 in `content/voice/manifest.json` may sound robotic until regenerated with the new profiles. Clear or rebuild manifest after deploying central TTS changes.
