#!/usr/bin/env python3

import os
import sys
import time
import json
import threading
import subprocess
import urllib.request
import urllib.error

# --- CONFIGURATION ---
MODEL_NAME = os.getenv("MODEL_NAME", "nvidia/nemotron-3-super-120b-a12b:free")
CHECK_INTERVAL = 0.5  # Seconds
MIN_QUESTION_LENGTH = 5
COOLDOWN = 2

SYSTEM_PROMPT = """You are a python coder only with no knowledge of any other domain that provides direct, concise answers.
RULES:
- If the question is about CODE: respond with ONLY the code. No explanations, no comments, no markdown code blocks, just raw code.
- Write clean, beginner-friendly Python code for machine learning tasks with clear comments and simple structure.
Use only these libraries: NumPy, Pandas, Matplotlib, Scikit-learn, XGBoost, Seaborn, Imblearn, SciPy, Pickle, regex, LightGBM, Plotly, statsmodels, and wordcloud.
Avoid unnecessary complexity, ensure code is correct and runnable, and explain steps briefly where needed.
"""

# --- HELPERS ---

def load_env():
    """Load .env file manually"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# --- PLATFORM HELPER ---
def get_platform():
    if sys.platform.startswith('win'): return 'win'
    if sys.platform.startswith('darwin'): return 'mac'
    return 'linux'

PLATFORM = get_platform()

def _detect_linux_display_server():
    """Detect whether running on Wayland or X11."""
    wayland_display = os.environ.get('WAYLAND_DISPLAY', '')
    xdg_session = os.environ.get('XDG_SESSION_TYPE', '').lower()
    if wayland_display or xdg_session == 'wayland':
        return 'wayland'
    return 'x11'

def _run(cmd, input_data=None, timeout=3):
    """Run a command, return (stdout, returncode). Never raises."""
    try:
        result = subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            timeout=timeout
        )
        return result.stdout, result.returncode
    except FileNotFoundError:
        return b'', 127  # command not found
    except subprocess.TimeoutExpired:
        return b'', 1
    except Exception:
        return b'', 1

def _cmd_exists(name):
    out, code = _run(['which', name])
    return code == 0

def clipboard_get():
    try:
        if PLATFORM == 'mac':
            out, code = _run(['pbpaste'])
            return out.decode('utf-8', errors='replace').strip() if code == 0 else ''

        elif PLATFORM == 'win':
            out, code = _run(['powershell.exe', '-command', 'Get-Clipboard'])
            return out.decode('utf-8', errors='replace').strip() if code == 0 else ''

        else:  # Linux — try Wayland first, then X11 tools
            display_server = _detect_linux_display_server()

            if display_server == 'wayland':
                # wl-paste is from the wl-clipboard package
                out, code = _run(['wl-paste', '--no-newline'])
                if code == 0:
                    return out.decode('utf-8', errors='replace').strip()

            # X11 path (also fallback if wl-paste missing)
            if _cmd_exists('xclip'):
                out, code = _run(['xclip', '-selection', 'clipboard', '-o'])
                if code == 0:
                    return out.decode('utf-8', errors='replace').strip()

            if _cmd_exists('xsel'):
                out, code = _run(['xsel', '--clipboard', '--output'])
                if code == 0:
                    return out.decode('utf-8', errors='replace').strip()

            return ''

    except Exception as e:
        print(f"error: {e}")
        return ''

def clipboard_set(text):
    """Set clipboard content — cross-platform with full Linux fallback chain."""
    data = text.encode('utf-8')
    try:
        if PLATFORM == 'mac':
            proc = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            proc.communicate(data)

        elif PLATFORM == 'win':
            ps_cmd = f'Set-Clipboard -Value @\'\n{text}\n\'@'
            subprocess.run(
                ['powershell.exe', '-command', ps_cmd],
                capture_output=True, timeout=5
            )

        else:  # Linux
            display_server = _detect_linux_display_server()
            success = False

            if display_server == 'wayland':
                out, code = _run(['wl-copy'], input_data=data)
                if code == 0:
                    success = True

            if not success and _cmd_exists('xclip'):
                proc = subprocess.Popen(
                    ['xclip', '-selection', 'clipboard', '-i'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                proc.communicate(data, timeout=3)
                if proc.returncode == 0:
                    success = True

            if not success and _cmd_exists('xsel'):
                proc = subprocess.Popen(
                    ['xsel', '--clipboard', '--input'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                proc.communicate(data, timeout=3)
                if proc.returncode == 0:
                    success = True

            if not success:
                print("⚠️ Could not set clipboard. Please install wl-clipboard (Wayland) or xclip/xsel (X11).")

    except Exception as e:
        print(f"error: {e}")

def call_openrouter_api(api_key, prompt):
    """Call OpenRouter API using standard urllib."""
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'HTTP-Referer': 'https://github.com/GarvitOfficial/cheatLikePro',
        'X-Title': 'CheatLikePro_Linux'
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1024
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            try:
                return result['choices'][0]['message']['content'].strip()
            except (KeyError, IndexError):
                return "Error: No answer choices found."

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            err_json = json.loads(error_body)
            msg = err_json.get('error', {}).get('message', str(e))
            return f"API Error {e.code}: {msg}"
        except Exception:
            return f"API Error {e.code}: {error_body}"
    except Exception as e:
        return f"Error: {str(e)}"

# --- MAIN CLASS ---

class ClipboardCheat:
    def __init__(self):
        self.last_clipboard = ""
        self.running = False
        self.processing = False
        self.api_key = None

    def setup(self):
        load_env()
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            print("❌ No OPENROUTER_API_KEY found!")
            print("   Set OPENROUTER_API_KEY in your .env file")
            return False

        # Verify clipboard tools are available before starting
        self._check_clipboard_tools()

        print("🔄 Testing OpenRouter connection...")
        test = call_openrouter_api(self.api_key, "Say 'OK'")
        if "API Error" in test:
            print(f"❌ {test}")
            return False

        print(f"✅ OpenRouter Connection OK!")
        return True

    def _check_clipboard_tools(self):
        """Warn early if no clipboard tool is installed."""
        if PLATFORM != 'linux':
            return
        ds = _detect_linux_display_server()
        has_tool = (
            (ds == 'wayland' and _cmd_exists('wl-copy')) or
            _cmd_exists('xclip') or
            _cmd_exists('xsel')
        )
        if not has_tool:
            if ds == 'wayland':
                print("⚠️ Wayland detected: 'wl-clipboard' is recommended (sudo apt install wl-clipboard).")
            else:
                print("⚠️ X11 detected: 'xclip' or 'xsel' is recommended (sudo apt install xclip).")
            print("   Clipboard read/write may fail until one is installed.\n")
        else:
            if ds == 'wayland' and _cmd_exists('wl-copy'):
                print(f"🖥️ Display: Wayland | Tool: wl-clipboard ✓")
            elif _cmd_exists('xclip'):
                print(f"🖥️ Display: X11 | Tool: xclip ✓")
            elif _cmd_exists('xsel'):
                print(f"🖥️ Display: X11 | Tool: xsel ✓")

    def process_clipboard(self, text):
        self.processing = True
        print(f"📋 Got clipboard text ({len(text)} chars) — querying AI...")

        answer = call_openrouter_api(self.api_key, text)

        if answer and "API Error" not in answer:
            clipboard_set(answer)
            print(f"✅ Answer written to clipboard!")
        else:
            print(f"⚠️ {answer}")

        self.processing = False

    def monitor_loop(self):
        print("👀 Monitoring clipboard... (Ctrl+C to stop)")
        self.last_clipboard = clipboard_get()

        while self.running:
            try:
                current = clipboard_get()

                if (current != self.last_clipboard
                        and len(current) >= MIN_QUESTION_LENGTH
                        and not self.processing):

                    self.last_clipboard = current

                    thread = threading.Thread(
                        target=self.process_clipboard,
                        args=(current,)
                    )
                    thread.daemon = True
                    thread.start()

                    time.sleep(COOLDOWN)

                time.sleep(CHECK_INTERVAL)

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"⚠️ Error: {e}")
                time.sleep(1)

    def start(self):
        print("=" * 50)
        print("🎯 CheatLikePro (Linux & ML Edition)")
        print("=" * 50)

        if not self.setup():
            return

        self.running = True
        try:
            self.monitor_loop()
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            print("\n👋 Stopped!")

if __name__ == "__main__":
    ClipboardCheat().start()
