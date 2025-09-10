#!/usr/bin/env python3
"""
Test script to verify voice recognition is working
"""

import speech_recognition as sr
import time

def test_voice_recognition():
    """Test basic voice recognition"""
    print("🎤 اختبار التعرف على الكلام...")
    
    # Initialize recognizer and microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    try:
        with microphone as source:
            print("🔧 تحديث مستوى الضوضاء...")
            recognizer.adjust_for_ambient_noise(source, duration=1.0)
            print("✅ تم تحديث مستوى الضوضاء")
            
            print("🎤 استمع للصوت...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("✅ تم تسجيل الصوت")
        
        print("🔄 معالجة الصوت...")
        
        # Try recognition
        try:
            text = recognizer.recognize_google(audio, language='ar-SA')
            print(f"✅ تم التعرف على الكلام: {text}")
            return text
        except sr.UnknownValueError:
            print("❌ لم أتمكن من فهم الصوت")
            return None
        except sr.RequestError as e:
            print(f"❌ خطأ في خدمة التعرف: {e}")
            return None
        except Exception as e:
            print(f"❌ خطأ: {e}")
            return None
            
    except sr.WaitTimeoutError:
        print("⏰ انتهت مهلة الاستماع")
        return None
    except Exception as e:
        print(f"❌ خطأ في الاستماع: {e}")
        return None

if __name__ == "__main__":
    print("🧪 اختبار التعرف على الكلام")
    print("=" * 40)
    
    result = test_voice_recognition()
    
    if result:
        print(f"🎉 نجح الاختبار! النص: {result}")
    else:
        print("❌ فشل الاختبار")
