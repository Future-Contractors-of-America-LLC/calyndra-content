# Band art QC report

Generated: **2026-06-26 23:40 UTC**

## Summary

| Status | Count |
|--------|-------|
| Band-unique symbols (pass) | 150 |
| Placeholder copies (fail) | 0 |
| Issues logged | 0 |
| Required band folders | 6 |
| Words checked | 331 |

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
| `seed` | Seed | baby | 0-23mo (58 png) |

## Pass: band-unique words

`again`, `algebra`, `all-done`, `apple`, `ball`, `bathroom`, `benefits`, `best_friend`, `big`, `birthday`, `blanket`, `blankie`, `blocks`, `book`, `breathe`, `bubbles`, `budget`, `bus`, `camping`, `car`, `cat`, `celebrate`, `cereal`, `charger`, `clap`, `clean`, `close`, `cold`, `contractor`, `cookie`, `copay`, `credit-card`, `crib`, `cuddle`, `daddy`, `debate`, `detention`, `diploma`, `direct-deposit`, `dirty`, `dog`, `down`, `drink`, `drivers-license`, `dry`, `earbuds`, `eat`, `friend`, `gentle`, `gig-work`, `go`, `guitar`, `happy`, `help`, `home`, `hot`, `hr`, `hug`, `hungry`, `hurt`, `internship`, `juice`, `kite`, `listen`, `little`, `little_brother`, `look`, `love`, `lullaby`, `mad`, `milk`, `mindfulness`, `modeling`, `mommy`, `more`, `mortgage`, `museum`, `need`, `no`, `onboarding`, `open`, `orchestra`, `overtime`, `owie`, `parking`, `part-time`, `patience`, `peek`, `pension`, `performance-review`, `permission`, `play`, `please`, `podcast`, `potty`, `presentation`, `prompt-wait`, `puzzle`, `regulation`, `reinforcement`, `retirement`, `rideshare`, `robotics`, `roommate`, `sad`, `sandbox`, `scaffold`, `scared`, `scholarship`, `science`, `scooter`, `shoe`, `sleep`, `snack`, `soccer`, `social-media`, `spelling`, `splash`, `sticker`, `stop`, `streaming`, `subscription`, `syllabus`, `symbol_eat`, `symbol_happy`, `symbol_help`, `symbol_more`, `symbol_play`, `tablet`, `taxes`, `textbook`, `tired`, `toy`, `tricycle`, `truck`, `tuition`, `up`, `visual-schedule`, `volunteer`, `wagon`, `wait`, `want`, `warranty`, `wash`, `water`, `wet`, `yearbook`, `yes`, `yogurt`, `yum`

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

## Warnings

- WORD COUNT varies across band folders (expanded vocab): bloom=324, bud=202, canopy=168, sprig=269, sprout=170, vine=312.
- `bud` lacks 2 word(s) vs `sprout` (e.g. dada, mama).
- `bud` has 34 extra word(s) vs `sprout` (e.g. alone, backpack, best_friend, break, brother).
- `sprig` lacks 2 word(s) vs `sprout` (e.g. dada, mama).
- `sprig` has 101 extra word(s) vs `sprout` (e.g. alarm, alone, appointment, baby, backpack).
- `vine` lacks 2 word(s) vs `sprout` (e.g. dada, mama).
- `vine` has 144 extra word(s) vs `sprout` (e.g. accommodation, alarm, allergy, alone, anxious).
- `bloom` lacks 2 word(s) vs `sprout` (e.g. dada, mama).
- `bloom` has 156 extra word(s) vs `sprout` (e.g. accommodation, alarm, allergy, alone, anxious).
- `canopy` lacks 22 word(s) vs `sprout` (e.g. bottle, brush-teeth, bunny, bye, coat).
- `canopy` has 20 extra word(s) vs `sprout` (e.g. aunt, best_friend, break, choice, cousin).
