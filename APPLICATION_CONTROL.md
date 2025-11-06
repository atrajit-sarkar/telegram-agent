# Application Control Features

## Overview
The Telegram bot now has powerful application control capabilities that allow you to:
- Open and close applications on your PC
- Control keyboard and mouse inputs
- Automate tasks within applications
- Monitor running processes

## 🚀 Application Management

### Open Application
Open any installed application on your PC.

**Examples:**
- "Open Notepad"
- "Launch Chrome"
- "Open Visual Studio Code"
- "Open notepad and open C:/file.txt"

**Function:** `open_application(application_name, file_path=None)`

### Close Application
Close running applications by process name.

**Examples:**
- "Close Notepad"
- "Close Chrome"
- "Kill notepad.exe"

**Function:** `close_application(process_name)`

### List Running Processes
See what applications are currently running.

**Examples:**
- "What apps are running?"
- "List all processes"
- "Show running applications"

**Function:** `list_running_processes()`

## ⌨️ Keyboard Control

### Type Text
Type text into the currently focused application.

**Examples:**
- "Type 'Hello World' in the active window"
- "Write 'This is a test' in notepad"

**Function:** `type_text(text, interval=0.1)`

### Press Keys
Press individual keyboard keys.

**Examples:**
- "Press Enter"
- "Press Tab 3 times"
- "Press F5"
- "Press Backspace"

**Function:** `press_key(key, presses=1, interval=0.1)`

**Supported keys:** enter, tab, space, backspace, delete, esc, f1-f12, up, down, left, right, etc.

### Press Hotkeys
Execute keyboard shortcuts.

**Examples:**
- "Press Ctrl+C" (Copy)
- "Press Ctrl+V" (Paste)
- "Press Ctrl+S" (Save)
- "Press Alt+Tab" (Switch window)
- "Press Ctrl+Shift+Esc" (Task Manager)

**Function:** `press_hotkey(*keys)`

## 🖱️ Mouse Control

### Click Mouse
Click at specific coordinates or current position.

**Examples:**
- "Click at position 500, 300"
- "Double click at 100, 200"
- "Right click at current position"

**Function:** `click_mouse(x=None, y=None, button='left', clicks=1)`

**Button options:** 'left', 'right', 'middle'

### Move Mouse
Move the cursor to specific coordinates.

**Examples:**
- "Move mouse to 800, 600"
- "Move cursor to top-left corner"

**Function:** `move_mouse(x, y, duration=0.5)`

### Scroll Mouse
Scroll up or down in the active window.

**Examples:**
- "Scroll down 5 times"
- "Scroll up 3 clicks"

**Function:** `scroll_mouse(clicks, direction='down')`

### Get Mouse Position
Find out where the cursor is currently located.

**Examples:**
- "Where is my mouse?"
- "Get cursor position"

**Function:** `get_mouse_position()`

### Get Screen Size
Get your screen resolution.

**Examples:**
- "What's my screen resolution?"
- "Get screen size"

**Function:** `get_screen_size()`

## 🎯 Practical Use Cases

### 1. Automated Note Taking
```
"Open Notepad, type 'Meeting Notes', press Enter twice, and type 'Date: Today'"
```

### 2. Quick Screenshot and Save
```
"Take a screenshot, open Paint, press Ctrl+V, and save it"
```

### 3. Application Workflow
```
"Open Chrome, wait 2 seconds, type 'github.com', and press Enter"
```

### 4. File Operations
```
"Open file explorer, press Ctrl+A to select all, and press Delete"
```

### 5. Task Management
```
"List running processes, close chrome.exe, and open Firefox"
```

### 6. Text Editing Automation
```
"Open VS Code with C:/project/main.py, press Ctrl+End to go to bottom, and type a new function"
```

## ⚠️ Important Notes

### Safety Considerations
- **Be careful with automation**: Mouse/keyboard actions happen on the actual PC
- **Add delays**: For complex workflows, add pauses between actions for reliability
- **Test carefully**: Start with simple commands before complex automation
- **Monitor actions**: Watch what's happening on your PC during automation

### Timing Tips
- Applications need time to open (~2-5 seconds)
- Use appropriate intervals between keypresses (default 0.1s)
- Add delays between mouse movements and clicks
- Wait for windows to fully load before interacting

### Common Applications

**Windows Built-in:**
- `notepad` - Notepad
- `calc` - Calculator
- `mspaint` - Paint
- `explorer` - File Explorer
- `cmd` - Command Prompt

**Common Third-party:**
- `chrome` - Google Chrome
- `firefox` - Firefox
- `code` - VS Code
- `outlook` - Outlook

**Full Path Example:**
```
"C:/Program Files/Application/app.exe"
```

## 🔧 Technical Details

### PyAutoGUI Integration
All keyboard and mouse functions use PyAutoGUI, which is already installed in your environment.

### Process Control
- Windows: Uses `tasklist` and `taskkill` commands
- Linux/Mac: Uses `ps` and `pkill` commands

### Error Handling
All functions return a dictionary with:
- `status`: "success" or "error"
- `message`: Description of what happened
- Additional data specific to the function

## 📝 Example Conversation

**You:** "Open Notepad and write a todo list"

**Bot:** 
1. Opens Notepad
2. Types "TODO LIST"
3. Presses Enter twice
4. Types "1. Review code"
5. Confirms completion

**You:** "Take a screenshot and show me mouse position"

**Bot:**
1. Captures screenshot
2. Gets current mouse coordinates (e.g., "245, 532")
3. Sends screenshot file

## 🚀 Getting Started

Just talk naturally to the bot! Examples:
- "Open calculator"
- "Type hello in the active window"
- "Click at the center of the screen"
- "Press Ctrl+C then Ctrl+V"
- "What's running on my PC?"

The AI will understand your intent and execute the appropriate commands!
