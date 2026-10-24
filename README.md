# Out Loud (Voice Sanitizer)

A lightweight, real-time, privacy-first macOS desktop application that transcribes speech locally and removes filler words, stuttered repetitions, and redundant phrases using deterministic, rule-based sanitization.

---

## Features

- **⚡ Real-Time Streaming Speech-to-Text**: Low-latency transcription powered by [Vosk](https://alphacephei.com/vosk/) and [Silero VAD](https://github.com/snakers4/silero-vad).
- **🧹 Rule-Based Sanitization**:
  - Removes common hesitation sounds (`uh`, `um`, `er`, `ah`).
  - Strips conversational fillers (`you know`, `i mean`, `sort of`, `kind of`).
  - Collapses consecutive duplicate words and contractions (`the the` → `the`, `don't don't` → `don't`).
  - Eliminates repeated short n-grams (2–4 words).
- **🔒 100% Offline & Private**: All speech processing, voice activity detection, and text cleaning run completely on-device. No audio or text ever leaves your machine.
- **📦 On-Demand Model Management**: Downloads and caches only the lightweight model required for the selected language (~40 MB per model).
- **🍎 macOS Native Focus**: Built specifically for macOS 13+ (Apple Silicon & Intel).

---

## Architecture & Pipeline

```text
[ Microphone ]
      │
      ▼ (16 kHz PCM)
[ Silero VAD ] ──────────► Detects speech start / end boundaries
      │ (speech chunks)
      ▼
[ VoskEngine ] ──────────► Offline streaming speech recognition
      │ (raw text)
      ▼
[ TextCleaner ] ─────────► Rule-based filler & repetition removal
      │
      ▼
[ Live Output ] ─────────► Terminal CLI (Phase 1) / Desktop GUI & Auto-Paste (Phases 4–5)
```

---

## Quickstart

### Prerequisites

- macOS 13+ (Apple Silicon or Intel)
- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`

### 1. Installation

Clone the repository and install dependencies with `uv`:

```bash
git clone https://github.com/your-username/out-loud.git
cd out-loud
uv sync
```

### 2. Run the CLI

Start the interactive CLI voice sanitizer:

```bash
uv run out-loud
# or
.venv/bin/python -m voice_sanitizer.main
```

1. Select your spoken language (defaults to English).
2. On first launch, the required model will automatically be downloaded to:
   `~/Library/Application Support/VoiceSanitizer/models/`
3. Speak into your microphone. Watch live partial transcriptions stream in, followed by the finalized clean text:

```text
  ▸ i want to go to the store
  Raw:   um i want to i want to go to the the store you know
  Clean: i want to go to the store
```

Press `Ctrl+C` to stop.

---

## Running Tests

Run the full unit test suite with `pytest`:

```bash
uv run pytest tests/ -v
```

---

## Project Structure

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

## Development Roadmap

- [x] **Phase 1: Core Engine (CLI only)** — Audio capture, Silero VAD, `ASREngine`, `VoskEngine`, rule-based `TextCleaner`, and interactive CLI.
- [ ] **Phase 2: Model Management** — Enhanced model registry, download verification, and cache management.
- [ ] **Phase 3: Full Audio Pipeline** — Push-to-talk, continuous streaming modes, and expanded multi-language filler dictionaries.
- [ ] **Phase 4: Desktop GUI (PySide6)** — Native macOS floating/docked window, live transcript view, and menu bar tray.
- [ ] **Phase 5: System Integration** — Global system hotkeys (`pynput`), accessibility permissions, and direct auto-paste into focused apps.
- [ ] **Phase 6: Packaging & Distribution** — Native macOS `.app` bundle, ad-hoc signing, and `.dmg` installer.
- [ ] **Phase 7: Polish & Optimization** — Enhanced sanitization heuristics, performance tuning, and comprehensive docs.

---

## License

MIT License. See LICENSE file for details.
