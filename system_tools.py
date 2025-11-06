import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Union, List, Dict, Optional
import pyautogui
import cv2
import numpy as np
from cryptography.fernet import Fernet
import google.generativeai as genai

try:
    import mss  # type: ignore
except ImportError:  # pragma: no cover - optional dependency fallback
    mss = None

# Configure Gemini for vision analysis
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


def get_cwd() -> dict:
    """Get the current working directory.
    
    Returns:
        dict: Contains status and current working directory path
    """
    try:
        cwd = os.getcwd()
        return {
            "status": "success",
            "cwd": cwd,
            "message": f"Current directory: {cwd}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get current directory: {str(e)}"
        }


def chdir(directory: str) -> dict:
    """Change the current working directory.
    
    Args:
        directory (str): Path to the directory to change to
        
    Returns:
        dict: Contains status and new current directory
    """
    try:
        os.chdir(directory)
        return {
            "status": "success",
            "cwd": os.getcwd(),
            "message": f"Changed directory to: {os.getcwd()}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to change directory: {str(e)}"
        }


def list_directory(directory: str) -> dict:
    """List all files and folders in the specified directory.
    
    Args:
        directory (str): Directory path to list. Use empty string "" or "." for current directory.
        
    Returns:
        dict: Contains status, list of files and folders
    """
    try:
        path = directory if directory and directory != "" else os.getcwd()
        items = os.listdir(path)
        
        files = []
        folders = []
        
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                folders.append(item)
            else:
                files.append(item)
        
        return {
            "status": "success",
            "path": path,
            "folders": folders,
            "files": files,
            "message": f"Found {len(folders)} folders and {len(files)} files in {path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list directory: {str(e)}"
        }


def read_file(file_path: str) -> dict:
    """Read the contents of a file.
    
    Args:
        file_path (str): Path to the file to read
        
    Returns:
        dict: Contains status and file content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {
            "status": "success",
            "file_path": file_path,
            "content": content,
            "message": f"Successfully read file: {file_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to read file: {str(e)}"
        }


def create_file(file_path: str, content: str) -> dict:
    """Create a new file with specified content.
    
    Args:
        file_path (str): Path where the file should be created
        content (str): Content to write to the file. Use empty string "" for blank file.
        
    Returns:
        dict: Contains status and file path
    """
    try:
        # Create parent directories if they don't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        file_content = content if content is not None else ""

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        
        return {
            "status": "success",
            "file_path": file_path,
            "message": f"Successfully created file: {file_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create file: {str(e)}"
        }


def write_file(file_path: str, content: str) -> dict:
    """Write content to an existing file (overwrites existing content).
    
    Args:
        file_path (str): Path to the file
        content (str): Content to write
        
    Returns:
        dict: Contains status message
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "status": "success",
            "file_path": file_path,
            "message": f"Successfully wrote to file: {file_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to write to file: {str(e)}"
        }


def delete_file(file_path: str) -> dict:
    """Delete a file.
    
    Args:
        file_path (str): Path to the file to delete
        
    Returns:
        dict: Contains status message
    """
    try:
        os.remove(file_path)
        return {
            "status": "success",
            "message": f"Successfully deleted file: {file_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to delete file: {str(e)}"
        }


def delete_directory(dir_path: str) -> dict:
    """Delete a directory and all its contents.
    
    Args:
        dir_path (str): Path to the directory to delete
        
    Returns:
        dict: Contains status message
    """
    try:
        shutil.rmtree(dir_path)
        return {
            "status": "success",
            "message": f"Successfully deleted directory: {dir_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to delete directory: {str(e)}"
        }


def create_directory(dir_path: str) -> dict:
    """Create a new directory.
    
    Args:
        dir_path (str): Path where the directory should be created
        
    Returns:
        dict: Contains status and directory path
    """
    try:
        os.makedirs(dir_path, exist_ok=True)
        return {
            "status": "success",
            "dir_path": dir_path,
            "message": f"Successfully created directory: {dir_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create directory: {str(e)}"
        }


def copy_file(source: str, destination: str) -> dict:
    """Copy a file from source to destination.
    
    Args:
        source (str): Source file path
        destination (str): Destination file path
        
    Returns:
        dict: Contains status message
    """
    try:
        shutil.copy2(source, destination)
        return {
            "status": "success",
            "message": f"Successfully copied {source} to {destination}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to copy file: {str(e)}"
        }


