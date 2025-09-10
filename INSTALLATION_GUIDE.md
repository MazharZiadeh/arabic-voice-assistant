# 📋 Installation Guide

Complete step-by-step installation guide for the Arabic Voice Assistant.

## 🖥️ System Requirements

### Operating System
- **Linux** (Ubuntu 20.04+ recommended)
- **macOS** (10.15+)
- **Windows** (10+ with WSL recommended)

### Hardware
- **Microphone** (built-in or external)
- **Speakers/Headphones** (for audio output)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space

### Software
- **Python 3.8+**
- **pip** (Python package manager)
- **git** (for cloning repository)

## 🔧 Installation Steps

### Step 1: Clone Repository
```bash
git clone <your-repository-url>
cd arabic_voice_assistant
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show venv path)
which python
```

### Step 3: Install Python Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 4: Install System Dependencies

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y mpg123 mplayer portaudio19-dev python3-pyaudio
```

#### CentOS/RHEL:
```bash
sudo yum install mpg123 mplayer portaudio-devel python3-pyaudio
```

#### macOS:
```bash
brew install mpg123 mplayer portaudio
```

#### Windows (WSL):
```bash
sudo apt-get update
sudo apt-get install -y mpg123 mplayer portaudio19-dev python3-pyaudio
```

### Step 5: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

### Step 6: Get API Keys

#### OpenAI API Key:
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up/Login
3. Go to API Keys section
4. Create new API key
5. Copy the key to `.env` file

#### ElevenLabs API Key:
1. Go to [ElevenLabs](https://elevenlabs.io/)
2. Sign up/Login
3. Go to Profile → API Keys
4. Create new API key
5. Copy the key to `.env` file

#### ElevenLabs Voice ID (Optional):
1. Go to ElevenLabs Voice Library
2. Choose a voice or create custom voice
3. Copy the Voice ID to `.env` file

### Step 7: Test Installation
```bash
# Test setup
python test_setup.py

# Test voice recognition
python test_voice.py
```

### Step 8: Run the Assistant
```bash
# Activate virtual environment
source venv/bin/activate

# Run the assistant
python arabic_voice_assistant.py
```

## 🔍 Verification

### Check Installation
Run the verification script:
```bash
python test_setup.py
```

Expected output:
```
✅ Python version: 3.x.x
✅ Virtual environment: Active
✅ Dependencies: All installed
✅ API Keys: Configured
✅ Audio system: Working
✅ Microphone: Detected
```

### Test Voice Recognition
```bash
python test_voice.py
```

Expected output:
```
🧪 اختبار التعرف على الكلام
========================================
🎤 اختبار التعرف على الكلام...
✅ تم تحديث مستوى الضوضاء
🎤 استمع للصوت...
✅ تم تسجيل الصوت
🔄 معالجة الصوت...
✅ تم التعرف على الكلام: [your speech]
🎉 نجح الاختبار!
```

## 🚨 Troubleshooting

### Common Installation Issues

#### 1. Python Version Error
```bash
# Check Python version
python3 --version

# If version < 3.8, install newer Python
sudo apt-get install python3.9
```

#### 2. Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Audio System Issues
```bash
# Check audio devices
arecord -l
aplay -l

# Test microphone
arecord -d 5 test.wav
aplay test.wav
```

#### 4. Permission Issues
```bash
# Add user to audio group
sudo usermod -a -G audio $USER

# Logout and login again
```

#### 5. API Key Issues
```bash
# Check .env file
cat .env

# Verify API keys are correct
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OpenAI:', bool(os.getenv('OPENAI_API_KEY'))); print('ElevenLabs:', bool(os.getenv('ELEVENLABS_API_KEY')))"
```

### Audio Troubleshooting

#### ALSA Warnings
These are normal and don't affect functionality:
```
ALSA lib pcm_dsnoop.c:567:(snd_pcm_dsnoop_open) unable to open slave
```

#### No Sound Output
```bash
# Install audio players
sudo apt-get install mpg123 mplayer

# Test audio
mpg123 test.mp3
```

#### Microphone Not Working
```bash
# Check microphone
arecord -l

# Test recording
arecord -d 5 test.wav
aplay test.wav
```

## 📱 Mobile/Remote Setup

### SSH Access
```bash
# Enable audio over SSH
ssh -X username@server

# Run assistant
python arabic_voice_assistant.py
```

### Docker Setup (Advanced)
```dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    mpg123 mplayer portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "arabic_voice_assistant.py"]
```

## 🔄 Updates

### Update Dependencies
```bash
# Activate virtual environment
source venv/bin/activate

# Update pip
pip install --upgrade pip

# Update requirements
pip install -r requirements.txt --upgrade
```

### Update Application
```bash
# Pull latest changes
git pull origin main

# Reinstall if needed
pip install -r requirements.txt
```

## 📞 Support

If you encounter issues:

1. **Check logs** for error messages
2. **Verify system requirements** are met
3. **Test individual components** (microphone, speakers, APIs)
4. **Check internet connection** for API calls
5. **Review troubleshooting section** above

For additional help, check the main README.md file.

---

**Installation complete! Your Arabic Voice Assistant is ready to use.** 🎉
