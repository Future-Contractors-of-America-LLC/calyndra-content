# Band art QC report

Generated: **2026-06-23 09:32 UTC**

## Summary

| Status | Count |
|--------|-------|
| Band-unique symbols (pass) | 64 |
| Placeholder copies (fail) | 0 |
| Issues logged | 0 |
| Required band folders | 6 |
| Words checked | 64 |

## Band -> audience mapping

| Band folder | Mascot | Audience | Age band |
|-------------|--------|----------|----------|
| `sprout` | Sprout | toddler | 2-4 |
| `bud` | Bud | child | 5-8 |
| `sprig` | Sprig | tween | 9-12 |
| `vine` | Vine | teen | 13-17 |
| `bloom` | Bloom | adult | 18+ |
| `canopy` | Canopy | caregiver | caregiver |

### Bootstrap (sprout copy until unique Seed art)

| Band folder | Mascot | Audience | Age band |
|-------------|--------|----------|----------|
| `seed` | Seed | baby | 0-23mo (64 png) |

## Pass: band-unique words

`again`, `all-done`, `apple`, `ball`, `bathroom`, `big`, `blanket`, `book`, `bus`, `car`, `cat`, `clean`, `close`, `cold`, `cookie`, `daddy`, `dirty`, `dog`, `down`, `drink`, `dry`, `eat`, `friend`, `go`, `happy`, `help`, `home`, `hot`, `hug`, `hungry`, `hurt`, `juice`, `listen`, `little`, `look`, `love`, `mad`, `milk`, `mommy`, `more`, `need`, `no`, `open`, `play`, `please`, `sad`, `scared`, `shoe`, `sleep`, `stop`, `symbol_eat`, `symbol_happy`, `symbol_help`, `symbol_more`, `symbol_play`, `tired`, `toy`, `up`, `wait`, `want`, `wash`, `water`, `wet`, `yes`

## Fail: placeholder (same file in every band folder)

These still show old Sprout/human/object art for every age band until regenerated per mascot.

(none)

## Rules for regeneration

- Match band portrait reference exactly (Sprout romper, Bud tee, Sprig tendrils, Vine hoodie, Bloom cardigan, Canopy dress).
- **Do not** use Canopy dress/canopy leaves unless band is `canopy`.
- Happy expression default; five fingers per visible hand.
- Each band folder must contain the same word set; hashes must differ across sprout, bud, sprig, vine, bloom, and canopy.

## Other media (manual check)

- Videos/cartoons: still shared files; titles vary by audience but footage is not yet per-band.
- Voice: Azure TTS profiles differ per audience in `speech_tts.py` (verify after central deploy).

## Issues

- None
