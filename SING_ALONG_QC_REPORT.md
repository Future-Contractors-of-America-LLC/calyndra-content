# Sing-along catalog QC report

Generated: **2026-06-24 17:27 UTC**

## Summary

| Audience | Total | Existing | New | Status |
|----------|-------|----------|-----|--------|
| baby | 6 | 0 | 6 | PASS |
| toddler | 7 | 1 | 6 | PASS |
| child | 6 | 0 | 6 | PASS |
| tween | 5 | 0 | 5 | PASS |

**Issues:** 0

## Rules checked

- At least 5 episodes per baby/toddler/child
- `durationMs` in [120000, 240000] (~2-4 min)
- Each episode has 4+ beats with ms/pose/lyric/word/mascotCue
- All `show_*` voice keys present in `caly-voice-scripts.json` per audience
- `bandPortrait` and `title` set on every episode

## Issues

- None
