#!/usr/bin/env python3
"""
Arabic Voice Assistant - Final Production Version
A complete Arabic voice assistant for office use with memory and task management
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
import openai
from elevenlabs import Voice, VoiceSettings
from elevenlabs.client import ElevenLabs
import speech_recognition as sr
import tempfile
import threading
import queue
import time
from datetime import datetime
import pickle
import subprocess

# Load environment variables
load_dotenv()

class ArabicVoiceAssistant:
    def __init__(self):
        """Initialize the Arabic Voice Assistant"""
        # API Configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = os.getenv("DEFAULT_VOICE_ID")
        self.voice_model = os.getenv("VOICE_MODEL", "eleven_multilingual_v2")
        
        # Office Configuration
        self.office_name = os.getenv("OFFICE_NAME", "Your Office Name")
        self.assistant_name = os.getenv("ASSISTANT_NAME", "المساعد الذكي")
        self.default_language = "ar"  # Force Arabic only
        
        # Initialize APIs
        self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
        self.elevenlabs_client = ElevenLabs(api_key=self.elevenlabs_api_key)
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Memory system
        self.memory_file = "assistant_memory.pkl"
        self.conversation_history = []
        self.office_context = {
            "current_tasks": [],
            "meetings": [],
            "announcements": [],
            "team_members": [],
            "user_preferences": {},
            "important_notes": [],
            "conversation_summary": ""
        }
        
        # Load existing memory
        self.load_memory()
        
        print(f"🎤 {self.assistant_name} جاهز للعمل في {self.office_name}")
        print(f"🔊 Language: {self.default_language}")
        print(f"🎵 Voice Model: {self.voice_model}")
        print(f"🧠 Memory: {len(self.conversation_history)} conversations loaded")

    def load_memory(self):
        """Load conversation history and context from file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'rb') as f:
                    data = pickle.load(f)
                    self.conversation_history = data.get('conversations', [])
                    self.office_context = data.get('context', self.office_context)
                print(f"✅ تم تحميل الذاكرة: {len(self.conversation_history)} محادثة")
        except Exception as e:
            print(f"❌ خطأ في تحميل الذاكرة: {e}")

    def save_memory(self):
        """Save conversation history and context to file"""
        try:
            data = {
                'conversations': self.conversation_history,
                'context': self.office_context
            }
            with open(self.memory_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"❌ خطأ في حفظ الذاكرة: {e}")

    def add_to_memory(self, user_input: str, assistant_response: str):
        """Add conversation to memory"""
        conversation = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'assistant_response': assistant_response
        }
        self.conversation_history.append(conversation)
        
        # Keep only last 100 conversations
        if len(self.conversation_history) > 100:
            self.conversation_history = self.conversation_history[-100:]
        
        # Save to file
        self.save_memory()

    def get_recent_context(self, limit: int = 5) -> str:
        """Get recent conversation context"""
        if not self.conversation_history:
            return ""
        
        recent_conversations = self.conversation_history[-limit:]
        context = "المحادثات الأخيرة:\n"
        for conv in recent_conversations:
            context += f"- المستخدم: {conv['user_input']}\n"
            context += f"- المساعد: {conv['assistant_response']}\n"
        return context

    async def listen_for_voice(self) -> Optional[str]:
        """Voice listening with timeout handling"""
        try:
            print("🎤 استمع...")
            
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("✅ تم تحديث مستوى الضوضاء")
                
                # Listen for voice input
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=8)
                print("✅ تم تسجيل الصوت")
            
            print("🔄 معالجة الصوت...")
            
            # Try Google recognition with timeout
            try:
                print("🔍 محاولة التعرف على الكلام...")
                
                # Use a timeout for Google recognition
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        self.recognizer.recognize_google, 
                        audio, 
                        language='ar-SA'
                    )
                    try:
                        text = future.result(timeout=5)  # 5 second timeout
                        if text and text.strip():
                            print(f"✅ تم التعرف على الكلام: {text}")
                            return text
                        else:
                            print("❌ النص فارغ")
                            return None
                    except concurrent.futures.TimeoutError:
                        print("⏰ انتهت مهلة التعرف على الكلام")
                        return None
                        
            except sr.UnknownValueError:
                print("❌ لم أتمكن من فهم الصوت - يرجى التحدث باللغة العربية")
                return None
            except sr.RequestError as e:
                print(f"❌ خطأ في خدمة التعرف على الكلام: {e}")
                return None
            except Exception as e:
                print(f"❌ خطأ في التعرف على الكلام: {e}")
                return None
                
        except sr.WaitTimeoutError:
            print("⏰ انتهت مهلة الاستماع")
            return None
        except Exception as e:
            print(f"❌ خطأ في الاستماع: {e}")
            return None

    async def generate_response(self, user_input: str) -> str:
        """Generate AI response using OpenAI with memory"""
        try:
            print(f"🤖 توليد الاستجابة لـ: {user_input}")
            
            # Get recent conversation context
            recent_context = self.get_recent_context()
            
            system_prompt = f"""أنت {self.assistant_name}، مساعد ذكي باللغة العربية في {self.office_name}.

المهمة: مساعدة الموظفين في المهام المكتبية والرد على استفساراتهم.

السياق الحالي:
{recent_context}

التفضيلات المحفوظة: {self.office_context.get('user_preferences', {})}
الملاحظات المهمة: {self.office_context.get('important_notes', [])}

تعليمات مهمة:
- ارد دائماً باللغة العربية فقط
- كن مفيداً ومهذباً
- استخدم الذاكرة للرد بناءً على المحادثات السابقة
- ساعد في المهام المكتبية مثل إدارة المهام والاجتماعات
- تذكر المعلومات المهمة التي يخبرك بها المستخدم

المهام المتاحة:
- إدارة المهام: أضف، عرض، حذف المهام
- إدارة الاجتماعات: جدولة، عرض، تذكير
- الإعلانات: إنشاء، عرض، بث
- الذاكرة: حفظ التفضيلات والملاحظات

رد على: {user_input}"""

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            result = response.choices[0].message.content.strip()
            print(f"✅ تم توليد الاستجابة: {result[:50]}...")
            return result
            
        except Exception as e:
            print(f"❌ خطأ في توليد الاستجابة: {e}")
            return "عذراً، حدث خطأ في معالجة طلبك."

    async def speak_response(self, text: str) -> None:
        """Convert text to speech using ElevenLabs with simple playback"""
        try:
            print(f"🔊 التحدث: {text}")
            
            # Generate audio using ElevenLabs
            print("🎵 توليد الصوت...")
            audio_generator = self.elevenlabs_client.text_to_speech.convert(
                text=text,
                voice_id=self.voice_id,
                model_id=self.voice_model
            )
            
            # Convert generator to bytes
            audio_bytes = b"".join(audio_generator)
            print("✅ تم توليد الصوت")
            
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_file_path = tmp_file.name
            
            # Play audio using system command
            print("🔊 تشغيل الصوت...")
            try:
                result = subprocess.run([
                    'mpg123', '-q', tmp_file_path
                ], capture_output=True, timeout=30)
                
                if result.returncode != 0:
                    print("⚠️ mpg123 فشل، جرب mplayer...")
                    # Fallback to mplayer
                    subprocess.run(['mplayer', '-really-quiet', tmp_file_path], timeout=30)
                    
            except subprocess.TimeoutExpired:
                print("⏰ انتهت مهلة تشغيل الصوت")
            except Exception as e:
                print(f"❌ خطأ في تشغيل الصوت: {e}")
                # Fallback to system TTS
                self.fallback_tts(text)
            
            # Clean up
            os.unlink(tmp_file_path)
            print("✅ انتهى تشغيل الصوت")
            
        except Exception as e:
            print(f"❌ خطأ في تحويل النص إلى كلام: {e}")
            # Fallback to system TTS
            self.fallback_tts(text)

    def fallback_tts(self, text: str) -> None:
        """Fallback TTS using system"""
        try:
            print("🔊 استخدام النظام الاحتياطي...")
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.say(text)
            engine.runAndWait()
        except:
            print(f"🔊 (Fallback): {text}")

    async def process_office_command(self, user_input: str) -> str:
        """Process office-specific commands"""
        user_input_lower = user_input.lower()
        
        # Task management
        if "أضف مهمة" in user_input:
            task = user_input.replace("أضف مهمة", "").strip()
            if task:
                self.office_context["current_tasks"].append(task)
                self.save_memory()
                return f"تم إضافة المهمة: {task}"
            else:
                return "يرجى تحديد المهمة المراد إضافتها"
        
        elif "عرض المهام" in user_input:
            if self.office_context["current_tasks"]:
                tasks = "\n".join([f"{i+1}. {task}" for i, task in enumerate(self.office_context["current_tasks"])])
                return f"المهام الحالية:\n{tasks}"
            else:
                return "لا توجد مهام حالياً"
        
        elif "حذف مهمة" in user_input:
            try:
                task_num = int(user_input.split()[-1]) - 1
                if 0 <= task_num < len(self.office_context["current_tasks"]):
                    removed_task = self.office_context["current_tasks"].pop(task_num)
                    self.save_memory()
                    return f"تم حذف المهمة: {removed_task}"
                else:
                    return "رقم المهمة غير صحيح"
            except:
                return "يرجى تحديد رقم المهمة المراد حذفها"
        
        # Memory commands
        elif "عرض الذاكرة" in user_input:
            if self.conversation_history:
                recent = self.conversation_history[-5:]
                memory_text = "المحادثات الأخيرة:\n"
                for conv in recent:
                    memory_text += f"- {conv['user_input']} -> {conv['assistant_response']}\n"
                return memory_text
            else:
                return "لا توجد محادثات محفوظة"
        
        elif "أضف تفضيل" in user_input:
            preference = user_input.replace("أضف تفضيل", "").strip()
            if preference:
                self.office_context["user_preferences"][f"pref_{len(self.office_context['user_preferences'])}"] = preference
                self.save_memory()
                return f"تم حفظ التفضيل: {preference}"
            else:
                return "يرجى تحديد التفضيل المراد حفظه"
        
        elif "عرض التفضيلات" in user_input:
            if self.office_context["user_preferences"]:
                prefs = "\n".join([f"- {pref}" for pref in self.office_context["user_preferences"].values()])
                return f"التفضيلات المحفوظة:\n{prefs}"
            else:
                return "لا توجد تفضيلات محفوظة"
        
        elif "أضف ملاحظة" in user_input or "أضف نوتة" in user_input:
            note = user_input.replace("أضف ملاحظة", "").replace("أضف نوتة", "").strip()
            if note:
                self.office_context["important_notes"].append(note)
                self.save_memory()
                return f"تم حفظ الملاحظة: {note}"
            else:
                return "يرجى تحديد الملاحظة المراد حفظها"
        
        elif "عرض الملاحظات" in user_input:
            if self.office_context["important_notes"]:
                notes = "\n".join([f"- {note}" for note in self.office_context["important_notes"]])
                return f"الملاحظات المهمة:\n{notes}"
            else:
                return "لا توجد ملاحظات محفوظة"
        
        else:
            return "يمكنني مساعدتك في إدارة المهام والاجتماعات وحفظ التفضيلات"

    async def run_conversation_loop(self):
        """Main conversation loop with better error handling"""
        print(f"\n🎯 {self.assistant_name} جاهز للاستماع...")
        print("💡 أوامر التحكم:")
        print("   - 'توقف' أو 'خروج' - إنهاء المحادثة")
        print("   - 'عرض الإعدادات' - عرض إعدادات النظام")
        print("=" * 60)
        
        while True:
            try:
                # Listen for voice input
                user_input = await self.listen_for_voice()
                
                if not user_input:
                    print("🔄 لم يتم فهم الصوت، جرب مرة أخرى...")
                    continue
                
                print(f"✅ تم فهم الصوت: {user_input}")
                
                # Check for control commands
                if "عرض الإعدادات" in user_input.lower():
                    settings = """
الإعدادات الحالية:
- استخدام مكتبة speech_recognition البسيطة
- مهلة الاستماع: 3 ثوان
- حد الكلام: 8 ثوان
- مهلة التعرف: 5 ثوان
- اللغة: العربية فقط
"""
                    print(settings)
                    await self.speak_response("تم عرض الإعدادات")
                    continue
                
                # Check for exit commands - Arabic only
                if any(word in user_input.lower() for word in ["توقف", "خروج"]):
                    await self.speak_response("وداعاً! أتمنى لك يوماً سعيداً")
                    break
                
                # Process the command - Arabic only
                if any(word in user_input for word in ["مهمة", "اجتماع", "إعلان", "ذاكرة", "تذكر", "تفضيل", "ملاحظة", "نوتة"]):
                    response = await self.process_office_command(user_input)
                else:
                    response = await self.generate_response(user_input)
                
                # Speak the response
                await self.speak_response(response)
                
                # Add to memory
                self.add_to_memory(user_input, response)
                
                print("-" * 30)
                
            except KeyboardInterrupt:
                print("\n👋 تم إيقاف المساعد")
                break
            except Exception as e:
                print(f"❌ خطأ: {e}")
                continue

async def main():
    """Main function with simple error handling"""
    try:
        assistant = ArabicVoiceAssistant()
        await assistant.run_conversation_loop()
    except KeyboardInterrupt:
        print("👋 تم إيقاف البرنامج")
    except Exception as e:
        print(f"❌ خطأ في تشغيل المساعد: {e}")

if __name__ == "__main__":
    asyncio.run(main())