#!/usr/bin/env python3
"""
setup_tools.py: Cross-platform installer for development tools (NVM, SDKMAN, Go, Docker, DBeaver, WezTerm, Tmux, no-mistakes, Fonts) 
and macOS apps (Maccy, Rectangle, OpenSuperWhisper) with startup & language configuration.
"""

import sys
import os
import shutil
import stat
import subprocess
from pathlib import Path

# Terminal Colors
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"

def print_info(msg):
    print(f"  {Colors.BLUE}➔{Colors.RESET} {msg}")

def print_success(msg):
    print(f"  {Colors.GREEN}✔{Colors.RESET} {Colors.DIM}{msg}{Colors.RESET}")

def print_warn(msg):
    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {msg}")

def print_error(msg):
    print(f"  {Colors.RED}✖{Colors.RESET} {msg}")

def run_cmd(cmd, shell=False, check=False):
    try:
        res = subprocess.run(cmd, shell=shell, capture_output=True, text=True, check=check)
        return res.returncode == 0, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def install_nvm():
    home = Path.home()
    nvm_dir = home / ".nvm"
    print_info("Checking Node Version Manager (NVM)...")

    if nvm_dir.exists():
        print_success("NVM is already installed at ~/.nvm")
        return

    if sys.platform in ["darwin", "linux"]:
        print_info("Installing NVM via official script...")
        cmd = "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash"
        ok, out, err = run_cmd(cmd, shell=True)
        if ok or nvm_dir.exists():
            print_success("NVM installed successfully at ~/.nvm")
        else:
            print_error(f"Failed to install NVM: {err}")
    elif sys.platform == "win32":
        print_info("Installing NVM for Windows via winget...")
        ok, out, err = run_cmd(["winget", "install", "CoreyButler.NVMforWindows", "--silent"])
        if ok:
            print_success("NVM for Windows installed successfully.")
        else:
            print_warn("Could not auto-install NVM for Windows. Please install manually.")

def install_sdkman():
    home = Path.home()
    sdkman_dir = home / ".sdkman"
    print_info("Checking Java Version Manager (SDKMAN!)...")

    if sdkman_dir.exists():
        print_success("SDKMAN! is already installed at ~/.sdkman")
        return

    if sys.platform in ["darwin", "linux"]:
        print_info("Installing SDKMAN! via official script...")
        cmd = 'curl -s "https://get.sdkman.io" | bash'
        ok, out, err = run_cmd(cmd, shell=True)
        if ok or sdkman_dir.exists():
            print_success("SDKMAN! installed successfully at ~/.sdkman")
        else:
            print_error(f"Failed to install SDKMAN!: {err}")
    elif sys.platform == "win32":
        print_warn("SDKMAN! requires WSL or Git Bash on Windows.")

def install_golang():
    print_info("Checking Golang (Go)...")
    has_go = shutil.which("go") is not None

    if has_go:
        ok, out, _ = run_cmd(["go", "version"])
        if ok:
            print_success(f"Golang is already installed ({out})")
            return

    if sys.platform == "darwin":
        brew_bin = shutil.which("brew") or "/opt/homebrew/bin/brew"
        if os.path.exists(brew_bin):
            print_info("Installing Golang via Homebrew...")
            ok, out, err = run_cmd([brew_bin, "install", "go"])
            if ok:
                print_success("Golang installed successfully via Homebrew.")
            else:
                print_error(f"Failed to install Go via Homebrew: {err}")
        else:
            print_error("Homebrew is required to install Go on macOS.")
    elif sys.platform == "linux":
        print_info("Installing Golang via package manager...")
        run_cmd("sudo apt-get update && sudo apt-get install -y golang", shell=True)
    elif sys.platform == "win32":
        run_cmd(["winget", "install", "GoLang.Go", "--silent"])

def install_docker():
    print_info("Checking Docker...")
    has_docker = shutil.which("docker") is not None or os.path.exists("/Applications/Docker.app")
    
    if has_docker:
        print_success("Docker is already installed.")
        return

    if sys.platform == "darwin":
        brew_bin = shutil.which("brew") or "/opt/homebrew/bin/brew"
        if os.path.exists(brew_bin):
            print_info("Installing Docker via Homebrew Cask...")
            ok, out, err = run_cmd([brew_bin, "install", "--cask", "docker"])
            if ok:
                print_success("Docker installed successfully.")
            else:
                print_error(f"Failed to install Docker: {err}")
    elif sys.platform == "linux":
        print_info("Installing Docker via official script...")
        run_cmd("curl -fsSL https://get.docker.com | sh", shell=True)
    elif sys.platform == "win32":
        run_cmd(["winget", "install", "Docker.DockerDesktop", "--silent"])

