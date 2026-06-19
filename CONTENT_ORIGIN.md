# Calyndra original content policy

All user-facing media in Calyndra is **original IP** created by the Calyndra pipeline (Caly agent, generation scripts, Azure Neural TTS personas) — not stock art, not third-party cartoon characters, not scraped media.

| Asset type | How it is created | Owner |
|------------|-------------------|--------|
| Symbol pictures | `GenerateImage` + `optimize_symbol_assets.py` per `ILLUSTRATION_STYLE.md` | Future Contractors of America LLC |
| Mascots (Sprout, Quest, Spark, Core, Guide) | GenerateImage original characters | FCOA LLC |
| Educational videos | `generate_videos_v4_long.py` — original scripts, illustrated frames, programmatic animation, Caly TTS narration | FCOA LLC |
| Caly voice | Azure Neural TTS via `/api/caly/speak` with persona SSML (`speech_tts.py`) | Licensed Azure voice + original scripts |
| Caly text | Azure OpenAI `caly-speak` with governance instructions | Original responses |
| Lessons / FAQs | `generate_caly_content_v2.py` | Original copy |

**Inspired-by only:** preschool-show *energy* (warm, bouncy, educational) — never copy Lucas & Friends, Disney, Nickelodeon, or other trademarked works.

**Regenerate:** see `calyndra-content/scripts/` and `ART_DIRECTION.md`.
