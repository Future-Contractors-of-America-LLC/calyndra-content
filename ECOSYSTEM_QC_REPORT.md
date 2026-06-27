# Ecosystem QC report

Generated: **2026-06-27 19:09 UTC**

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
| `seed` | 58 | 54 | PASS |
| `sprout` | 170 | 87 | PASS |
| `bud` | 202 | 117 | PASS |
| `sprig` | 269 | 183 | PASS |
| `vine` | 312 | 221 | PASS |
| `bloom` | 324 | 236 | PASS |
| `canopy` | 168 | 56 | PASS |

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
Voice QC: PASS - 0 issue(s), 3 warning(s)
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
  Warnings: 36
  WARN: pip_gentle_hello_long.webm: 231s < 255s (85% of 300s target) — re-render needed
  WARN: fern_garden_share_long.webm: 410s < 510s (85% of 600s target) — re-render needed
  WARN: moss_kindness_trail_long.webm: 603s < 765s (85% of 900s target) — re-render needed
  WARN: reed_wisdom_perch_long.webm: 654s < 1020s (85% of 1200s target) — re-render needed
  WARN: sage_crossroads_long.webm: 1065s < 1530s (85% of 1800s target) — re-render needed
  WARN: laurel_morning_song_long.webm: 1386s < 2295s (85% of 2700s target) — re-render needed
  WARN: pip_soft_breeze_long.webm: 240s < 255s (85% of 300s target) — re-render needed
  WARN: pip_moonlight_snuggle_long.webm: 224s < 255s (85% of 300s target) — re-render needed
  WARN: pip_twinkle_toes_long.webm: 236s < 255s (85% of 300s target) — re-render needed
  WARN: pip_rainbow_wave_long.webm: 251s < 255s (85% of 300s target) — re-render needed
  WARN: pip_heartbeat_lullaby_long.webm: 252s < 255s (85% of 300s target) — re-render needed
  WARN: fern_flower_surprise_long.webm: 424s < 510s (85% of 600s target) — re-render needed
  WARN: fern_patience_pots_long.webm: 449s < 510s (85% of 600s target) — re-render needed
  WARN: fern_butterfly_visit_long.webm: 465s < 510s (85% of 600s target) — re-render needed
  WARN: fern_weeding_teamwork_long.webm: 462s < 510s (85% of 600s target) — re-render needed
  WARN: fern_seed_gift_long.webm: 449s < 510s (85% of 600s target) — re-render needed
  WARN: moss_bridge_builders_long.webm: 667s < 765s (85% of 900s target) — re-render needed
  WARN: moss_lost_and_found_long.webm: placeholder 5s (target 900s full)
  WARN: moss_campfire_stories_long.webm: placeholder 5s (target 900s full)
  WARN: moss_apology_path_long.webm: placeholder 5s (target 900s full)
  WARN: moss_team_harvest_long.webm: placeholder 5s (target 900s full)
  WARN: reed_rumor_mist_long.webm: placeholder 5s (target 1200s full)
  WARN: reed_patience_listeners_long.webm: placeholder 5s (target 1200s full)
  WARN: reed_honest_feather_long.webm: placeholder 5s (target 1200s full)
  WARN: reed_storm_shelter_long.webm: placeholder 5s (target 1200s full)
  WARN: reed_mentor_circle_long.webm: placeholder 5s (target 1200s full)
  WARN: sage_truth_telling_long.webm: placeholder 5s (target 1800s full)
  WARN: sage_peer_pressure_long.webm: placeholder 5s (target 1800s full)
  WARN: sage_forgiveness_trail_long.webm: placeholder 5s (target 1800s full)
  WARN: sage_service_saturday_long.webm: placeholder 5s (target 1800s full)
  WARN: sage_steady_anchor_long.webm: placeholder 5s (target 1800s full)
  WARN: laurel_evening_rest_long.webm: placeholder 5s (target 2700s full)
  WARN: laurel_caregiver_breath_long.webm: placeholder 5s (target 2700s full)
  WARN: laurel_gratitude_journal_long.webm: placeholder 5s (target 2700s full)
  WARN: laurel_community_table_long.webm: placeholder 5s (target 2700s full)
  WARN: laurel_legacy_roots_long.webm: placeholder 5s (target 2700s full)
```

### qc_cinematic_catalog.py (exit 0)

```
Cinematic QC (strict-uhd): 36 episodes checked.
  WARN: pip_gentle_hello_long: probed 1280x720 — UHD upgrade pending (ship allows HD interim).
  WARN: pip_gentle_hello_long: catalog profile `hd` — UHD upgrade pending.
  WARN: pip_gentle_hello_long: duration 231s < 255s (85% of 300s target). Full-length re-render pending.
  WARN: fern_garden_share_long: probed 1280x720 — UHD upgrade pending (ship allows HD interim).
  WARN: fern_garden_share_long: catalog profile `hd` — UHD upgrade pending.
  WARN: fern_garden_share_long: duration 410s < 510s (85% of 600s target). Full-length re-render pending.
  WARN: moss_kindness_trail_long: probed 1280x720 — UHD upgrade pending (ship allows HD interim).
  WARN: moss_kindness_trail_long: catalog profile `hd` — UHD upgrade pending.
  WARN: moss_kindness_trail_long: duration 603s < 765s (85% of 900s target). Full-length re-render pending.
  WARN: reed_wisdom_perch_long: probed 1280x720 — UHD upgrade pending (ship allows HD interim).
  WARN: reed_wisdom_perch_long: catalog profile `hd` — UHD upgrade pending.
  WARN: reed_wisdom_perch_long: duration 654s < 1020s (85% of 1200s target). Full-length re-render pending.
  WARN: sage_crossroads_long: probed 1280x720 — UHD upgrade pending (ship allows HD interim).
  WARN: sage_crossroads_long: catalog profile `hd` — UHD upgrade pending.
  WARN: sage_crossroads_long: duration 1065s < 1530s (85% of 1800s target). Full-length re-render pending.
```

### qc_style_consistency.py (exit 0)

```
Style QC: 0 issue(s), 0 warning(s).
```


## Issues

- None