def move_file(source: str, destination: str) -> dict:
    """Move or rename a file.
    
    Args:
        source (str): Source file path
        destination (str): Destination file path
        
    Returns:
        dict: Contains status message
    """
    try:
        shutil.move(source, destination)
        return {
            "status": "success",
            "message": f"Successfully moved {source} to {destination}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to move file: {str(e)}"
        }


def file_exists(file_path: str) -> dict:
    """Check if a file or directory exists.
    
    Args:
        file_path (str): Path to check
        
    Returns:
        dict: Contains status and existence check result
    """
    try:
        exists = os.path.exists(file_path)
        return {
            "status": "success",
            "exists": exists,
            "message": f"Path {'exists' if exists else 'does not exist'}: {file_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to check path existence: {str(e)}"
        }


def execute_command(command: str) -> dict:
    """Execute a shell command and return the output.
    
    Args:
        command (str): Command to execute
        
    Returns:
        dict: Contains status, output, and error (if any)
    """
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output, error = process.communicate()
        
        return {
            "status": "success" if process.returncode == 0 else "error",
            "output": output.strip(),
            "error": error.strip() if error else None,
            "return_code": process.returncode,
            "message": f"Command executed: {command}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to execute command: {str(e)}"
        }


def change_file_permissions(file_path: str, mode: str) -> dict:
    """Change file permissions (chmod).
    
    Args:
        file_path (str): Path to the file
        mode (str): Permission mode in octal format (e.g., '755')
        
    Returns:
        dict: Contains status message
    """
    try:
        permission = int(mode, 8)
        os.chmod(file_path, permission)
        return {
            "status": "success",
            "message": f"Successfully changed permissions of {file_path} to {mode}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to change permissions: {str(e)}"
        }


def encrypt_files(directory: str) -> dict:
    """Encrypt all files in the specified directory (excluding encryption key and script).
    
    Args:
        directory (str): Directory containing files to encrypt. Use empty string "" or "." for current directory.
        
    Returns:
        dict: Contains status and encryption details
    """
    try:
        dir_path = directory if directory and directory != "" else os.getcwd()
        files = []
        
        for file in os.listdir(dir_path):
            full_path = os.path.join(dir_path, file)
            if file not in ["secretkey.key", "encrypt.py", "decrypt.py"] and os.path.isfile(full_path):
                files.append(full_path)
        
        # Generate or load encryption key
        key_path = os.path.join(dir_path, "secretkey.key")
        if not os.path.exists(key_path):
            key = Fernet.generate_key()
            with open(key_path, "wb") as key_file:
                key_file.write(key)
        else:
            with open(key_path, "rb") as key_file:
                key = key_file.read()
        
        # Encrypt files
        encrypted_count = 0
        for file_path in files:
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                encrypted_content = Fernet(key).encrypt(content)
                with open(file_path, "wb") as f:
                    f.write(encrypted_content)
                encrypted_count += 1
            except Exception as e:
                continue
        
        return {
            "status": "success",
            "encrypted_files": encrypted_count,
            "total_files": len(files),
            "message": f"Successfully encrypted {encrypted_count} out of {len(files)} files in {dir_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to encrypt files: {str(e)}"
        }


def decrypt_files(directory: str) -> dict:
    """Decrypt all encrypted files in the specified directory.
    
    Args:
        directory (str): Directory containing files to decrypt. Use empty string "" or "." for current directory.
        
    Returns:
        dict: Contains status and decryption details
    """
    try:
        dir_path = directory if directory and directory != "" else os.getcwd()
        files = []
        
        for file in os.listdir(dir_path):
            full_path = os.path.join(dir_path, file)
            if file not in ["secretkey.key", "encrypt.py", "decrypt.py"] and os.path.isfile(full_path):
                files.append(full_path)
        
        # Load decryption key
        key_path = os.path.join(dir_path, "secretkey.key")
        with open(key_path, "rb") as key_file:
            key = key_file.read()
        
        # Decrypt files
        decrypted_count = 0
        for file_path in files:
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                decrypted_content = Fernet(key).decrypt(content)
                with open(file_path, "wb") as f:
                    f.write(decrypted_content)
                decrypted_count += 1
            except Exception as e:
                continue
        
        return {
            "status": "success",
            "decrypted_files": decrypted_count,
            "total_files": len(files),
            "message": f"Successfully decrypted {decrypted_count} out of {len(files)} files in {dir_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to decrypt files: {str(e)}"
        }


