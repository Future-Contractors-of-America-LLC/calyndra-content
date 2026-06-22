# Caly voice growth arc

**One Caly maturing over time** — not random voice swaps. Caly is **female at every band**. Each audience maps to a growth nickname, neural voice, express-as style, styledegree, and SSML prosody. Primary character name is always **Caly**.

## Character × voice matrix

| Band | Nickname | Azure voice | Style | Rate | Pitch | Delivery |
|------|----------|-------------|-------|------|-------|----------|
| toddler | **Sprout** | en-US-AriaNeural | affectionate (0.85) | ?18% | +6% | Warm preschool host — gentle, not chipmunk |
| child | **Bud** | en-US-AnaNeural | cheerful (0.80) | ?4% | +4% | Natural kid energy, light phrase breaks (100 ms) |
| tween | **Sprig** | en-US-AvaNeural | friendly (0.78) | 0% | +2% | Curious, clear, bridging child and teen |
| teen | **Vine** | en-US-JennyNeural | friendly (0.72) | +2% | 0% | Respectful, direct, sounds like a real teen |
| adult | **Bloom** | en-US-AvaNeural | calm (0.68) | ?2% | ?2% | Warm adult guide — grounded, not robotic |
| caregiver | **Canopy** | en-US-JennyNeural | friendly (0.70) | ?8% | ?1% | Calm professional support tone |

## Humanization

`humanize_for_speech()` in `speech_tts.py`:

- Strips parenthetical nicknames before TTS ("I'm Caly (Sprout)" ? "I'm Caly")
- Uses contractions from child band upward
- Toddler keeps fuller phrases; teen/adult/caregiver get natural contractions

Phrase breaks for toddler/child are **short** (140 ms / 100 ms) so delivery feels conversational, not staccato.

## SSML

Implemented in `calyndra-central/speech_tts.py`:

- Toddler/child: clause splits + short breaks + caps emphasis where needed
- Tween through caregiver: steady prosody; emotional tone from `mstts:express-as` style + styledegree

## API headers

`POST /api/caly/speak` returns MP3 with:

- `X-Caly-Voice` — neural voice name
- `X-Caly-Character` — Caly-toddler | Caly-child | …
- `X-Caly-Audience` — toddler | child | tween | teen | adult | caregiver

## Frontend mirror

`calyndra-app/js/caly-voice.js` `BROWSER_VOICE_PREFER` uses **female** voices only for browser fallback, matching the arc above.

## Cached voice clips

Stale MP3 in `content/voice/manifest.json` may sound robotic until regenerated with the new profiles. Clear or rebuild manifest after deploying central TTS changes.
