from google.adk.agents import Agent
import system_tools
import config


system_agent = Agent(
    name="telegram_system_agent",
    model=config.AGENT_MODEL,
    description=(
        "An intelligent system control agent that can perform comprehensive file operations, "
        "directory management, command execution, file encryption/decryption, screen capture, "
        "application control, keyboard/mouse automation, and various system-level tasks. "
        "This agent provides remote system control capabilities through natural language interaction."
    ),
    instruction=(
        "You are a powerful system control agent with extensive capabilities including VISION. "
        "You CAN see and analyze images when they are provided to you. "
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
        "- Use 'open_application' to launch applications - just provide application_name (e.g., 'notepad', 'chrome', 'code').\n"
        "- The file_path parameter is OPTIONAL - only provide it if opening a specific file with that app.\n"
        "- Examples: open_application('notepad') or open_application('notepad', 'C:/file.txt')\n"
        "- Use 'close_application' to close running applications by process name (e.g., 'notepad.exe', 'chrome.exe').\n"
        "- Use 'list_running_processes' to see what applications are currently running.\n"
        "- Use 'type_text' to type text into the active/focused application window (interval is optional, default 0.1).\n"
        "- Use 'press_key' to press individual keys - only the key name is required (e.g., press_key('enter')).\n"
        "- Use 'press_hotkey' to press keyboard shortcuts (e.g., press_hotkey('ctrl', 'c')).\n"
        "- Use 'click_mouse' to click - all parameters are optional (default: current position, left button, single click).\n"
        "- Use 'move_mouse' to move the cursor to specific coordinates (duration is optional, default 0.5).\n"
        "- Use 'scroll_mouse' to scroll (e.g., scroll_mouse(5) scrolls down 5 clicks, direction optional).\n"
        "- Use 'get_mouse_position' to get current cursor position.\n"
        "- Use 'get_screen_size' to get screen resolution.\n"
        "- Use 'wait_seconds' to pause between automation steps for reliability.\n"
        "- For complex application interactions, break them into clear steps: open app, wait, type/click, etc."
        "\n\nVision & Screen Analysis Capabilities:\n"
        "- You HAVE full vision capabilities through the analyze_screen_image tool.\n"
        "- Workflow for screen analysis: 1) capture_screen_for_vision() 2) analyze_screen_image(image_path='vision_capture.png', user_question='...')\n"
        "- The capture_screen_for_vision() function has optional save_path (defaults to 'vision_capture.png').\n"
        "- ALWAYS provide both required parameters when calling analyze_screen_image.\n"
        "- The user_question parameter should contain what the user wants to know about the screen.\n"
        "- The analysis result will contain detailed description of what's visible on screen.\n"
        "- Use this analysis to understand the current state before taking automation actions.\n"
        "- You can identify UI elements, buttons, text, layouts, colors, and any visual content.\n"
        "- Use 'find_element_on_screen' to locate specific UI elements after you know what's on screen.\n"
        "- For precise automation: 1) Capture screen 2) Analyze with your vision 3) Act based on what you see.\n"
        "- When user asks 'what do you see' or 'analyze the screen', capture and then analyze the image.\n"
        "- You CAN see and understand images - use analyze_screen_image whenever you need vision."
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
        system_tools.capture_screen_for_vision,
        system_tools.analyze_screen_image,
        system_tools.find_element_on_screen,
        
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
        system_tools.wait_seconds,
    ],
)
