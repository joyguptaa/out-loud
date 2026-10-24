# Agent Guidelines – Voice Sanitizer

This document is the single source of truth for any AI agent working on the **Voice Sanitizer** project.
Follow these rules strictly.

---

## 1. Project Goal (Never Forget)

Build a **general-purpose macOS desktop application** that:

- Listens to the microphone in real time
- Transcribes speech using lightweight ASR models
- Removes fillers, repeated words, and short repeated phrases using **rule-based** sanitization
- Lets the user choose spoken language + output language
- Downloads **only** the model weights required for the selected languages
- Works fully offline after models are downloaded
- Ships first as a polished **`.dmg`** installer for macOS

**Hard constraints:**

- No heavy general-purpose LLMs in the MVP
- Prefer Vosk → Moonshine → faster-whisper (tiny/base)
- Keep the app as lightweight as possible
- Primary target: macOS 13+ (Apple Silicon + Intel)

---

## 2. Project Folder Structure Rule

Before adding or creating any new file or directory in this repository:

1. **Check the Project Structure First**: Always consult the reference folder structure documented below (and in `README.md`) before creating any new file or directory. Ensure every new component, module, asset, test, or script is placed strictly according to this structure.
2. **Clarification Over Assumption**: If there is any ambiguity, doubt, or confusion regarding where a file should belong or if a new path/file is needed, **ask the user directly for clarification instead of deciding or assuming on your own**.

### Official Folder Structure

```text
out-loud/
├── README.md
├── Agents.md
├── pyproject.toml / requirements.txt
├── src/
│   └── voice_sanitizer/
│       ├── __init__.py
│       ├── main.py                     # Entry point
│       ├── gui/
│       │   ├── __init__.py
│       │   ├── main_window.py
│       │   ├── settings_dialog.py
│       │   └── styles.py
│       ├── audio/
│       │   ├── __init__.py
│       │   ├── recorder.py             # Mic + VAD
│       │   └── pipeline.py
│       ├── asr/
│       │   ├── __init__.py
│       │   ├── base.py                 # Abstract ASR interface
│       │   ├── vosk_engine.py
│       │   ├── moonshine_engine.py
│       │   └── whisper_engine.py
│       ├── sanitizer/
│       │   ├── __init__.py
│       │   ├── cleaner.py
│       │   └── fillers.py              # Language-specific filler lists
│       ├── models/
│       │   ├── __init__.py
│       │   ├── manager.py              # Download & cache logic
│       │   └── registry.py             # Available models metadata
│       ├── output/
│       │   ├── __init__.py
│       │   └── paste.py
│       └── utils/
│           ├── __init__.py
│           ├── hotkeys.py
│           └── config.py
├── resources/
│   ├── icons/
│   └── fillers/                        # Optional JSON filler lists
├── scripts/
│   ├── build_mac.sh
│   └── create_dmg.sh
└── tests/
```

---

## 3. Atomic Commits Rule

- Make **small, focused, atomic commits**.
- Each commit should do **one logical thing only** (e.g. “Add VoskEngine class”, “Implement English filler removal”, “Add model download progress bar”).
- Never mix unrelated changes in the same commit (e.g. don’t combine a new feature + refactoring + formatting).
- Write clear and descriptive commit messages in the imperative mood:
  - Good: `Add Silero VAD to audio recorder`
  - Good: `Implement rule-based repetition removal`
  - Bad: `Update stuff`, `Fixes`, `WIP`
- If a change is large, break it into multiple sequential atomic commits.
- Do not create commits that leave the project in a broken state.

## 4. Development Phases (Follow Strictly)

Work **one phase at a time**.
After finishing a phase, summarize what was done, how to test it, and **wait for user confirmation** before starting the next phase.

### Phase 1 – Core Engine (CLI only)

- Project setup (`uv` or `poetry`)
- Microphone capture + Silero VAD
- Abstract `ASREngine` base class
- `VoskEngine` implementation
- Rule-based `TextCleaner` (English first)
- Simple CLI that prints raw → cleaned text in real time

### Phase 2 – Model Management

- `ModelRegistry` with supported languages
- `ModelManager` (download + cache to `~/Library/Application Support/VoiceSanitizer/models/`)
- Auto-download only the required language model

### Phase 3 – Full Audio Pipeline

- Connect Mic → VAD → ASR → Sanitizer → callback
- Support continuous + push-to-talk
- Expand filler lists to more languages

### Phase 4 – Desktop GUI (PySide6)

- Main window (language selectors, Start/Stop, live transcript, status)
- Settings dialog (hotkey, auto-paste, model size)
- System tray / menu bar support
- Native Mac look (light/dark mode)

### Phase 5 – System Integration

- Global hotkey (`pynput`)
- Auto-paste into focused app
- macOS Accessibility permission handling

### Phase 6 – Packaging (DMG)

- Create proper `.app` bundle (Briefcase or py2app)
- Ad-hoc code signing
- Professional DMG (drag-to-Applications)
- Test on Apple Silicon + Intel

### Phase 7 – Polish

- Better sanitization heuristics
- Error handling & logging
- README + basic docs
- Unit tests for sanitizer

---

## 5. Technical Preferences & Rules

- **ASR Priority**: Vosk (preferred) → Moonshine → faster-whisper tiny/base
- **Sanitization**: Must remain pure rule-based (no LLM) for MVP
- **Type hints**: Required on all new functions and methods
- **Config location**: `~/Library/Application Support/VoiceSanitizer/`
- **Models location**: `~/Library/Application Support/VoiceSanitizer/models/`
- Prefer small, focused modules over large files
- Write clean, readable, well-commented code
- Never introduce heavy dependencies without asking

---

## 6. Communication Rules

- After completing any phase or significant task, provide:
  1. Short summary of what was implemented
  2. How to run / test it
  3. Any open questions or blockers
- If you are unsure about architecture, library choice, or file placement → **ask the user**
- Do not invent new top-level folders or major architectural changes without approval

---

## 7. Current Status Tracking

At the top of your responses when working on the project, always state:

**Current Phase:** [Phase X]
**Status:** [In Progress / Completed / Blocked]

---

**End of Agent Guidelines**