def capture_screenshot(save_path: str = "screenshot.png") -> dict:
    """Capture a screenshot of the current screen.
    
    Args:
        save_path (str): Optional path where the screenshot should be saved. Default is "screenshot.png".
        
    Returns:
        dict: Contains status and file path
    """
    try:
        path = save_path if save_path and save_path != "" else "screenshot.png"

        if mss is not None:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                raw_img = sct.grab(monitor)
                frame = np.array(raw_img)
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                cv2.imwrite(path, frame_bgr)
        else:
            screenshot = pyautogui.screenshot()
            screenshot.save(path)

        return {
            "status": "success",
            "file_path": path,
            "message": f"Screenshot saved to: {path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to capture screenshot: {str(e)}"
        }


def record_screen(duration: int, output_file: str = "screen_recording.mp4") -> dict:
    """Record the screen for a specified duration.
    
    Args:
        duration (int): Duration in seconds to record
        output_file (str): Optional output video file path. Default is "screen_recording.mp4".
        
    Returns:
        dict: Contains status and file path
    """
    try:
        if mss is None:
            return {
                "status": "error",
                "message": (
                    "Screen recording requires the optional 'mss' package. "
                    "Install it with 'pip install mss' and try again."
                )
            }

        codec = cv2.VideoWriter_fourcc(*"mp4v")
        fps = 10.0

        file_path = output_file if output_file and output_file != "" else "recording.mp4"

        with mss.mss() as sct:
            monitor = sct.monitors[1]
            resolution = (monitor["width"], monitor["height"])
            out = cv2.VideoWriter(file_path, codec, fps, resolution)

            frames_to_capture = int(duration * fps)
            captured_frames = 0
            start_time = time.time()

            while captured_frames < frames_to_capture:
                raw_img = sct.grab(monitor)
                frame = np.array(raw_img)
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                out.write(frame_bgr)
                captured_frames += 1

                expected_time = captured_frames / fps
                elapsed = time.time() - start_time
                sleep_duration = expected_time - elapsed
                if sleep_duration > 0:
                    time.sleep(sleep_duration)

        out.release()
        cv2.destroyAllWindows()

        return {
            "status": "success",
            "file_path": file_path,
            "duration": duration,
            "frames": captured_frames,
            "message": f"Screen recorded for {duration} seconds and saved to: {file_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to record screen: {str(e)}"
        }


def get_file_info(file_path: str) -> dict:
    """Get detailed information about a file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        dict: Contains status and file information
    """
    try:
        stat_info = os.stat(file_path)
        return {
            "status": "success",
            "file_path": file_path,
            "size_bytes": stat_info.st_size,
            "size_mb": round(stat_info.st_size / (1024 * 1024), 2),
            "modified_time": time.ctime(stat_info.st_mtime),
            "created_time": time.ctime(stat_info.st_ctime),
            "is_file": os.path.isfile(file_path),
            "is_directory": os.path.isdir(file_path),
            "message": f"File info retrieved for: {file_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get file info: {str(e)}"
        }


def batch_rename_files(directory: str, old_name: str, new_name_prefix: str) -> dict:
    """Batch rename all files in a directory with a new prefix.
    
    Args:
        directory (str): Directory containing files to rename
        old_name (str): Current name pattern (not used, kept for compatibility)
        new_name_prefix (str): New name prefix for files
        
    Returns:
        dict: Contains status and rename details
    """
    try:
        files = os.listdir(directory)
        renamed_count = 0
        
        for index, file in enumerate(files):
            full_path = os.path.join(directory, file)
            if os.path.isfile(full_path):
                file_ext = os.path.splitext(file)[1]
                new_name = f"{new_name_prefix}{index}{file_ext}"
                new_path = os.path.join(directory, new_name)
                os.rename(full_path, new_path)
                renamed_count += 1
            elif os.path.isdir(full_path):
                new_name = f"{new_name_prefix}{index}"
                new_path = os.path.join(directory, new_name)
                os.rename(full_path, new_path)
                renamed_count += 1
        
        return {
            "status": "success",
            "renamed_count": renamed_count,
            "message": f"Successfully renamed {renamed_count} items in {directory}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to batch rename files: {str(e)}"
        }


