# Caly voice growth arc

**One Caly maturing over time** — not random voice swaps. Each audience band maps to a growth nickname, neural voice, express-as style, and SSML `<prosody>` tuning. Primary character name is always **Caly**.

## Character × voice matrix

| Band | Nickname | Azure voice | Style | Rate | Pitch | Delivery |
|------|----------|-------------|-------|------|-------|----------|
| toddler | **Sprout** | en-US-AriaNeural | affectionate | ?35% | +15% | Slowest, highest pitch, sing-song phrase breaks (350 ms) |
| child | **Bud** | en-US-AnaNeural | cheerful | ?10% | +10% | Slightly faster, still bouncy; lighter phrase breaks (220 ms) |
| teen | **Vine** | en-US-JennyNeural | friendly | +3% | +2% | Neutral teen energy, respectful and direct |
| adult | **Bloom** | en-US-GuyNeural | calm | ?5% | ?8% | Steady, clear AAC guidance |
| caregiver | **Canopy** | en-US-GuyNeural | friendly | ?12% | ?10% | Warm professional, caregiver-facing (same voice base as adult) |

## SSML differentiation

Implemented in `calyndra-central/speech_tts.py`:

- **Toddler:** clause splits + 350 ms `<break>` between phrases + moderate emphasis on ALL-CAPS words + affectionate style + slowest/highest prosody.
- **Child:** same structure with 220 ms breaks and cheerier rate/pitch — still exploratory, not baby-talk.
- **Teen / adult / caregiver:** single `<prosody>` wrap without sing-song breaks; style tag carries emotional tone.

## API headers

`POST /api/caly/speak` returns MP3 with:

- `X-Caly-Voice` — neural voice name (e.g. `en-US-AriaNeural`)
- `X-Caly-Character` — Caly-toddler | Caly-child | … (internal band label)
- `X-Caly-Audience` — toddler | child | teen | adult | caregiver

## Frontend mirror

`calyndra-app/js/caly-voice.js` `BROWSER_VOICE_PREFER` matches the growth arc for offline/browser fallback. When the user changes **Audience** in the app, the next `calySpeak()` call uses the new band.

## Agent alignment

`CALY_INSTRUCTIONS.md` (central + agent) documents the same band tones so text and TTS stay aligned per audience.
