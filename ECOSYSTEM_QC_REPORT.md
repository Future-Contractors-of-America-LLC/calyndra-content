# Ecosystem QC report

Generated: **2026-06-25 20:01 UTC**

**Overall:** PASS (0 issue(s))

## Summary

| Check | Result |
|-------|--------|
| `qc_band_assets.py` | PASS |
| `qc_art_quality.py` | PASS |
| `qc_voice_profiles.py` | PASS |
| `qc_games_catalog.py` | PASS |
| `qc_sing_along_catalog.py` | PASS |
| `qc_cartoon_catalog.py` | PASS |
| `qc_cinematic_catalog.py` | PASS |
| `qc_style_consistency.py` | PASS |
| Vocabulary files (words per band) | PASS |
| Games catalog (5+ new per band) | PASS |
| Sing-along (5+ per band) | PASS |
| Caly and Friends episodes | PASS |
| Symbol PNG counts vs manifest | PASS |
| app/index.html baby audience | PASS |
| speech_tts.py neural profiles (7 bands) | PASS |
| Art quality (`qc_art_quality.py`) | PASS |
| Voice profiles (`qc_voice_profiles.py`) | PASS |
| Manifest sync to calyndra-app/content | 30 file(s) |

## Vocabulary

| Band | words.json | Status |
|------|------------|--------|
| baby | yes | PASS |
| toddler | yes | PASS |
| child | yes | PASS |
| tween | yes | PASS |
| teen | yes | PASS |
| adult | yes | PASS |
| caregiver | yes | PASS |

## Games (new per band)

| Band | New games | Status |
|------|-----------|--------|
| baby | 5 | PASS |
| toddler | 5 | PASS |
| child | 5 | PASS |
| tween | 5 | PASS |
| teen | 5 | PASS |
| adult | 5 | PASS |
| caregiver | 5 | PASS |

## Sing-along episodes

| Band | Episodes | Status |
|------|----------|--------|
| baby | 6 | PASS |
| toddler | 7 | PASS |
| child | 6 | PASS |
| tween | 5 | PASS |
| teen | 5 | PASS |
| adult | 5 | PASS |
| caregiver | 5 | PASS |

## Caly and Friends

| Band | Episodes | Status |
|------|----------|--------|
| baby | 6 | PASS |
| toddler | 6 | PASS |
| child | 6 | PASS |
| tween | 6 | PASS |
| teen | 6 | PASS |
| adult | 6 | PASS |

## Symbol folders vs manifest

| Band folder | PNG count | Manifest expected | Status |
|-------------|-----------|-------------------|--------|
| `seed` | 161 | 150 | PASS |
| `sprout` | 168 | 150 | PASS |
| `bud` | 202 | 150 | PASS |
| `sprig` | 269 | 150 | PASS |
| `vine` | 312 | 150 | PASS |
| `bloom` | 324 | 150 | PASS |
| `canopy` | 168 | 150 | PASS |

## Synced to calyndra-app/content

- `band-art-manifest.json`
- `band-games-catalog.json`
- `sing-along-catalog.json`
- `caly-voice-scripts.json`
- `caly_character_registry.json`
- `videos/caly_friends_catalog.json`
- `adult-phrases.json`
- `adult-vocab.json`
- `adult-words.json`
- `baby-phrases.json`
- `baby-vocab.json`
- `baby-words.json`
- `caregiver-phrases.json`
- `caregiver-vocab.json`
- `caregiver-words.json`
- `child-core.json`
- `child-expanded.json`
- `child-phrases.json`
- `child-vocab.json`
- `child-words.json`
- `teen-adult-functional.json`
- `teen-phrases.json`
- `teen-vocab.json`
- `teen-words.json`
- `toddler-core.json`
- `toddler-phrases.json`
- `toddler-words.json`
- `tween-phrases.json`
- `tween-vocab.json`
- `tween-words.json`

## Sub-script output

### qc_band_assets.py (exit 0)

```
QC: 150 pass, 0 placeholder, 0 issues
Wrote band-art-manifest.json and BAND_QC_REPORT.md
```

### qc_art_quality.py (exit 0)

```
Art QC: PASS - 0 issue(s), 2 warning(s)
Wrote ART_QC_REPORT.md
```

### qc_voice_profiles.py (exit 0)