def download_file(file_path: str) -> dict:
    """Prepare a file for download by returning its path.
    This function validates that the file exists and is accessible.
    The actual file transfer will be handled by the Telegram bot.
    
    Args:
        file_path (str): Path to the file to download
        
    Returns:
        dict: Contains status, file path, and metadata for download
    """
    try:
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File not found: {file_path}"
            }
        
        if not os.path.isfile(file_path):
            return {
                "status": "error",
                "message": f"Path is not a file: {file_path}"
            }
        
        stat_info = os.stat(file_path)
        size_mb = round(stat_info.st_size / (1024 * 1024), 2)
        
        return {
            "status": "success",
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "size_mb": size_mb,
            "size_bytes": stat_info.st_size,
            "message": f"File ready for download: {file_path} ({size_mb} MB)"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to prepare file for download: {str(e)}"
        }


def download_directory(directory_path: str, output_zip: str = "") -> dict:
    """Create a zip archive of a directory for download.
    
    Args:
        directory_path (str): Path to the directory to download
        output_zip (str): Optional output zip file name. Default "" for auto-generated name (directory name + .zip)
        
    Returns:
        dict: Contains status and zip file path
    """
    try:
        if not os.path.exists(directory_path):
            return {
                "status": "error",
                "message": f"Directory not found: {directory_path}"
            }
        
        if not os.path.isdir(directory_path):
            return {
                "status": "error",
                "message": f"Path is not a directory: {directory_path}"
            }
        
        # Determine output zip name
        if output_zip is None or output_zip == "":
            dir_name = os.path.basename(directory_path.rstrip('/\\'))
            output_zip = f"{dir_name}.zip"
        
        # Create zip archive
        shutil.make_archive(
            output_zip.replace('.zip', ''),
            'zip',
            directory_path
        )
        
        zip_path = output_zip if output_zip.endswith('.zip') else f"{output_zip}.zip"
        stat_info = os.stat(zip_path)
        size_mb = round(stat_info.st_size / (1024 * 1024), 2)
        
        return {
            "status": "success",
            "file_path": zip_path,
            "directory": directory_path,
            "size_mb": size_mb,
            "message": f"Directory archived for download: {zip_path} ({size_mb} MB)"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to archive directory: {str(e)}"
        }


def list_files_in_directory(directory_path: str) -> dict:
    """List all files in a directory with detailed information.
    Useful before downloading to see what files exist.
    
    Args:
        directory_path (str): Path to the directory to list
        
    Returns:
        dict: Contains list of files with sizes
    """
    try:
        if not os.path.exists(directory_path):
            return {
                "status": "error",
                "message": f"Directory not found: {directory_path}"
            }
        
        if not os.path.isdir(directory_path):
            return {
                "status": "error",
                "message": f"Path is not a directory: {directory_path}"
            }
        
        items = []
        for item_name in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item_name)
            stat_info = os.stat(item_path)
            
            item_info = {
                "name": item_name,
                "type": "directory" if os.path.isdir(item_path) else "file",
                "size_bytes": stat_info.st_size if os.path.isfile(item_path) else 0,
                "size_mb": round(stat_info.st_size / (1024 * 1024), 2) if os.path.isfile(item_path) else 0,
                "modified": time.ctime(stat_info.st_mtime)
            }
            items.append(item_info)
        
        # Sort: directories first, then files
        items.sort(key=lambda x: (x["type"] != "directory", x["name"]))
        
        return {
            "status": "success",
            "directory": directory_path,
            "items": items,
            "total_items": len(items),
            "message": f"Found {len(items)} items in {directory_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list directory: {str(e)}"
        }


