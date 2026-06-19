# Calyndra cartoons & games — kid engagement + clinical alignment

Original Calyndra IP only. Educational AAC tool — **not** diagnosis, treatment, or emergency services.

## Kid engagement bar

- Caly mascot visible and reactive every scene / round
- Neural TTS on every prompt, celebration, and story beat (persona-matched)
- Bright motion: bounce, parade, confetti, mascot pulse — never static slides alone
- Repetition with variation (Super Simple Songs energy): same word, new context
- Interactive tap-along during cartoons and games
- Always skippable — no trapped loops

## Clinical alignment bar (SLP / OT / developmental pediatric friendly)

- **Modeling language:** "Your grown-up can model this word with you."
- **Assent-first:** Skip, pause, and "no" honored in scripts and UI
- **Errorless option:** Caly Says shows hand hints after one gentle miss
- **Celebrate attempts:** "Every try counts" — not only correct answers
- **Low sensory load:** No flashing >3Hz; captions on all cartoon narration
- **Caregiver co-play:** Short cue on Play screen for adult modeling
- **Evidence-aligned AAC practices:** aided language stimulation, wait time, follow the child's lead (see ASHA AAC practice briefs — we implement UX, not citations in-app)

## Voice

All narration via Caly Neural TTS (`/api/caly/speak`) with scripts in `games/caly-voice-scripts.json` and cartoon scene tables in `scripts/generate_videos_v5_cartoon.py`.

## Regenerate

```bash
python scripts/generate_videos_v5_cartoon.py
python scripts/optimize_symbol_assets.py
```
