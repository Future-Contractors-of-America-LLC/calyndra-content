# Ecosystem QC report

Generated: **2026-06-24 12:18 UTC**

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
| baby | 1 | PASS |
| toddler | 1 | PASS |
| child | 1 | PASS |
| tween | 1 | PASS |
| teen | 1 | PASS |
| adult | 1 | PASS |

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
baby: 1 episode(s) - Pip's Gentle Hello
  toddler: 1 episode(s) - Fern's Garden Share
  child: 1 episode(s) - Moss and the Kindness Trail
  tween: 1 episode(s) - Reed's Wisdom Perch
  teen: 1 episode(s) - Sage at the Crossroads
  adult: 1 episode(s) - Laurel's Morning Song

QC summary
  Episodes: 6
  Errors: 0
  Warnings: 5
  WARN: Pilot fern_garden_share_long.webm: 52s (full target 600s)
  WARN: Pilot moss_kindness_trail_long.webm: 49s (full target 900s)
  WARN: reed_wisdom_perch_long.webm: placeholder 5s (target 1200s full)
  WARN: sage_crossroads_long.webm: placeholder 5s (target 1800s full)
  WARN: laurel_morning_song_long.webm: placeholder 5s (target 2700s full)
```


## Issues

- None