def install_dbeaver():
    print_info("Checking DBeaver...")
    has_dbeaver = shutil.which("dbeaver") is not None or os.path.exists("/Applications/DBeaver.app")
    
    if has_dbeaver:
        print_success("DBeaver is already installed.")
        return

    if sys.platform == "darwin":
        brew_bin = shutil.which("brew") or "/opt/homebrew/bin/brew"
        if os.path.exists(brew_bin):
            print_info("Installing DBeaver via Homebrew Cask...")
            ok, out, err = run_cmd([brew_bin, "install", "--cask", "dbeaver-community"])
            if ok:
                print_success("DBeaver installed successfully.")
            else:
                print_error(f"Failed to install DBeaver: {err}")
    elif sys.platform == "linux":
        run_cmd("sudo snap install dbeaver-ce", shell=True)
    elif sys.platform == "win32":
        run_cmd(["winget", "install", "dbeaver.dbeaver", "--silent"])

def install_wezterm():
    print_info("Checking WezTerm...")
    has_wezterm = shutil.which("wezterm") is not None or os.path.exists("/Applications/WezTerm.app")
    
    if has_wezterm:
        print_success("WezTerm is already installed.")
        return

    if sys.platform == "darwin":
        brew_bin = shutil.which("brew") or "/opt/homebrew/bin/brew"
        if os.path.exists(brew_bin):
            print_info("Installing WezTerm via Homebrew Cask...")
            ok, out, err = run_cmd([brew_bin, "install", "--cask", "wezterm"])
            if ok or os.path.exists("/Applications/WezTerm.app"):
                print_success("WezTerm installed successfully.")
            else:
                print_error(f"Failed to install WezTerm: {err or out}")
        else:
            print_error("Homebrew is required to install WezTerm on macOS.")
    elif sys.platform == "linux":
        print_info("Installing WezTerm via package manager...")
        run_cmd("curl -fsSL https://apt.fury.io/wez/gpg.key | sudo gpg --yes --dearmor -o /etc/apt/trusted.gpg.d/wezterm-fury.gpg && echo 'deb https://apt.fury.io/wez/ * *' | sudo tee /etc/apt/sources.list.d/wezterm.list && sudo apt-get update && sudo apt-get install -y wezterm", shell=True)
    elif sys.platform == "win32":
        run_cmd(["winget", "install", "wez.wezterm", "--silent"])

def install_tmux():
    print_info("Checking tmux...")
    has_tmux = shutil.which("tmux") is not None

    if has_tmux:
        ok, out, _ = run_cmd(["tmux", "-V"])
        if ok:
            print_success(f"tmux is already installed ({out})")
            return

    if sys.platform == "darwin":
        brew_bin = shutil.which("brew") or "/opt/homebrew/bin/brew"
        if os.path.exists(brew_bin):
            print_info("Installing tmux via Homebrew...")
            ok, out, err = run_cmd([brew_bin, "install", "tmux"])
            if ok or shutil.which("tmux"):
                print_success("tmux installed successfully via Homebrew.")
            else:
                print_error(f"Failed to install tmux: {err or out}")
        else:
            print_error("Homebrew is required to install tmux on macOS.")
    elif sys.platform == "linux":
        print_info("Installing tmux via package manager...")
        run_cmd("sudo apt-get update && sudo apt-get install -y tmux", shell=True)
    elif sys.platform == "win32":
        run_cmd(["winget", "install", "tmux.tmux", "--silent"])

