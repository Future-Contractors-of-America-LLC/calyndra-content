# Ecosystem QC report

Generated: **2026-06-24 17:38 UTC**

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
| Vocabulary files (words per band) | PASS |
| Games catalog (5+ new per band) | PASS |
| Sing-along (5+ baby/toddler/child) | PASS |
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
| `seed` | 146 | 146 | PASS |
| `sprout` | 146 | 146 | PASS |
| `bud` | 146 | 146 | PASS |
| `sprig` | 146 | 146 | PASS |
| `vine` | 146 | 146 | PASS |
| `bloom` | 146 | 146 | PASS |
| `canopy` | 146 | 146 | PASS |

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
QC: 146 pass, 0 placeholder, 0 issues
Wrote band-art-manifest.json and BAND_QC_REPORT.md
```

### qc_art_quality.py (exit 0)

```
Art QC: PASS - 0 issue(s), 8 warning(s)
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
QC: 4 audiences, 0 issues
Wrote SING_ALONG_QC_REPORT.md
  baby: 6 episodes (6 new)
  toddler: 7 episodes (6 new)
  child: 6 episodes (6 new)
  tween: 5 episodes (5 new)
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
  Warnings: 30
  WARN: Script-only (no webm yet): pip_soft_breeze_long.webm
  WARN: Script-only (no webm yet): pip_moonlight_snuggle_long.webm
  WARN: Script-only (no webm yet): pip_twinkle_toes_long.webm
  WARN: Script-only (no webm yet): pip_rainbow_wave_long.webm
  WARN: Script-only (no webm yet): pip_heartbeat_lullaby_long.webm
  WARN: Script-only (no webm yet): fern_flower_surprise_long.webm
  WARN: Script-only (no webm yet): fern_patience_pots_long.webm
  WARN: Script-only (no webm yet): fern_butterfly_visit_long.webm
  WARN: Script-only (no webm yet): fern_weeding_teamwork_long.webm
  WARN: Script-only (no webm yet): fern_seed_gift_long.webm
  WARN: Script-only (no webm yet): moss_bridge_builders_long.webm
  WARN: Script-only (no webm yet): moss_lost_and_found_long.webm
  WARN: Script-only (no webm yet): moss_campfire_stories_long.webm
  WARN: Script-only (no webm yet): moss_apology_path_long.webm
  WARN: Script-only (no webm yet): moss_team_harvest_long.webm
  WARN: Script-only (no webm yet): reed_rumor_mist_long.webm
  WARN: Script-only (no webm yet): reed_patience_listeners_long.webm
  WARN: Script-only (no webm yet): reed_honest_feather_long.webm
  WARN: Script-only (no webm yet): reed_storm_shelter_long.webm
  WARN: Script-only (no webm yet): reed_mentor_circle_long.webm
  WARN: Script-only (no webm yet): sage_truth_telling_long.webm
  WARN: Script-only (no webm yet): sage_peer_pressure_long.webm
  WARN: Script-only (no webm yet): sage_forgiveness_trail_long.webm
  WARN: Script-only (no webm yet): sage_service_saturday_long.webm
  WARN: Script-only (no webm yet): sage_steady_anchor_long.webm
  WARN: Script-only (no webm yet): laurel_evening_rest_long.webm
  WARN: Script-only (no webm yet): laurel_caregiver_breath_long.webm
  WARN: Script-only (no webm yet): laurel_gratitude_journal_long.webm
  WARN: Script-only (no webm yet): laurel_community_table_long.webm
  WARN: Script-only (no webm yet): laurel_legacy_roots_long.webm
```


## Issues

- None
