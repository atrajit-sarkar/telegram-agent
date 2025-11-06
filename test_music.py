"""Test script for music generation functionality."""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the music generation function
from system_tools import generate_music

def test_music_generation():
    """Test the generate_music function with a simple prompt."""
    print("🎵 Testing Music Generation...")
    print("=" * 60)
    
    # Test with a short duration for quick testing
    result = generate_music(
        prompts="lo-fi hip hop, chill",
        duration=10,  # Just 10 seconds for testing
        bpm=90,
        output_file="test_music.wav"
    )
    
    print("\n📋 Result:")
    print("-" * 60)
    for key, value in result.items():
        print(f"{key}: {value}")
    print("-" * 60)
    
    if result.get("status") == "success":
        print("\n✅ SUCCESS! Music generation is working!")
        print(f"📁 File created: {result.get('file_path')}")
        print(f"📊 File size: {result.get('size_mb')} MB")
        
        # Check if file actually exists
        file_path = result.get('file_path')
        if file_path and os.path.exists(file_path):
            print(f"✅ File verified: {file_path}")
            file_size = os.path.getsize(file_path)
            print(f"📦 Actual file size: {file_size:,} bytes")
        else:
            print("❌ File not found!")
    else:
        print("\n❌ FAILED! Music generation encountered an error.")
        print(f"Error message: {result.get('message')}")
    
    return result

if __name__ == "__main__":
    print("Starting music generation test...\n")
    try:
        result = test_music_generation()
        sys.exit(0 if result.get("status") == "success" else 1)
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
