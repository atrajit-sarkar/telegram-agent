# AI Vision Integration Guide

## Overview
The bot now has **full vision capabilities** - it can see your screen and intelligently interact with applications based on what it sees!

## How It Works

### 1. **Screen Capture for Vision** 📸
When you ask the bot to capture the screen for analysis:
```
"Capture screen for vision"
"Take a vision screenshot"
"Let the AI see my screen"
```

The bot will:
1. Take a screenshot of your entire screen
2. Save it as `vision_capture.png`
3. **Send the image to YOU** via Telegram
4. **Store the image for the AI** to analyze

### 2. **Automatic AI Vision Analysis** 🤖👁️
**IMPORTANT:** The captured image is automatically sent to the AI (Gemini with vision) on your **next message**.

Example workflow:
```
You: "Capture screen for vision"
Bot: ✅ Vision capture successful! [sends screenshot]

You: "What do you see on the screen?"
Bot: [AI analyzes the image and describes what's visible]
     "I can see a Windows desktop with Chrome browser open showing..."

You: "Click on the search button"
Bot: [AI identifies the search button location and clicks it]
```

### 3. **Vision-Guided Automation** 🎯

The AI can:
- **Identify UI elements** (buttons, text fields, menus, etc.)
- **Read text** from the screen
- **Suggest click coordinates** for specific elements
- **Navigate applications** intelligently
- **Verify results** by capturing again

## Practical Examples

### Example 1: Find and Click a Button
```
You: "Capture screen for vision"
Bot: ✅ Vision captured!

You: "Where is the submit button?"
Bot: "I can see a blue 'Submit' button in the lower right corner at approximately coordinates (850, 720)"

You: "Click on it"
Bot: ✅ Clicked at (850, 720)
```

### Example 2: Fill Out a Form
```
You: "Open Chrome and go to example.com"
Bot: ✅ Opened Chrome

You: "Wait 3 seconds then capture screen for vision"
Bot: ✅ Waited 3 seconds
     ✅ Vision captured!

You: "Fill in the username field with 'testuser'"
Bot: [Analyzes screen, finds username field]
     "I can see the username field. Clicking on it..."
     ✅ Clicked at (450, 320)
     ✅ Typed 'testuser'
```

### Example 3: Read and Understand Content
```
You: "Capture screen for vision"
Bot: ✅ Vision captured!

You: "What's written in the error message?"
Bot: "I can see a red error message that says: 'Connection timeout. Please try again later.'"

You: "What should I do?"
Bot: "Based on the error, I recommend: 1) Check your internet connection..."
```

## Key Features

### ✅ Automatic Image Forwarding
- Screenshot is captured → Sent to you → **Stored for AI**
- Next message automatically includes the image for AI analysis
- AI can "see" and understand the screen state

### ✅ Multi-Step Automation
```
You: "Open Notepad, wait 2 seconds, capture screen, then type 'Hello World'"
```
The AI will:
1. Open Notepad
2. Wait 2 seconds
3. Capture screen for vision
4. See that Notepad is open
5. Type "Hello World" in the right place

### ✅ Intelligent Coordinate Detection
The AI can:
- Analyze the screenshot
- Identify element positions
- Provide accurate click coordinates
- Suggest adjustments if needed

## Advanced Usage

### Vision-Guided Testing
```
You: "Open the app, capture screen, then verify the login button is visible"
Bot: [Opens app, captures screen]
     "Yes, I can confirm the login button is visible in the center of the screen at coordinates (640, 480)"
```

### Visual Debugging
```
You: "Capture screen every 5 seconds and tell me when the download completes"
Bot: [Captures screen repeatedly]
     "Download in progress: 45%"
     [5 seconds later]
     "Download in progress: 78%"
     [5 seconds later]
     "Download complete! I can see 'Download finished' message"
```

### Smart Navigation
```
You: "Navigate to Settings in this application"
Bot: [Captures screen]
     "I can see a gear icon in the top right corner. Clicking it..."
     ✅ Clicked Settings
     [Captures again]
     "Settings menu is now open. What would you like to configure?"
```

## Technical Details

### Image Flow
1. **Capture**: `capture_screen_for_vision()` creates PNG file
2. **Storage**: File path stored in `last_vision_captures[chat_id]`
3. **Transmission**: Image sent to you via Telegram
4. **AI Upload**: On next message, image sent to Gemini AI
5. **Analysis**: AI uses vision model to understand content
6. **Action**: AI can then interact based on what it sees

### Supported Image Format
- Format: PNG
- Source: Full screen capture
- Resolution: Native screen resolution
- Color: RGB/BGR (automatically converted)

### AI Vision Model
- Model: Gemini 2.0 Flash (with vision capabilities)
- Input: Text + Image (multimodal)
- Output: Text understanding + action suggestions

## Best Practices

### 1. **Capture Before Complex Tasks**
```
You: "Capture screen, then fill out the registration form"
```
This lets the AI see the form structure first.

### 2. **Use Wait Commands**
```
You: "Open app, wait 3 seconds, capture screen"
```
Give apps time to load before capturing.

### 3. **Request Verification**
```
You: "Click submit, wait 2 seconds, capture screen to verify"
```
Confirm actions succeeded by seeing the result.

### 4. **Iterative Refinement**
```
You: "Capture screen"
You: "Find the red button"
You: "Now click 20 pixels to the right of it"
```
Adjust based on AI's understanding.

## Limitations

- **Single Screen**: Captures primary monitor only
- **Timing**: Brief delay between capture and AI analysis
- **Accuracy**: AI suggestions are approximate, may need adjustment
- **OCR**: No dedicated OCR yet (relies on AI vision interpretation)
- **Performance**: Large images may take time to process

## Future Enhancements

Coming soon:
- Multi-monitor support
- Element highlighting
- Automatic coordinate refinement
- OCR integration for text extraction
- Video stream analysis
- Confidence scores for element detection

## Quick Reference

| Command | What It Does |
|---------|-------------|
| `capture_screen_for_vision` | Take screenshot + store for AI |
| `wait_seconds` | Pause between actions |
| `get_screen_size` | Get resolution for coordinate calculations |
| `click_mouse` | Click at coordinates (AI suggests these) |
| `type_text` | Type text in active window |
| `get_mouse_position` | Get current cursor position |

## Troubleshooting

**Q: AI doesn't seem to see the image**
A: Make sure you send a follow-up message after capturing. The image is attached to your NEXT message.

**Q: AI identifies wrong location**
A: Try capturing again or manually specify coordinates: `click_mouse 500 300 left 1`

**Q: Image quality is poor**
A: Check screen resolution with `get_screen_size` and ensure `mss` package is installed.

---

**Try it now!** Say: *"Capture screen for vision, then tell me what you see"*
