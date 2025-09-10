#!/usr/bin/env python3
"""
Voice Configuration Script
Helps you configure your custom ElevenLabs voice ID
"""

import os
import sys
from pathlib import Path

def get_voice_id():
    """Get voice ID from user"""
    print("🎵 ElevenLabs Voice Configuration")
    print("=" * 40)
    print("To find your voice ID:")
    print("1. Go to https://elevenlabs.io/app/voice-library")
    print("2. Find your custom voice")
    print("3. Copy the voice ID from the URL or voice settings")
    print()
    
    voice_id = input("Enter your ElevenLabs voice ID: ").strip()
    
    if not voice_id:
        print("❌ Voice ID cannot be empty")
        return None
    
    return voice_id

def get_api_keys():
    """Get API keys from user"""
    print("\n🔑 API Keys Configuration")
    print("=" * 30)
    
    openai_key = input("Enter your OpenAI API key: ").strip()
    elevenlabs_key = input("Enter your ElevenLabs API key: ").strip()
    
    if not openai_key or not elevenlabs_key:
        print("❌ Both API keys are required")
        return None, None
    
    return openai_key, elevenlabs_key

def update_env_file(openai_key, elevenlabs_key, voice_id):
    """Update .env file with new values"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Read current content
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Update values
    content = content.replace("OPENAI_API_KEY=your_openai_api_key_here", f"OPENAI_API_KEY={openai_key}")
    content = content.replace("ELEVENLABS_API_KEY=your_elevenlabs_api_key_here", f"ELEVENLABS_API_KEY={elevenlabs_key}")
    content = content.replace("DEFAULT_VOICE_ID=arabic_voice_id", f"DEFAULT_VOICE_ID={voice_id}")
    
    # Write back
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("✅ .env file updated successfully")
    return True

def test_configuration():
    """Test the configuration"""
    print("\n🧪 Testing Configuration")
    print("=" * 25)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv("OPENAI_API_KEY")
        elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        voice_id = os.getenv("DEFAULT_VOICE_ID")
        
        if openai_key and openai_key != "your_openai_api_key_here":
            print("✅ OpenAI API key configured")
        else:
            print("❌ OpenAI API key not configured")
        
        if elevenlabs_key and elevenlabs_key != "your_elevenlabs_api_key_here":
            print("✅ ElevenLabs API key configured")
        else:
            print("❌ ElevenLabs API key not configured")
        
        if voice_id and voice_id != "arabic_voice_id":
            print(f"✅ Voice ID configured: {voice_id}")
        else:
            print("❌ Voice ID not configured")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Main configuration function"""
    print("🚀 Arabic Voice Assistant - Voice Configuration")
    print("=" * 55)
    
    # Check if .env exists
    if not Path(".env").exists():
        print("❌ .env file not found. Please run setup first.")
        return
    
    # Get configuration from user
    voice_id = get_voice_id()
    if not voice_id:
        return
    
    openai_key, elevenlabs_key = get_api_keys()
    if not openai_key or not elevenlabs_key:
        return
    
    # Update .env file
    if update_env_file(openai_key, elevenlabs_key, voice_id):
        print("\n🎉 Configuration completed!")
        
        # Test configuration
        if test_configuration():
            print("\n🚀 You can now run the voice assistant:")
            print("   python arabic_voice_assistant.py")
        else:
            print("\n⚠️  Configuration test failed. Please check your values.")
    else:
        print("\n❌ Configuration failed.")

if __name__ == "__main__":
    main()
