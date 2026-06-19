# Calyndra Content

Real AAC vocabulary, board layouts, caregiver onboarding, lesson scripts, and Caly-authored guidance—grounded in [Calyndra System Law](https://github.com/Future-Contractors-of-America-LLC/calyndra-system-law).

## Structure

| Path | Description |
|------|-------------|
| `vocabulary/` | JSON symbol sets: toddler (20), child (50), teen/adult functional |
| `boards/` | Age-band board layout specifications |
| `onboarding/` | Welcome, introducing AAC, assent tips (Caly voice) |
| `lessons/` | Five quick-start modules for caregivers |
| `generated/` | FAQ, sensory UX tips, introduction scripts |

## Usage

- **Web & mobile apps** load vocabulary JSON from bundled copies in `calyndra-app/content/` and `calyndra-mobile/src/data/`.
- **API**: pass `vocabulary_term` with `/api/caly/invoke` for symbol-focused Caly responses.

## License

Copyright Future Contractors of America LLC. Content for Calyndra product use.
