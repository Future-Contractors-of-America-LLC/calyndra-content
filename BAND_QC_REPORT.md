# Band art QC report

Generated: **2026-06-24 12:34 UTC**

## Summary

| Status | Count |
|--------|-------|
| Band-unique symbols (pass) | 146 |
| Placeholder copies (fail) | 0 |
| Issues logged | 0 |
| Required band folders | 6 |
| Words checked | 146 |

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
| `seed` | Seed | baby | 0-23mo (146 png) |

## Pass: band-unique words

`again`, `algebra`, `all-done`, `apple`, `ball`, `bathroom`, `benefits`, `big`, `birthday`, `blanket`, `blankie`, `blocks`, `book`, `breathe`, `bubbles`, `budget`, `bus`, `camping`, `car`, `cat`, `celebrate`, `cereal`, `charger`, `clap`, `clean`, `close`, `cold`, `contractor`, `cookie`, `copay`, `credit-card`, `crib`, `cuddle`, `daddy`, `debate`, `detention`, `diploma`, `direct-deposit`, `dirty`, `dog`, `down`, `drink`, `drivers-license`, `dry`, `earbuds`, `eat`, `friend`, `gig-work`, `go`, `guitar`, `happy`, `help`, `home`, `hot`, `hr`, `hug`, `hungry`, `hurt`, `internship`, `juice`, `kite`, `listen`, `little`, `look`, `love`, `lullaby`, `mad`, `milk`, `mindfulness`, `modeling`, `mommy`, `more`, `mortgage`, `museum`, `need`, `no`, `onboarding`, `open`, `orchestra`, `overtime`, `owie`, `parking`, `part-time`, `patience`, `peek`, `pension`, `performance-review`, `permission`, `play`, `please`, `podcast`, `potty`, `presentation`, `prompt-wait`, `puzzle`, `regulation`, `reinforcement`, `retirement`, `rideshare`, `robotics`, `roommate`, `sad`, `sandbox`, `scaffold`, `scared`, `scholarship`, `science`, `scooter`, `shoe`, `sleep`, `soccer`, `social-media`, `spelling`, `splash`, `sticker`, `stop`, `streaming`, `subscription`, `syllabus`, `symbol_eat`, `symbol_happy`, `symbol_help`, `symbol_more`, `symbol_play`, `tablet`, `taxes`, `textbook`, `tired`, `toy`, `tricycle`, `truck`, `tuition`, `up`, `visual-schedule`, `volunteer`, `wagon`, `wait`, `want`, `warranty`, `wash`, `water`, `wet`, `yearbook`, `yes`, `yogurt`, `yum`

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
