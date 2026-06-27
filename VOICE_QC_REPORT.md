# Voice profile QC report

Generated: **2026-06-26 23:39 UTC**

**Overall:** PASS (0 issue(s), 3 warning(s))

- App VOICE_PROFILE_VERSION: **4**
- Manifest clips: **3341**
- Manifest generated: **True**

## Azure Neural profiles (speech_tts.py)

| Audience | Voice | Rate | Style | Status |
|----------|-------|------|-------|--------|
| baby | en-US-AriaNeural | -28% | affectionate | PASS |
| toddler | en-US-JaneNeural | -22% | affectionate | PASS |
| child | en-US-AnaNeural | -8% | cheerful | PASS |
| tween | en-US-AvaNeural | +0% | friendly | PASS |
| teen | en-US-JennyNeural | +2% | friendly | PASS |
| adult | en-US-MichelleNeural | -2% | calm | PASS |
| caregiver | en-US-NancyNeural | -8% | friendly | PASS |

## Issues

- None

## Warnings

- TTS: `toddler` uses `en-US-JaneNeural` (expected contains `AriaNeural`).
- TTS: `adult` uses `en-US-MichelleNeural` (expected contains `AvaNeural`).
- TTS: `caregiver` uses `en-US-NancyNeural` (expected contains `JennyNeural`).
