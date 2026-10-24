# out-loud

A local voice sanitizer application.

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