```
Voice QC: PASS - 0 issue(s), 0 warning(s)
Wrote VOICE_QC_REPORT.md
```

### qc_games_catalog.py (exit 0)

```
QC: 7 audiences, 0 issues
Wrote GAMES_QC_REPORT.md
  baby: 5 new / 13 total
  toddler: 5 new / 13 total
  child: 5 new / 13 total
  tween: 5 new / 13 total
  teen: 5 new / 13 total
  adult: 5 new / 13 total
  caregiver: 5 new / 13 total
```

### qc_sing_along_catalog.py (exit 0)

```
QC: 7 audiences, 0 issues
Wrote SING_ALONG_QC_REPORT.md
  baby: 6 episodes (6 new)
  toddler: 7 episodes (6 new)
  child: 6 episodes (6 new)
  tween: 5 episodes (5 new)
  teen: 5 episodes (5 new)
  adult: 5 episodes (5 new)
  caregiver: 5 episodes (5 new)
```

### qc_cartoon_catalog.py (exit 0)

```
baby: 6 episode(s) - Pip's Gentle Hello, Pip and the Soft Breeze, Pip's Moonlight Snuggle, Pip's Twinkle Toes, Pip's Rainbow Wave, Pip's Heartbeat Lullaby
  toddler: 6 episode(s) - Fern's Garden Share, Fern's Flower Surprise, Fern's Patience Pots, Fern's Butterfly Visit, Fern's Weeding Teamwork, Fern's Seed Gift
  child: 6 episode(s) - Moss and the Kindness Trail, Moss the Bridge Builders, Moss Lost and Found, Moss's Campfire Stories, Moss and the Apology Path, Moss's Team Harvest
  tween: 6 episode(s) - Reed's Wisdom Perch, Reed and the Rumor Mist, Reed's Patience Listeners, Reed's Honest Feather, Reed's Storm Shelter, Reed's Mentor Circle
  teen: 6 episode(s) - Sage at the Crossroads, Sage and Truth Telling, Sage and Peer Pressure, Sage's Forgiveness Trail, Sage's Service Saturday, Sage's Steady Anchor
  adult: 6 episode(s) - Laurel's Morning Song, Laurel's Evening Rest, Laurel's Caregiver Breath, Laurel's Gratitude Journal, Laurel's Community Table, Laurel's Legacy Roots

QC summary
  Episodes: 36
  Errors: 0
  Warnings: 0
```

### qc_cinematic_catalog.py (exit 0)

```
Cinematic QC: 36 episodes checked.
  WARN: pip_gentle_hello_long: pilot resolution 1280x720 — schedule UHD re-render.
  WARN: fern_garden_share_long: pilot resolution 1280x720 — schedule UHD re-render.
  WARN: moss_kindness_trail_long: pilot resolution 1280x720 — schedule UHD re-render.
  WARN: reed_wisdom_perch_long: resolution 1280x720 — HD upgrade pending (target 1920x1080+).
  WARN: sage_crossroads_long: resolution 1280x720 — HD upgrade pending (target 1920x1080+).
  WARN: laurel_morning_song_long: resolution 1280x720 — HD upgrade pending (target 1920x1080+).
  WARN: pip_soft_breeze_long: resolution 1280x720 — HD upgrade pending (target 1920x1080+).
  WARN: pip_moonlight_snuggle_long: resolution 1280x720 — HD upgrade pending (target 1920x1080+).
  WARN: pip_twinkle_toes_long: resolution 1280x720 — HD upgrade pending (target 1920x1080+).
  WARN: pip_rainbow_wave_long: resolution 1280x720 — HD upgrade pending (target 1920x1080+).
  WARN: pip_heartbeat_lullaby_long: resolution 1280x720 — HD upgrade pending (target 1920x1080+).
  WARN: fern_flower_surprise_long: resolution 1280x720 — HD upgrade pending (target 1920x1080+).
  WARN: fern_patience_pots_long: resolution 1280x720 — HD upgrade pending (target 1920x1080+).
  WARN: fern_butterfly_visit_long: resolution 1280x720 — HD upgrade pending (target 1920x1080+).
  WARN: fern_weeding_teamwork_long: resolution 1280x720 — HD upgrade pending (target 1920x1080+).
```

### qc_style_consistency.py (exit 0)

```
Style QC: 0 issue(s), 0 warning(s).
```


## Issues

- None
