<div align="center">

# CheatLikePro

**The Ultimate Stealthy Clipboard AI Assistant**

*Copy a question. Wait 1-2 seconds. Paste the exact answer.*

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-green)](https://github.com/GarvitOfficial/cheatLikePro)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen)](https://github.com/GarvitOfficial/cheatLikePro)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## Overview

**CheatLikePro** is a lightweight, zero-dependency background utility powered by modern Large Language Models (LLMs) via OpenRouter.

It silently monitors your clipboard. Whenever you copy (`Ctrl+C` / `Cmd+C`) a question, problem, or prompt, **CheatLikePro** fetches the answer from the AI model and instantly updates your clipboard with the solution.

> **No GUI. No Popups. Zero Latency. Zero Dependencies.**

---

## Workflow

```mermaid
flowchart LR
    A[Copy Question] --> B[Silent Engine]
    B --> C[OpenRouter AI]
    C --> D[Update Clipboard]
    D --> E[Paste Answer]
```



---

## Available Editions

CheatLikePro comes in two specialized editions:

| Feature | Standard Edition (`cheat.py`) | Linux & ML Edition (`cheat_linux.py`) |
| :--- | :--- | :--- |
| **Supported OS** | macOS, Windows, Linux | Linux (Native Display Engine) |
| **Target Focus** | General Q&A, MCQs, Math & Code | Python, Data Science & ML Workflows |
| **Default Model** | `upstage/solar-pro-3:free` | `nvidia/nemotron-3-super-120b-a12b:free` |
| **Clipboard Backend** | Cross-platform standard sub-process | Wayland (`wl-clipboard`) & X11 (`xclip` / `xsel`) |
| **Output Style** | Direct, concise & letter options for MCQs | Executable Python code (NumPy, Pandas, PyTorch) |
| **Script Path** | [`./cheat.py`](file:///Users/ganu/Programming/cheatlikepro/cheatLikePro/cheat.py) | [`./cheat_linux.py`](file:///Users/ganu/Programming/cheatlikepro/cheatLikePro/cheat_linux.py) |

---

## Features

- **Stealth Mode**: Operates silently in the background with no windows or popups.
- **Zero External Dependencies**: Uses standard Python 3 standard library (`urllib`, `subprocess`, `threading`, `json`).
- **Non-Blocking Multi-Threading**: Clipboard monitoring and network queries run on daemon threads.
- **Linux Wayland & X11 Native**: Built-in auto-detection for `wl-clipboard` (Wayland) and `xclip`/`xsel` (X11).
- **Multi-Model Ecosystem**: Works with OpenRouter models (DeepSeek-V3, Gemini 2.0, Nemotron, Llama 3, GPT-4o).
- **Smart Output Formatting**:
  - **Multiple Choice**: Returns only the answer option (e.g. `"B"`).
  - **Code Problems**: Returns raw executable code without conversational fluff.
  - **Math**: Returns exact numerical calculations.

---

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/GarvitOfficial/cheatLikePro.git
cd cheatLikePro
```

### 2. Configure API Key
Get your free API Key from [OpenRouter](https://openrouter.ai/keys).

```bash
# Create configuration file
cp .env.example .env

# Edit .env and paste your key
# OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

---

## Usage

### Standard Cross-Platform Edition
```bash
python3 cheat.py
```

### Linux & Machine Learning Edition
```bash
python3 cheat_linux.py
```

#### Linux Display Server Prerequisites
On Linux, install your display server's clipboard utility:
```bash
# Wayland
sudo apt install wl-clipboard

# X11
sudo apt install xclip
```

---

## Configuration (`.env`)

Customize model selection in `.env`:

```ini
# OpenRouter API Key
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here

# Selected Model
MODEL_NAME=upstage/solar-pro-3:free
```

### Recommended Models

| Model | ID | Speed | Best For |
| :--- | :--- | :--- | :--- |
| **Solar Pro 3 (Free)** | `upstage/solar-pro-3:free` | Ultra Fast | General QA & Fast MCQs |
| **Nemotron 3 (Free)** | `nvidia/nemotron-3-super-120b-a12b:free` | Ultra Fast | Coding & Data Science |
| **Gemini 2.0 Flash** | `google/gemini-2.0-flash-001` | Instant | Complex Reasoning |
| **DeepSeek Chat** | `deepseek/deepseek-chat` | Fast | Algorithmic Code |

---

## How To Use

1. Run the script in your terminal (`python3 cheat.py` or `python3 cheat_linux.py`).
2. Copy any question or code prompt (`Ctrl+C` or `Cmd+C`).
3. Wait 1 to 2 seconds.
4. Paste (`Ctrl+V` or `Cmd+V`) — the answer replaces your clipboard.

> *Text shorter than 5 characters is ignored to avoid accidental API calls.*

---

## Privacy & Safety

- **Direct Connections**: All requests are sent directly to `https://openrouter.ai/api/v1/chat/completions`.
- **Zero Logging**: No clipboard history is stored on disk.
- **Open Source**: 100% open and inspectable Python code.

---

## License & Authors

MIT License. Developed by [GarvitOfficial](https://github.com/GarvitOfficial) & [SonaliDuvesh](https://github.com/SonaliDuvesh).
