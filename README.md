<div align="center">

# CheatLikePro 🕵️‍♂️

**The Ultimate Stealthy Clipboard Assistant**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-green)](https://github.com/GarvitOfficial/cheatLikePro)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)](https://github.com/GarvitOfficial/cheatLikePro)

</div>

---

## 🚀 What is this?

**CheatLikePro** is a lightweight, background utility that gives you superpowers. It silently monitors your clipboard for questions, instantly fetches answers from advanced AI models (Gemini, DeepSeek, Llama, etc.), and places the answer right back into your clipboard.

**You copy a question. You wait 2 seconds. You paste the answer.**

It's sleek, it's fast, and it runs with **ZERO external dependencies** (no `pip install` required).

## ✨ Features

- **🕵️‍♂️ Stealth Mode**: Runs silently in the background. No GUI, no popups.
- **⚡ Super Fast**: optimized for speed with low-latency models.
- **🔌 Zero Dependencies**: Uses standard Python libraries only. Native `urllib` & `subprocess`.
- **🌍 Cross-Platform**: Works flawlessly on **macOS**, **Windows**, and **Linux**.
- **🤖 Multi-Model Support**: Defaults to `upstage/solar-pro-3` (free/fast), but compatiable with DeepSeek, Gemini, GPT-4o via OpenRouter.
- **🧠 Smart Formatting**:
  - **Code Questions**: Returns specific code only. No fluff.
  - **MCQ**: Returns just the option (e.g., "B").
  - **Math**: Returns just the number.

## 🛠️ Quick Start

### 1. Get the Code
```bash
git clone https://github.com/GarvitOfficial/cheatLikePro.git
cd cheatLikePro
```

### 2. Configure API Key
Get your key from [OpenRouter](https://openrouter.ai/keys) (gives you access to all top models).

```bash
# Create your configuration file
cp .env.example .env

# Open .env and paste your key
# OPENROUTER_API_KEY=sk-or-v1-...
```

### 3. Run It
```bash
python3 cheat.py
```

## 🎮 How To Use

1.  **Start the script** (keep it running in a terminal).
2.  **Highlight & Copy** (`Ctrl+C` / `Cmd+C`) any question or code problem.
3.  **Wait** ~1-2 seconds.
4.  **Paste** (`Ctrl+V` / `Cmd+V`). The answer will be there.

> **Note**: It won't trigger for short text (<5 chars) to avoid spamming the API.

## ⚙️ Configuration

Edit the `.env` file to customize:

```ini
# API Key (Required)
OPENROUTER_API_KEY=sk-or-your-key...

# Model Selection
# Recommended: upstage/solar-pro-3:free (Free, Smart)
# Fast: google/gemini-2.0-flash-001
# Smartest: deepseek/deepseek-chat
MODEL_NAME=upstage/solar-pro-3:free
```

## 🔒 Privacy & Safety

-   **Process**: Your clipboard data is sent **ONLY** to the OpenRouter API.
-   **No Logging**: The script does not save your clipboard history to disk.
-   **Source Code**: The entire logic is in `cheat.py`. It's open source—read it yourself!

## ⚠️ Disclaimer

This tool is for **educational purposes only**. The authors are not responsible for any misuse during exams, interviews, or other controlled environments. Use responsibly. 😉

---

<div align="center">
Made with ❤️ by <a href="https://github.com/GarvitOfficial">GarvitOfficial</a>
</div>
