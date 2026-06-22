# Caly motion and presence standards

**One plant Caly** — fluid, humanoid-adjacent motion on Sprout pose art. Not human portraits. Goal: animated character kids want to hug (toddler) without uncanny realism.

## Motion principles

| Principle | Implementation |
|-----------|----------------|
| Idle life | Breathing sway + subtle stem lean always on |
| Attention | Blink cycle every 3–6 s (respect `prefers-reduced-motion`) |
| Speech | Head/stem bob synced to TTS/speak events |
| React | Pose swap + bounce on celebrate/listen/dance |
| Age scale | Bouncier toddler ? smoother teen ? calmer adult/caregiver |

## Age-band motion profiles

| Band | Nickname | Idle | Speak bob | Celebrate | Clinical note |
|------|----------|------|-----------|-----------|---------------|
| toddler | Sprout | High bounce, wide sway | Fast bob, 1.2× amplitude | Jump pose + big burst | Caregiver-readable delight; no startling flashes |
| child | Bud | Medium bounce | Medium bob | Jump-celebrate | Assent-friendly; skip animations if reduce-motion |
| teen | Vine | Low bounce, smooth lean | Subtle bob | Listen-ear cue | Cool not childish — no infantilizing bounce |
| adult | Bloom | Minimal sway | Gentle nod | Sleepy/calm default | Professional calm for functional AAC |
| caregiver | Canopy | Calm sway (adult-like) | Soft nod | Wave welcome | Same character; warm not cartoon overload |

Registry: `caly_character_registry.json` ? `motionProfiles`.

## CSS architecture

- `css/caly-mascot-motion.css` — idle, blink, speak, age-band intensity variables
- `js/caly-mascot.js` — `attachMotion()`, `onSpeakStart()`, `onSpeakEnd()`
- `js/caly-voice.js` — fires motion during cached/Azure/browser TTS

## Reduced motion

When `prefers-reduced-motion: reduce` or app `sensory.reduceMotion`:

- Disable blink and celebrate bounce
- Keep static pose + optional single nod on speak

## SLP/OT/BCBA acceptability

- Motion supports engagement, not compliance pressure
- No sudden full-screen flashes tied to "correct" answers
- Celebrations can be quieted via sensory settings (`quietCelebrations`)
- Plant character avoids uncanny human lip-sync; pose + transform only

## Voice sync

Motion speak state lasts for estimated utterance duration if audio length unknown; cleared on `onSpeakEnd` from `calySpeak()` promise chain.

Reference: `CALY_CHARACTER_AGING.md`, `CALY_VOICE_GROWTH.md`, `CLINICAL_ENGAGEMENT_BAR.md`.