def install_no_mistakes():
    print_info("Checking no-mistakes...")
    home = Path.home()
    target_bin = home / "bin" / "no-mistakes"
    bin_in_path = shutil.which("no-mistakes")

    if bin_in_path or target_bin.exists():
        bin_file = str(bin_in_path or target_bin)
        ok, out, _ = run_cmd([bin_file, "--version"])
        if ok:
            print_success(f"no-mistakes is already installed ({out})")
            return

    no_mistakes_bin = home / ".no-mistakes" / "bin" / "no-mistakes"
    if not no_mistakes_bin.exists():
        print_info("Installing no-mistakes via official script...")
        run_cmd("curl -fsSL https://raw.githubusercontent.com/kunchenguid/no-mistakes/main/docs/install.sh | sh", shell=True)

    if not no_mistakes_bin.exists() and shutil.which("go"):
        print_info("Building no-mistakes via `go install`...")
        run_cmd("go install github.com/kunchenguid/no-mistakes/cmd/no-mistakes@latest", shell=True)

    src_bin = None
    if no_mistakes_bin.exists():
        src_bin = no_mistakes_bin
    elif (home / "go" / "bin" / "no-mistakes").exists():
        src_bin = home / "go" / "bin" / "no-mistakes"

    if src_bin:
        target_bin.parent.mkdir(parents=True, exist_ok=True)
        if target_bin.exists() or target_bin.is_symlink():
            target_bin.unlink(missing_ok=True)
        shutil.copy2(src_bin, target_bin)
        target_bin.chmod(target_bin.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print_success(f"Installed no-mistakes binary to {target_bin}")
    else:
        print_warn("no-mistakes installation could not be verified automatically.")

def install_fonts():
    print_info("Checking Hack Nerd Font...")
    if sys.platform == "darwin":
        user_font = Path.home() / "Library" / "Fonts" / "HackNerdFont-Regular.ttf"
        system_font = Path("/Library/Fonts/HackNerdFont-Regular.ttf")
        if user_font.exists() or system_font.exists():
            print_success("Hack Nerd Font is already installed.")
            return

        brew_bin = shutil.which("brew") or "/opt/homebrew/bin/brew"
        if os.path.exists(brew_bin):
            print_info("Installing font-hack-nerd-font via Homebrew Cask...")
            ok, out, err = run_cmd([brew_bin, "install", "--cask", "font-hack-nerd-font"])
            if ok or user_font.exists():
                print_success("Hack Nerd Font installed successfully.")
            else:
                print_warn(f"Cask install for font-hack-nerd-font returned: {err or out}")

def install_opensuperwhisper():
    print_info("Checking OpenSuperWhisper...")
    has_app = os.path.exists("/Applications/OpenSuperWhisper.app")

    if not has_app and sys.platform == "darwin":
        brew_bin = shutil.which("brew") or "/opt/homebrew/bin/brew"
        if os.path.exists(brew_bin):
            print_info("Installing OpenSuperWhisper via Homebrew Cask...")
            ok, out, err = run_cmd([brew_bin, "install", "--cask", "opensuperwhisper"])
            if ok or os.path.exists("/Applications/OpenSuperWhisper.app"):
                print_success("OpenSuperWhisper installed successfully.")
            else:
                print_error(f"Failed to install OpenSuperWhisper: {err or out}")
        else:
            print_error("Homebrew is required to install OpenSuperWhisper on macOS.")
    elif has_app:
        print_success("OpenSuperWhisper.app is already installed in /Applications.")

    if sys.platform == "darwin" and os.path.exists("/Applications/OpenSuperWhisper.app"):
        print_info("Configuring OpenSuperWhisper language support (English & Brazilian Portuguese auto-detection)...")
        run_cmd(["defaults", "write", "ru.starmel.OpenSuperWhisper", "whisperLanguage", "-string", "auto"])
        print_success("Configured OpenSuperWhisper language setting ('auto' for English & Brazilian Portuguese).")

        run_cmd(["open", "-a", "OpenSuperWhisper"])

        ok, out, _ = run_cmd(["osascript", "-e", 'tell application "System Events" to get name of every login item'])
        existing_items = [item.strip() for item in out.split(",")] if ok else []

        if "OpenSuperWhisper" in existing_items:
            print_success("OpenSuperWhisper is already configured in macOS startup login items.")
        else:
            apple_script = (
                'tell application "System Events" to make new login item '
                'at end with properties {path:"/Applications/OpenSuperWhisper.app", hidden:false}'
            )
            ok_item, _, err_item = run_cmd(["osascript", "-e", apple_script])
            if ok_item:
                print_success("Added OpenSuperWhisper to macOS startup login items.")
            else:
                print_warn(f"Could not add OpenSuperWhisper to login items: {err_item}")

def setup_mac_apps():
    if sys.platform != "darwin":
        return

    print_info("Checking macOS Productivity Apps (Maccy & Rectangle)...")
    brew_bin = shutil.which("brew") or "/opt/homebrew/bin/brew"
    if not os.path.exists(brew_bin):
        print_warn("Homebrew not found. Cannot install Maccy/Rectangle casks.")
        return

    # 1. Install Casks
    casks = ["maccy", "rectangle"]
    for cask in casks:
        app_name = cask.capitalize()
        app_path = Path(f"/Applications/{app_name}.app")
        if not app_path.exists():
            print_info(f"Installing {app_name} via Homebrew Cask...")
            ok, out, err = run_cmd([brew_bin, "install", "--cask", cask])
            if ok:
                print_success(f"{app_name} installed successfully.")
            else:
                print_warn(f"Cask install for {app_name} returned: {err or out}")
        else:
            print_success(f"{app_name}.app is already installed in /Applications.")

    # 2. Ensure apps are running
    for app in ["Maccy", "Rectangle"]:
        run_cmd(["open", "-a", app])

    # 3. Add to macOS Login Items (Startup)
    print_info("Configuring startup login items for Maccy & Rectangle...")
    ok, out, _ = run_cmd(["osascript", "-e", 'tell application "System Events" to get name of every login item'])
    existing_items = [item.strip() for item in out.split(",")] if ok else []

    for app in ["Maccy", "Rectangle"]:
        if app in existing_items:
            print_success(f"{app} is already configured in macOS startup login items.")
        else:
            app_path = f"/Applications/{app}.app"
            if os.path.exists(app_path):
                apple_script = (
                    f'tell application "System Events" to make new login item '
                    f'at end with properties {{path:"{app_path}", hidden:false}}'
                )
                ok_item, _, err_item = run_cmd(["osascript", "-e", apple_script])
                if ok_item:
                    print_success(f"Added {app} to macOS startup login items.")
                else:
                    print_warn(f"Could not add {app} to login items: {err_item}")

def main():
    install_nvm()
    install_sdkman()
    install_golang()
    install_docker()
    install_dbeaver()
    install_wezterm()
    install_tmux()
    install_no_mistakes()
    install_fonts()
    install_opensuperwhisper()
    setup_mac_apps()

if __name__ == "__main__":
    main()
