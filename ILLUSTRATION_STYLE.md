# Calyndra illustration standard (all band symbols)

**Quality bar:** Band portraits in `assets/caly-bands/` plus `CALY_SYMBOL_ART_RULES.md`  preschool show polish, original IP only.

## Locked character rules (read first)

See **`CALY_SYMBOL_ART_RULES.md`** for:

- **Expression:** Caly is **happy by default** on every symbol unless the word is explicitly an emotion (sad, mad, scared, etc.). Words like help, stop, and wait still use a warm smile.
- **Hands:** **Exactly five fingers** on each visible hand, every age band, every asset.

## Master prompt suffix (append to every word)

> Preschool educational cartoon illustration for an AAC app. Caly [NICKNAME] plant girl matching band portrait reference. Warm happy smile and bright eyes (unless symbol is an listed emotion exception). Exactly five fingers on each visible hand. Chunky rounded shapes, pastel mint and sky-blue palette, thick dark-green outlines, friendly big-eyed cartoon style, soft gradients, warm storybook lighting. Square 1:1, soft mint-to-sky gradient background, single clear pictogram centered, modest clothing, no text, no letters, no trademarked characters. Original Calyndra art only.

## Per-word prompts

| id | pictogram |
|----|-----------|
| no | Caly gently shaking head with soft **happy-calm** smile, X symbol nearby, respectful boundary |
| all-done | toddler pushing toy blocks away with finished smile |
| go | green go arrow with happy walking feet |
| wait | hourglass and gentle pause palm, patient smile |
| drink | colorful sippy cup with straw and water drops |
| bathroom | friendly potty chair with sparkle clean |
| sad | gentle tearful toddler face, caregiver-validated warmth |
| hug | open arms asking for consent hug, hearts |
| hurt | bandage on knee; Caly **kind and hopeful**, not distressed |
| sleep | cozy bed with moon and stars |
| up | arrow up with arms reaching up |
| down | arrow down with sitting gesture |
| water | shiny water drop and glass of water |
| milk | cute milk carton with cow spot |
| juice | bright juice box with straw |
| apple | shiny red apple with leaf |
| cookie | chocolate chip cookie |
| dog | friendly golden puppy wagging tail |
| cat | friendly orange kitten |
| ball | red playground ball |
| book | colorful picture book open |
| car | small red toy car |
| bus | yellow school bus smiling |
| shoe | colorful kids sneaker |
| wash | soap bubbles and hands washing |
| open | door opening with light |
| close | door closed snug |
| again | circular repeat arrows |
| please | hands together please gesture |
| love | big pink heart |
| mommy | warm mother figure waving |
| daddy | warm father figure waving |
| look | big friendly eyes looking |
| listen | ear with sound waves |
| big | large star next to small star |
| little | tiny star next to big star |
| wet | water splash on hands |
| dry | fluffy towel |
| hot | steaming soup bowl |
| cold | snowflake and ice cube |
| clean | sparkle shine on surface |
| dirty | small mud spot, still friendly |
| friend | two kids holding hands |
| blanket | soft cozy blanket |
| toy | teddy bear |
| stop | flat palm stop gesture, clear red stop sign |
| home | cozy house with heart window |

Regenerate with GenerateImage + band portrait reference ? copy to `calyndra-content/symbols/images/{band}/`, sync via `scripts/sync_band_symbols_to_app.py`.

**Do not install** symbols that fail the expression or five-finger checks in `CALY_SYMBOL_ART_RULES.md`.
