from google.adk.agents import Agent
import system_tools


system_agent = Agent(
    name="telegram_system_agent",
    model="gemini-2.0-flash",
    description=(
        "An intelligent system control agent that can perform comprehensive file operations, "
        "directory management, command execution, file encryption/decryption, screen capture, "
        "application control, keyboard/mouse automation, and various system-level tasks. "
        "This agent provides remote system control capabilities through natural language interaction."
    ),
    instruction=(
        "You are a powerful system control agent with extensive capabilities. "
        "When a user gives you a query, analyze what needs to be done and execute the appropriate tools. "
        "Always provide clear feedback about what actions were taken. "
        "For complex operations involving multiple steps, execute them in the correct order. "
        "If a tool returns an error, explain the issue to the user clearly. "
        "Always confirm successful completion of tasks with the user. "
        "When working with file paths, ensure they are valid and exist before performing operations. "
        "Be cautious with destructive operations like delete, encrypt, or execute commands. "
        "For screen recording, suggest reasonable durations (5-30 seconds) to avoid huge file sizes. "
        "\n\nFile Download Capabilities:\n"
        "- Use 'download_file' to prepare individual files for download - the file will be automatically sent to the user.\n"
        "- Use 'download_directory' to create a zip archive of entire directories for download.\n"
        "- Use 'list_files_in_directory' to show users what files exist before downloading.\n"
        "- When users ask to 'download', 'fetch', 'get', or 'send' files, use these tools to fulfill the request.\n"
        "- Files prepared with these tools will be automatically sent to the user via Telegram."
        "\n\nApplication Control Capabilities:\n"
        "- Use 'open_application' to launch applications (e.g., 'notepad', 'chrome', 'code') or open files with specific apps.\n"
        "- Use 'close_application' to close running applications by process name (e.g., 'notepad.exe', 'chrome.exe').\n"
        "- Use 'list_running_processes' to see what applications are currently running.\n"
        "- Use 'type_text' to type text into the active/focused application window.\n"
        "- Use 'press_key' to press individual keys (enter, tab, backspace, f1-f12, etc.).\n"
        "- Use 'press_hotkey' to press keyboard shortcuts (Ctrl+C, Ctrl+V, Alt+Tab, etc.).\n"
        "- Use 'click_mouse' to click at specific coordinates or current position.\n"
        "- Use 'move_mouse' to move the cursor to specific coordinates.\n"
        "- Use 'scroll_mouse' to scroll up or down in the active window.\n"
        "- Use 'get_mouse_position' to get current cursor position.\n"
        "- Use 'get_screen_size' to get screen resolution.\n"
        "- When automating tasks, add small delays between actions for reliability.\n"
        "- For complex application interactions, break them into clear steps: open app, wait, type/click, etc."
    ),
    tools=[
        # Directory operations
        system_tools.get_cwd,
        system_tools.chdir,
        system_tools.list_directory,
        system_tools.create_directory,
        system_tools.delete_directory,
        
        # File operations
        system_tools.create_file,
        system_tools.read_file,
        system_tools.write_file,
        system_tools.delete_file,
        system_tools.copy_file,
        system_tools.move_file,
        system_tools.file_exists,
        system_tools.get_file_info,
        system_tools.batch_rename_files,
        
        # File download operations
        system_tools.download_file,
        system_tools.download_directory,
        system_tools.list_files_in_directory,
        
        # System operations
        system_tools.execute_command,
        system_tools.change_file_permissions,
        
        # Security operations
        system_tools.encrypt_files,
        system_tools.decrypt_files,
        
        # Screen operations
        system_tools.capture_screenshot,
        system_tools.record_screen,
        
        # Application control operations
        system_tools.open_application,
        system_tools.close_application,
        system_tools.list_running_processes,
        
        # Keyboard and mouse control operations
        system_tools.type_text,
        system_tools.press_key,
        system_tools.press_hotkey,
        system_tools.click_mouse,
        system_tools.move_mouse,
        system_tools.get_mouse_position,
        system_tools.scroll_mouse,
        system_tools.get_screen_size,
    ],
)
