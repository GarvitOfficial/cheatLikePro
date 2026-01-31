#!/usr/bin/env python3
"""
🎯 CheatLikePro - Clipboard AI Answer Tool
Monitors clipboard, gets answers from OpenRouter (Gemini/DeepSeek/etc), puts them back.
ZERO DEPENDENCIES - Runs with standard Python 3.
"""

import os
import sys
import time
import json
import threading
import subprocess
import urllib.request
import urllib.error

# --- CONFIGURATION ---
# Common models: 
# - upstage/solar-pro-3:free (Free & Good)
# - google/gemini-2.0-flash-001 (Fast & Good)
# - deepseek/deepseek-chat (Cheap & Smart)

MODEL_NAME = os.getenv("MODEL_NAME", "upstage/solar-pro-3:free")
CHECK_INTERVAL = 0.5  # Seconds
MIN_QUESTION_LENGTH = 5
COOLDOWN = 2

# System prompt
SYSTEM_PROMPT = """You are a helpful assistant that provides direct, concise answers.
RULES:
- If the question is about CODE: respond with ONLY the code. No explanations, no comments, no markdown code blocks, just raw code.
- For multiple choice questions: state ONLY the correct option (e.g., "B" or "Option B")
- For calculations: show ONLY the final answer
- For general questions: give a brief, direct answer in 1-2 sentences max
- NEVER add preamble like "Here's the answer" or "Sure!"
- NEVER explain your reasoning unless explicitly asked"""

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

def clipboard_get():
    """Get clipboard content (Cross-platform)"""
    try:
        if PLATFORM == 'mac':
            return subprocess.check_output(['pbpaste'], text=True).strip()
        elif PLATFORM == 'win':
            # Use PowerShell to get clipboard text
            cmd = 'powershell.exe -command "Get-Clipboard"'
            return subprocess.check_output(cmd, shell=True, text=True).strip()
        else: # Linux
            # Try xclip then xsel
            try:
                return subprocess.check_output(['xclip', '-selection', 'clipboard', '-o'], text=True).strip()
            except:
                return subprocess.check_output(['xsel', '-b', '-o'], text=True).strip()
    except Exception:
        return ""

def clipboard_set(text):
    """Set clipboard content (Cross-platform)"""
    try:
        if PLATFORM == 'mac':
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
        elif PLATFORM == 'win':
            # Use clip command
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
            # Windows 'clip' expects CP1252 or UTF-16, but simple ASCII/UTF-8 usually passes through okay-ish
            # or use PowerShell Set-Clipboard for better Unicode support
            process.communicate(text.encode('utf-8')) # simpler method
        else: # Linux
             try:
                process = subprocess.Popen(['xclip', '-selection', 'clipboard', '-i'], stdin=subprocess.PIPE)
                process.communicate(text.encode('utf-8'))
             except:
                process = subprocess.Popen(['xsel', '-b', '-i'], stdin=subprocess.PIPE)
                process.communicate(text.encode('utf-8'))
    except Exception as e:
        print(f"⚠️ Clipboard error: {e}")

def call_openrouter_api(api_key, prompt):
    """Call OpenRouter API using standard urllib"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'HTTP-Referer': 'https://github.com/GarvitOfficial/cheatLikePro', # Required by OpenRouter
        'X-Title': 'CheatLikePro'
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
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # Extract text from response (OpenAI format)
            try:
                text = result['choices'][0]['message']['content']
                return text.strip()
            except (KeyError, IndexError):
                return "Error: No answer choices found."
                
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            err_json = json.loads(error_body)
            msg = err_json.get('error', {}).get('message', str(e))
            return f"API Error {e.code}: {msg}"
        except:
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
            print("❌ No OpenRouter API key found!")
            print("   Set OPENROUTER_API_KEY in .env file")
            print("   Get one at: https://openrouter.ai/keys")
            return False
        
        # Simple test
        print("🔄 Testing OpenRouter connection...")
        test = call_openrouter_api(self.api_key, "Say 'OK'")
        if "Error" in test and "API Error" in test:
            print(f"❌ {test}")
            return False
            
        print(f"✅ API Connection OK! (Model: {MODEL_NAME})")
        return True
    
    def process_clipboard(self, text):
        self.processing = True
        print(f"📋 Question: {text[:50]}...")
        
        answer = call_openrouter_api(self.api_key, text)
        
        if answer and "API Error" not in answer:
            clipboard_set(answer)
            print(f"✅ Answer copied! ({len(answer)} chars)")
        else:
            print(f"⚠️  {answer}")
        
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
                    
                    # Process in background
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
        print("🎯 CheatLikePro - ZERO DEPENDENCY MODE (OpenRouter)")
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
