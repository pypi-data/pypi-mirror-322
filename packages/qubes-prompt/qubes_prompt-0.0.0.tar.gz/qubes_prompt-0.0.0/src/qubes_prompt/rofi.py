#!/usr/bin/env python
#This is the rofi_qubes launcher script from the qubes-prompt pip package
#copyright (c) 2025 Ubuntupunk

import sys
import os
import json
import subprocess
import webbrowser
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

def check_rofi_installed():
    """Check if rofi is available in the system."""
    try:
        subprocess.run(['which', 'rofi'], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_package_manager_instructions():
    """Return installation instructions for various package managers."""
    instructions = f"""
    {colorize("Rofi is not installed.", RED + BOLD)} Please install it using one of the following methods:

    {colorize("For Debian/Ubuntu:", BLUE)}
    sudo apt update && sudo apt install rofi

    {BLUE}For Arch Linux:{RESET}
    sudo pacman -S rofi

    {BLUE}For Fedora:{RESET}
    sudo dnf install rofi

    {BLUE}For macOS:{RESET}
    brew install rofi

    {GREEN}Alternative methods:{RESET}
    1. Using Git:
    git clone https://github.com/davatorium/rofi.git
    cd rofi
    mkdir build && cd build
    ../configure
    make
    sudo make install

    {RED}{BOLD}Please install rofi and try again.{RESET}
"""
    return instructions

def load_qubes_commands(file_path):
    """Load Qubes commands from a JSON file."""
    package_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(package_dir, 'db', 'commands.json')
    with open(full_path, 'r') as file:
        return json.load(file)

qubes_commands = load_qubes_commands('db/commands.json')
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.png") #PLEASE FIX
#print(f"Icon path: {icon_path}")  # Debug print
#print(f"Icon exists: {os.path.exists(icon_path)}")  # Verify file exists

def format_commands_for_rofi(commands):
    """Format commands for rofi."""
    formatted_commands = []
    for command in commands:
        formatted_commands.append(f"{command['name']} | {command['command']} | {command['options']} | {command['description']}")
    return formatted_commands

def execute_rofi(commands):
    """Execute rofi and return the selected command."""
    if not check_rofi_installed():
        print(get_package_manager_instructions())
        sys.exit(1)

    rofi_process = subprocess.Popen(
        ['rofi','-dmenu', '-i', '-show-icons', '-theme-str', f'configuration {{ icon: "{icon_path}"; }}',
         '-theme-str', 'window { width: 50%; }','-theme-str', 'listview { columns: 1; }','-p','QUBES Command:'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = rofi_process.communicate(input='\n'.join(commands))
    if stderr:
        print(f"rofi error: {stderr}")
        return None
    return stdout.strip()

def open_qubes_command_url(selected_command):
    """Open the URL associated with the selected command."""
    if not selected_command:
        return
    parts = selected_command.split(" | ")
    if len(parts) != 4:
        print("Invalid command format")
        return
    description = parts[2]

    # Construct the path to the qubes.md file
    package_dir = os.path.dirname(os.path.abspath(__file__))
    qubes_md_path = os.path.join(package_dir, 'assets', 'qubes.md')

    # Construct the URL to open the qubes.md file with the description as a fragment
    url = f"file://{qubes_md_path}#:{description}"
    subprocess.run(['xdg-open', url])

def main():
    """Main function."""
    qubes_commands = load_qubes_commands('commands.json')
    formatted_commands = format_commands_for_rofi(qubes_commands)
    selected_command_rofi = execute_rofi(formatted_commands)
    if selected_command_rofi:
        open_qubes_command_url(selected_command_rofi)
    else:
        print("No command selected from rofi")

if __name__ == "__main__":
    main()