def open_application(application_name: str, file_path: str = "") -> dict:
    """Open an application installed on the PC. Can also open a file with a specific application.
    
    Args:
        application_name (str): Name or path of the application to open (e.g., 'notepad', 'chrome', 'code', or full path)
        file_path (str): Optional path to a file to open with the application. Leave empty if no file to open.
        
    Returns:
        dict: Contains status and application info
        
    Examples:
        - open_application('notepad') - Opens Notepad
        - open_application('chrome') - Opens Chrome browser
        - open_application('notepad', 'C:/file.txt') - Opens file.txt in Notepad
        - open_application('C:/Program Files/App/app.exe') - Opens app using full path
    """
    try:
        if file_path and file_path != "":
            # Open application with a specific file
            if os.path.exists(file_path):
                subprocess.Popen([application_name, file_path])
                return {
                    "status": "success",
                    "application": application_name,
                    "file_opened": file_path,
                    "message": f"Opened {file_path} with {application_name}"
                }
            else:
                return {
                    "status": "error",
                    "message": f"File not found: {file_path}"
                }
        else:
            # Just open the application
            subprocess.Popen(application_name, shell=True)
            return {
                "status": "success",
                "application": application_name,
                "message": f"Successfully opened {application_name}"
            }
    except FileNotFoundError:
        return {
            "status": "error",
            "message": f"Application not found: {application_name}. Make sure it's in your PATH or provide the full path."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to open application: {str(e)}"
        }


def type_text(text: str, interval: float = 0.1) -> dict:
    """Type text into the currently focused application window.
    
    Args:
        text (str): The text to type
        interval (float): Optional delay between each character in seconds. Default is 0.1 (standard speed).
        
    Returns:
        dict: Contains status and typed text info
    """
    try:
        pyautogui.write(text, interval=interval)
        return {
            "status": "success",
            "text_typed": text,
            "character_count": len(text),
            "message": f"Successfully typed {len(text)} characters"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to type text: {str(e)}"
        }


def press_key(key: str, presses: int = 1, interval: float = 0.1) -> dict:
    """Press a keyboard key or key combination in the active application.
    
    Args:
        key (str): Key to press (e.g., 'enter', 'tab', 'ctrl', 'alt', 'space', 'backspace', 'delete', 'f1'-'f12', etc.)
        presses (int): Optional number of times to press the key. Default is 1 for single press.
        interval (float): Optional delay between presses in seconds. Default is 0.1.
        
    Returns:
        dict: Contains status and key press info
        
    Examples:
        - press_key('enter') - Press Enter once
        - press_key('tab', 3) - Press Tab 3 times
        - press_key('f5') - Press F5 key
    """
    try:
        pyautogui.press(key, presses=presses, interval=interval)
        return {
            "status": "success",
            "key": key,
            "presses": presses,
            "message": f"Successfully pressed '{key}' {presses} time(s)"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to press key: {str(e)}"
        }


def press_hotkey(*keys: str) -> dict:
    """Press a keyboard shortcut/hotkey combination (e.g., Ctrl+C, Alt+Tab).
    
    Args:
        *keys: Keys to press together (e.g., 'ctrl', 'c' for Ctrl+C)
        
    Returns:
        dict: Contains status and hotkey info
        
    Examples:
        - press_hotkey('ctrl', 'c') - Copy
        - press_hotkey('ctrl', 'v') - Paste
        - press_hotkey('ctrl', 's') - Save
        - press_hotkey('alt', 'tab') - Switch window
        - press_hotkey('ctrl', 'shift', 'esc') - Task Manager
    """
    try:
        pyautogui.hotkey(*keys)
        hotkey_combo = '+'.join(keys)
        return {
            "status": "success",
            "hotkey": hotkey_combo,
            "keys": list(keys),
            "message": f"Successfully pressed hotkey: {hotkey_combo}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to press hotkey: {str(e)}"
        }


def click_mouse(x: int = -1, y: int = -1, button: str = 'left', clicks: int = 1) -> dict:
    """Click the mouse at a specific position or current position.
    
    Args:
        x (int): Optional X coordinate to click. Default -1 to click at current position
        y (int): Optional Y coordinate to click. Default -1 to click at current position
        button (str): Optional mouse button to click - 'left', 'right', or 'middle'. Default is 'left'
        clicks (int): Optional number of clicks. Default 1 for single, use 2 for double-click
        
    Returns:
        dict: Contains status and click info
    """
    try:
        if x >= 0 and y >= 0:
            pyautogui.click(x=x, y=y, button=button, clicks=clicks)
            position = f"({x}, {y})"
        else:
            pyautogui.click(button=button, clicks=clicks)
            current_pos = pyautogui.position()
            position = f"({current_pos.x}, {current_pos.y})"
        
        return {
            "status": "success",
            "button": button,
            "clicks": clicks,
            "position": position,
            "message": f"Successfully clicked {button} button {clicks} time(s) at {position}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to click mouse: {str(e)}"
        }


