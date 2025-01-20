#!/usr/bin/env python
#This is a cli fzf version of the qubes-prompt pip package
#copyright (c) 2025 Ubuntupunk

import sys
import json
import subprocess
import webbrowser
import urllib.parse
import os

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def colorize(text, color_code):
    """Apply color code to text if output is a tty."""
    if os.isatty(sys.stdout.fileno()):
        return f"{color_code}{text}{RESET}"
    return text

def check_fzf_installed():
    """Check if fzf is available in the system."""
    try:
        subprocess.run(['which', 'fzf'], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_package_manager_instructions():
    """Return installation instructions for various package managers."""
    instructions = f"""
    {colorize("FZF is not installed. Please install it using one of the following methods:", RED + BOLD)}

    {colorize("For Debian/Ubuntu:", BLUE)}
    sudo apt update && sudo apt install fzf

    {colorize("For Arch Linux:", BLUE)}
    sudo pacman -S fzf

    {colorize("For Fedora:", BLUE)}
    sudo dnf install fzf

    {colorize("For macOS:", BLUE)}
    brew install fzf

    {colorize("Alternative methods:", GREEN)}
    1. Using Git:
    git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
    ~/.fzf/install

    2. Using Python pip:
    pip install fzf

    {colorize("Please install fzf and try again.", RED + BOLD)}
"""
    return instructions

def load_qubes_commands(file_path):
    """Load Qubes commands from a JSON file."""
    package_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(package_dir, 'db', 'commands.json')
    with open(full_path, 'r') as file:
        return json.load(file)

def format_commands_for_fzf(commands):
    """Format commands for fzf."""
    formatted_commands = []
    for command in commands:
        formatted_commands.append(f"{command['name']} | {command['command']} | {command['options']} | {urllib.parse.unquote(command['description'])} ")
    return formatted_commands

def execute_fzf(commands):
    """Execute fzf and return the selected command."""
    if not check_fzf_installed():
        print(get_package_manager_instructions())
        sys.exit(1)
    process = subprocess.Popen(['fzf', '--height', '40%', '--layout=reverse', '--border'],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)

    output, _ = process.communicate('\n'.join(commands))
    return output.strip() if output else None

def open_qubes_command_url(selected_command):
    """Open the URL associated with the selected command."""
    if not selected_command:
        return
    print(f"Processing selected command: {selected_command}")  # Debug print
    parts = selected_command.split(" | ")
    print(f"Split parts: {parts}")  # Debug print
    if len(parts) != 4:
        print("Invalid command format")
        return
    
    # Extract the command name from the selected command
    command_name = parts[0]
    
    # Construct the path to the qubes.md file
    package_dir = os.path.dirname(os.path.abspath(__file__))
    qubes_md_path = os.path.join(package_dir, 'assets', 'qubes.md')

    # Construct the URL using the command name
    url = f"file://{qubes_md_path}#contents#{command_name.lower().replace(' ', '-')}"
    print(f"Opening URL: {url}")  # Debug print
    subprocess.run(['xdg-open', url])

def main():
    qubes_commands = load_qubes_commands('commands.json')
    formatted_commands = format_commands_for_fzf(qubes_commands)
    selected_command_fzf = execute_fzf(formatted_commands)
    if selected_command_fzf:
        open_qubes_command_url(selected_command_fzf)
    else:
        print("No command selected from fzf")

if __name__ == "__main__":
    main()
