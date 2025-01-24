# slandroid/tool.py
import subprocess
import sys
import os
import shutil
from pathlib import Path

# Mapping of file extensions to their respective language interpreters
LANGUAGE_MAPPING = {
    # Python
    ".py": {"command": "python", "install": "pip install"},
    
    # JavaScript (Node.js)
    ".js": {"command": "node", "install": "npm install -g"},
    
    # Bash
    ".sh": {"command": "bash", "install": None},
    
    # Ruby
    ".rb": {"command": "ruby", "install": "gem install"},
    
    # Java (requires compilation first)
    ".java": {"command": "java", "install": None},
    
    # Go
    ".go": {"command": "go run", "install": "go install"},
    
    # PHP
    ".php": {"command": "php", "install": "sudo apt install php"},
    
    # Perl
    ".pl": {"command": "perl", "install": "sudo apt install perl"},
    
    # C (requires compilation)
    ".c": {"command": "gcc", "install": "sudo apt install gcc"},
    
    # C++ (requires compilation)
    ".cpp": {"command": "g++", "install": "sudo apt install g++"},
    
    # Rust
    ".rs": {"command": "rustc", "install": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"},
    
    # TypeScript (requires compilation to JavaScript)
    ".ts": {"command": "ts-node", "install": "npm install -g ts-node"},
    
    # PowerShell
    ".ps1": {"command": "pwsh", "install": "sudo apt install powershell"},
    
    # Lua
    ".lua": {"command": "lua", "install": "sudo apt install lua5.3"},
    
    # R
    ".r": {"command": "Rscript", "install": "sudo apt install r-base"},
    
    # Swift
    ".swift": {"command": "swift", "install": "sudo apt install swift"},
    
    # Kotlin
    ".kt": {"command": "kotlin", "install": "sudo apt install kotlin"},
    
    # Dart
    ".dart": {"command": "dart", "install": "sudo apt install dart"},
    
    # Haskell
    ".hs": {"command": "runhaskell", "install": "sudo apt install haskell-platform"},
    
    # Elixir
    ".exs": {"command": "elixir", "install": "sudo apt install elixir"},
    
    # Add more languages as needed
}

def detect_language(script_path):
    """Detect the language based on the file extension."""
    ext = Path(script_path).suffix
    return LANGUAGE_MAPPING.get(ext)

def install_interpreter(language_info):
    """Install the required interpreter or runtime."""
    if language_info["install"]:
        print(f"Installing {language_info['command']}...")
        try:
            subprocess.run(language_info["install"].split(), check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {language_info['command']}: {e}")
            return False
    return True

def run_script(script_path):
    """Run the script using the appropriate interpreter."""
    language_info = detect_language(script_path)
    if not language_info:
        print(f"Unsupported file type: {Path(script_path).suffix}")
        return

    # Check if the interpreter is installed
    if not shutil.which(language_info["command"].split()[0]):
        print(f"{language_info['command']} is not installed.")
        if not install_interpreter(language_info):
            print(f"Please install {language_info['command']} manually and try again.")
            return

    # Run the script
    try:
        command = language_info["command"].split() + [script_path]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")
    except FileNotFoundError:
        print(f"Script file not found: {script_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: slandroid <script_path>")
    else:
        run_script(sys.argv[1])

if __name__ == "__main__":
    main()