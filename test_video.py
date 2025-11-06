"""Test script for video generation using Google Veo 3.1."""
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ Error: google-genai package not found!")
    print("Install it with: pip install google-genai")
    exit(1)

def test_video_generation():
    """Test the video generation using Veo 3.1."""
    print("🎬 Testing Video Generation with Veo 3.1...")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables!")
        return False
    
    try:
        # Initialize client
        print("📡 Initializing Google GenAI client...")
        client = genai.Client(api_key=api_key)
        
        # Define the prompt
        prompt = """A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.
A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"""
        
        print("\n📝 Prompt:")
        print("-" * 60)
        print(prompt)
        print("-" * 60)
        
        # Start video generation
        print("\n🎥 Starting video generation...")
        print("⏳ This may take several minutes...")
        
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
        )
        
        print(f"✅ Operation started: {operation.name}")
        
        # Poll the operation status until the video is ready
        wait_count = 0
        while not operation.done:
            wait_count += 1
            elapsed = wait_count * 10
            print(f"⏳ Waiting for video generation to complete... ({elapsed}s elapsed)")
            time.sleep(10)
            operation = client.operations.get(operation)
        
        print(f"\n✅ Video generation completed after ~{wait_count * 10} seconds!")
        
        # Download the generated video
        print("\n💾 Downloading generated video...")
        generated_video = operation.response.generated_videos[0]
        
        output_file = "dialogue_example.mp4"
        client.files.download(file=generated_video.video)
        generated_video.video.save(output_file)
        
        print(f"✅ Generated video saved to: {output_file}")
        
        # Check if file exists and get size
        if os.path.exists(output_file):
            file_size_mb = round(os.path.getsize(output_file) / (1024 * 1024), 2)
            print(f"📦 File size: {file_size_mb} MB")
            print(f"📁 Full path: {os.path.abspath(output_file)}")
            print("\n🎉 SUCCESS! Video generation is working!")
            return True
        else:
            print("❌ Error: Video file was not created!")
            return False
            
    except Exception as e:
        print(f"\n❌ Error during video generation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting video generation test...\n")
    success = test_video_generation()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ TEST PASSED - Video generation is working!")
        print("=" * 60)
        exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ TEST FAILED - Video generation encountered errors")
        print("=" * 60)
        exit(1)
