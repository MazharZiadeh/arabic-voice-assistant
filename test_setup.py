#!/usr/bin/env python3
"""
Test script to verify the Arabic Voice Assistant setup
"""

import os
import sys
from dotenv import load_dotenv

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing package imports...")
    
    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        import elevenlabs
        print("✅ ElevenLabs imported successfully")
    except ImportError as e:
        print(f"❌ ElevenLabs import failed: {e}")
        return False
    
    try:
        import speech_recognition as sr
        print("✅ SpeechRecognition imported successfully")
    except ImportError as e:
        print(f"❌ SpeechRecognition import failed: {e}")
        return False
    
    try:
        import pyaudio
        print("✅ PyAudio imported successfully")
    except ImportError as e:
        print(f"❌ PyAudio import failed: {e}")
        return False
    
    try:
        import pygame
        print("✅ Pygame imported successfully")
    except ImportError as e:
        print(f"❌ Pygame import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment configuration"""
    print("\n🔧 Testing environment configuration...")
    
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    
    if openai_key and openai_key != "your_openai_api_key_here":
        print("✅ OpenAI API key configured")
    else:
        print("⚠️  OpenAI API key not configured (edit .env file)")
    
    if elevenlabs_key and elevenlabs_key != "your_elevenlabs_api_key_here":
        print("✅ ElevenLabs API key configured")
    else:
        print("⚠️  ElevenLabs API key not configured (edit .env file)")
    
    return True

def test_audio_system():
    """Test audio system"""
    print("\n🔊 Testing audio system...")
    
    try:
        import speech_recognition as sr
        import pyaudio
        
        # Test microphone
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        print("✅ Microphone detected")
        
        # Test audio output
        import pygame
        pygame.mixer.init()
        print("✅ Audio output system ready")
        
        return True
    except Exception as e:
        print(f"❌ Audio system test failed: {e}")
        return False

def test_arabic_voice_assistant():
    """Test the main voice assistant class"""
    print("\n🤖 Testing Arabic Voice Assistant class...")
    
    try:
        # Set dummy API keys for testing
        os.environ["OPENAI_API_KEY"] = "test_key"
        os.environ["ELEVENLABS_API_KEY"] = "test_key"
        
        from arabic_voice_assistant import ArabicVoiceAssistant
        
        # This will fail due to invalid API keys, but we can test the class structure
        try:
            assistant = ArabicVoiceAssistant()
            print("✅ ArabicVoiceAssistant class created successfully")
            return True
        except ValueError as e:
            if "API key" in str(e):
                print("✅ ArabicVoiceAssistant class structure is correct")
                print("⚠️  API keys need to be configured for full functionality")
                return True
            else:
                print(f"❌ ArabicVoiceAssistant creation failed: {e}")
                return False
    except Exception as e:
        print(f"❌ ArabicVoiceAssistant test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Arabic Voice Assistant Setup")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_environment,
        test_audio_system,
        test_arabic_voice_assistant
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n📋 Next steps:")
        print("1. Edit .env file and add your real API keys")
        print("2. Run: python arabic_voice_assistant.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
