# 🎤 Arabic Voice Assistant

A complete Arabic voice assistant for office use with memory, task management, and natural language processing.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Microphone
- Internet connection (for OpenAI and ElevenLabs APIs)

### Installation

1. **Clone and setup:**
   ```bash
   git clone <your-repo>
   cd arabic_voice_assistant
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install system dependencies:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y mpg123 mplayer
   ```

5. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Configuration

Edit `.env` file with your API keys:

```env
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# ElevenLabs API Key
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# ElevenLabs Voice ID (optional)
DEFAULT_VOICE_ID=your_custom_voice_id_here

# Voice Model (optional)
VOICE_MODEL=eleven_multilingual_v2

# Office Configuration (optional)
OFFICE_NAME=Your Office Name
ASSISTANT_NAME=المساعد الذكي
```

### Running the Assistant

```bash
# Activate virtual environment
source venv/bin/activate

# Run the assistant
python arabic_voice_assistant.py
```

## 🎯 Features

### Core Features
- **Arabic Speech Recognition** - Natural Arabic voice input
- **Arabic Text-to-Speech** - High-quality Arabic voice output using ElevenLabs
- **Persistent Memory** - Remembers conversations and context across sessions
- **Office Task Management** - Add, view, and manage tasks
- **Note Taking** - Save and retrieve important notes
- **Preference Management** - Remember user preferences

### Voice Commands

#### Basic Commands
- **"مرحبا"** - Hello
- **"ما هو الوقت؟"** - What time is it?
- **"شكرا"** - Thank you
- **"توقف"** - Stop assistant

#### Task Management
- **"أضف مهمة [وصف]"** - Add task
- **"عرض المهام"** - Show all tasks
- **"حذف مهمة [رقم]"** - Delete task by number

#### Memory Commands
- **"عرض الذاكرة"** - Show conversation history
- **"أضف تفضيل [تفضيلك]"** - Save preference
- **"عرض التفضيلات"** - Show saved preferences
- **"أضف ملاحظة [ملاحظتك]"** - Save note
- **"عرض الملاحظات"** - Show saved notes

#### System Commands
- **"عرض الإعدادات"** - Show system settings

## 🛠️ Technical Details

### Architecture
- **Speech Recognition**: Google Speech Recognition API
- **Natural Language Processing**: OpenAI GPT-3.5-turbo
- **Text-to-Speech**: ElevenLabs API
- **Audio Playback**: mpg123/mplayer with fallbacks
- **Memory Storage**: Pickle-based persistent storage

### File Structure
```
arabic_voice_assistant/
├── arabic_voice_assistant.py    # Main application
├── configure_voice.py           # Voice configuration utility
├── test_setup.py               # Setup verification
├── requirements.txt            # Python dependencies
├── .env                       # Environment configuration
├── .env.example              # Environment template
├── assistant_memory.pkl      # Persistent memory storage
├── README.md                 # This file
├── archive/                  # Archived development files
└── venv/                    # Virtual environment
```

### Dependencies
- `openai>=1.0.0` - OpenAI API client
- `elevenlabs>=0.2.0` - ElevenLabs TTS API
- `speech_recognition>=3.10.0` - Speech recognition
- `pyaudio>=0.2.11` - Audio input/output
- `pyttsx3>=2.90` - Fallback TTS
- `pydub>=0.25.1` - Audio processing
- `python-dotenv>=1.0.0` - Environment management

## 🔧 Troubleshooting

### Common Issues

#### Speech Recognition Timeout
- **Problem**: "⏰ انتهت مهلة التعرف على الكلام"
- **Solution**: Check internet connection, try speaking louder/clearer

#### Audio Playback Issues
- **Problem**: No sound output
- **Solution**: Install mpg123: `sudo apt-get install mpg123`

#### Microphone Not Working
- **Problem**: "❌ خطأ في الاستماع"
- **Solution**: Check microphone permissions and audio device

#### ALSA Warnings
- **Problem**: ALSA lib warnings in console
- **Solution**: These are normal and don't affect functionality

### Debug Mode
Run with debug output:
```bash
python arabic_voice_assistant.py --debug
```

## 📚 Usage Examples

### Basic Conversation
```
User: "مرحبا"
Assistant: "مرحباً! كيف يمكنني مساعدتك اليوم؟"

User: "ما هو الوقت؟"
Assistant: "الوقت الحالي هو [current time]"
```

### Task Management
```
User: "أضف مهمة إرسال التقرير"
Assistant: "تم إضافة المهمة: إرسال التقرير"

User: "عرض المهام"
Assistant: "المهام الحالية:
1. إرسال التقرير
2. مراجعة العقد"
```

### Memory Usage
```
User: "أضف تفضيل أحب القهوة السوداء"
Assistant: "تم حفظ التفضيل: أحب القهوة السوداء"

User: "عرض التفضيلات"
Assistant: "التفضيلات المحفوظة:
- أحب القهوة السوداء"
```

## 🔒 Security

- API keys are stored in `.env` file (not committed to git)
- Memory data is stored locally in `assistant_memory.pkl`
- No sensitive data is sent to external services except OpenAI and ElevenLabs

## 📝 License

This project is for office use. Please ensure you have proper API keys and permissions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Ensure all dependencies are installed
4. Verify API keys are correct

---

**Made with ❤️ for Arabic office productivity**