def move_mouse(x: int, y: int, duration: float = 0.5) -> dict:
    """Move the mouse cursor to a specific position.
    
    Args:
        x (int): X coordinate to move to
        y (int): Y coordinate to move to
        duration (float): Optional time in seconds for the movement. Default is 0.5.
        
    Returns:
        dict: Contains status and movement info
    """
    try:
        pyautogui.moveTo(x, y, duration=duration)
        return {
            "status": "success",
            "position": f"({x}, {y})",
            "duration": duration,
            "message": f"Successfully moved mouse to ({x}, {y})"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to move mouse: {str(e)}"
        }


def get_mouse_position() -> dict:
    """Get the current position of the mouse cursor.
    
    Returns:
        dict: Contains status and current mouse position
    """
    try:
        position = pyautogui.position()
        return {
            "status": "success",
            "x": position.x,
            "y": position.y,
            "position": f"({position.x}, {position.y})",
            "message": f"Current mouse position: ({position.x}, {position.y})"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get mouse position: {str(e)}"
        }


def get_screen_size() -> dict:
    """Get the screen resolution/size.
    
    Returns:
        dict: Contains status and screen dimensions
    """
    try:
        size = pyautogui.size()
        return {
            "status": "success",
            "width": size.width,
            "height": size.height,
            "resolution": f"{size.width}x{size.height}",
            "message": f"Screen size: {size.width}x{size.height}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get screen size: {str(e)}"
        }


def scroll_mouse(clicks: int, direction: str = 'down') -> dict:
    """Scroll the mouse wheel in the active window.
    
    Args:
        clicks (int): Number of scroll clicks (positive number)
        direction (str): Optional scroll direction - 'up' or 'down'. Default is 'down'
        
    Returns:
        dict: Contains status and scroll info
    """
    try:
        scroll_amount = clicks if direction == 'up' else -clicks
        pyautogui.scroll(scroll_amount)
        return {
            "status": "success",
            "clicks": clicks,
            "direction": direction,
            "message": f"Successfully scrolled {direction} {clicks} clicks"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to scroll: {str(e)}"
        }


