# Auto Clicker with Random Delay

This script simulates mouse clicks at a specific screen location every 5 to 15 seconds. It's useful for keeping a 
window active or simulating user interaction.

## Features
- Captures your mouse position after a 10-second delay.
- Clicks at that position repeatedly with a random delay between 5 and 20 seconds.
- Runs until you stop it manually (Ctrl+C).

## Motivation:
Many online training platforms require users to periodically interact with the screen—like clicking a button—to 
confirm they are actively watching. This can be frustrating when the content is passive or when the user wants to multitask.

The Auto Clicker with Random Delay was created to solve this problem by simulating human-like interaction. It 
automatically clicks at a specified location on the screen at random intervals, helping keep the session active 
without constant manual input. This allows users to stay compliant with platform requirements while freeing up 
their time for other tasks.

## How to Run the script:
1. `python autoClickonScreen\run.py`
1. Move your mouse to the desired click location within 10 seconds.
2. The script will start clicking at that position at random intervals between 5 to 20 seconds.
3. Press Ctrl+C to stop the script.

## Requirements
- Python 3
- `pyautogui` library

## Installation
Install the required library using: 
`pip install pyautogui`