def close_application(process_name: str) -> dict:
    """Close an application by its process name (Windows only).
    
    Args:
        process_name (str): Name of the process to close (e.g., 'notepad.exe', 'chrome.exe')
        
    Returns:
        dict: Contains status and closure info
    """
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(['taskkill', '/F', '/IM', process_name], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return {
                    "status": "success",
                    "process": process_name,
                    "message": f"Successfully closed {process_name}"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to close {process_name}: {result.stderr}"
                }
        else:
            # Linux/Mac
            result = subprocess.run(['pkill', '-f', process_name], 
                                  capture_output=True, text=True)
            return {
                "status": "success",
                "process": process_name,
                "message": f"Attempted to close {process_name}"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to close application: {str(e)}"
        }


def list_running_processes() -> dict:
    """List all currently running processes on the system (Windows only).
    
    Returns:
        dict: Contains status and list of running processes
    """
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(['tasklist'], capture_output=True, text=True)
            if result.returncode == 0:
                processes = []
                lines = result.stdout.split('\n')[3:]  # Skip header lines
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            processes.append({
                                "name": parts[0],
                                "pid": parts[1]
                            })
                
                return {
                    "status": "success",
                    "processes": processes[:50],  # Limit to first 50 to avoid huge output
                    "total_count": len(processes),
                    "message": f"Found {len(processes)} running processes (showing first 50)"
                }
            else:
                return {
                    "status": "error",
                    "message": "Failed to retrieve process list"
                }
        else:
            # Linux/Mac
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            processes = []
            for line in result.stdout.split('\n')[1:]:  # Skip header
                if line.strip():
                    parts = line.split(None, 10)
                    if len(parts) >= 11:
                        processes.append({
                            "name": parts[10],
                            "pid": parts[1]
                        })
            
            return {
                "status": "success",
                "processes": processes[:50],
                "total_count": len(processes),
                "message": f"Found {len(processes)} running processes (showing first 50)"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list processes: {str(e)}"
        }


def capture_screen_for_vision(save_path: str = "vision_capture.png") -> dict:
    """Capture the current screen and save it for vision analysis. This allows the AI to see what's on the screen and understand application states.
    
    Args:
        save_path (str): Optional path where the screenshot should be saved for analysis. Default is "vision_capture.png".
        
    Returns:
        dict: Contains status, file path, and screen information for AI vision analysis
    """
    try:
        path = save_path if save_path and save_path != "" else "vision_capture.png"

        if mss is not None:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                raw_img = sct.grab(monitor)
                frame = np.array(raw_img)
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                cv2.imwrite(path, frame_bgr)
                
                return {
                    "status": "success",
                    "file_path": path,
                    "screen_width": monitor["width"],
                    "screen_height": monitor["height"],
                    "is_vision_capture": True,
                    "message": f"✅ Vision capture successful! Screen captured at {path}. This image will be sent to the AI for analysis. The AI can now see what's on your screen (Resolution: {monitor['width']}x{monitor['height']}). You can now ask questions about what's visible or request actions based on the screen content."
                }
        else:
            return {
                "status": "error",
                "message": "Screen capture for vision requires the 'mss' package"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to capture screen for vision: {str(e)}"
        }


def analyze_screen_image(image_path: str, user_question: str) -> dict:
    """Analyze a screenshot image using Gemini Vision API and return detailed analysis.
    
    Args:
        image_path (str): Path to the image file to analyze (e.g., "vision_capture.png")
        user_question (str): Specific question to ask about the image (e.g., "What applications are open?" or "Describe what you see")
        
    Returns:
        dict: Contains status and AI analysis of the image
    """
    try:
        if not GOOGLE_API_KEY:
            return {
                "status": "error",
                "message": "GOOGLE_API_KEY not configured. Cannot perform vision analysis."
            }
        
        if not os.path.exists(image_path):
            return {
                "status": "error",
                "message": f"Image file not found: {image_path}"
            }
        
        # Use Gemini 2.0 Flash for vision analysis (fast and efficient)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Load the image
        import PIL.Image
        img = PIL.Image.open(image_path)
        
        # Create prompt for vision analysis
        prompt = f"""You are analyzing a screenshot of a computer screen. 
        
User's question: {user_question}

Please provide a detailed analysis of what you see in this screenshot. Include:
- What applications or windows are visible
- Any text content you can read
- UI elements (buttons, menus, etc.)
- Overall layout and state of the screen
- Answer to the user's specific question

Be specific and detailed in your response."""
        
        # Generate response with image
        response = model.generate_content([prompt, img])
        
        return {
            "status": "success",
            "analysis": response.text,
            "image_analyzed": image_path,
            "message": f"✅ Vision analysis complete for {image_path}"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to analyze image: {str(e)}"
        }


def find_element_on_screen(element_description: str) -> dict:
    """Use OCR and image recognition to find UI elements on the screen by description. This helps locate buttons, text fields, and other interface elements.
    
    Args:
        element_description (str): Description of the element to find (e.g., "Submit button", "Username text field", "File menu")
        
    Returns:
        dict: Contains status and information about found elements with coordinates
    """
    try:
        # Capture current screen
        if mss is None:
            return {
                "status": "error",
                "message": "Element detection requires the 'mss' package"
            }
        
        # For now, return a placeholder message explaining the capability
        # Full OCR implementation would require pytesseract or similar
        return {
            "status": "info",
            "message": f"Element detection for '{element_description}' is available. The AI can analyze screenshots to understand screen content and suggest click coordinates. First capture the screen using capture_screen_for_vision, then the AI can analyze it.",
            "suggestion": "Use capture_screen_for_vision first, then the AI vision model can analyze the image and provide coordinates for clicking on specific elements."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to find element: {str(e)}"
        }


def wait_seconds(seconds: int) -> dict:
    """Wait for a specified number of seconds. Useful for giving applications time to load or respond between automation steps.
    
    Args:
        seconds (int): Number of seconds to wait
        
    Returns:
        dict: Contains status and wait duration
    """
    try:
        time.sleep(seconds)
        return {
            "status": "success",
            "waited_seconds": seconds,
            "message": f"Waited {seconds} seconds"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to wait: {str(e)}"
        }

