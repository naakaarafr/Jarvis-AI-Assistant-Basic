# 🤖 Jarvis AI Assistant

A sophisticated voice-controlled AI assistant powered by Google's Gemini AI, featuring speech recognition, text-to-speech, and intelligent conversation capabilities.

## ✨ Features

### 🎙️ Voice Recognition
- **Smart Microphone Detection**: Automatically detects and prioritizes Boult Audio and Intel microphones
- **Manual Microphone Selection**: Choose from all available system microphones
- **Microphone Testing**: Built-in functionality to test microphone quality
- **Ambient Noise Adjustment**: Automatically adjusts for background noise

### 🧠 AI-Powered Conversations
- **Gemini Integration**: Powered by Google's Gemini 2.0 Flash model
- **Contextual Chat**: Maintains conversation history for natural dialogue
- **AI Prompt Processing**: Handle complex AI queries with dedicated processing
- **Smart Response Generation**: Temperature-controlled responses for natural conversation

### 🔊 Text-to-Speech
- **Cross-Platform TTS**: Works on Windows, macOS, and Linux
- **Multiple TTS Engines**: Supports various speech synthesis options
- **Voice Feedback**: Jarvis speaks all responses and confirmations

### 🌐 Web Integration
- **Quick Website Access**: Voice commands to open popular websites
  - YouTube
  - Wikipedia  
  - Google
- **Browser Integration**: Seamless web browsing through voice commands

### 📱 Application Control
- **FaceTime Integration**: Launch FaceTime with voice commands
- **Passky Integration**: Access password manager via voice
- **Music Player**: Play local music files
- **Time Announcements**: Get current time in natural language

### 🎛️ System Management
- **Chat Reset**: Clear conversation history on command
- **Microphone Switching**: Change microphones during runtime
- **Graceful Exit**: Proper shutdown with voice confirmation

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- Internet connection for Gemini AI
- Microphone (preferably Boult Audio or Intel)
- Google Gemini API key

### Required Packages
```bash
pip install speech-recognition
pip install google-generativeai
pip install python-dotenv
pip install numpy
```

### System Dependencies

#### Windows
- Built-in Windows Speech API (automatically available)

#### macOS
- Built-in `say` command (automatically available)

#### Linux
Install one of the following TTS engines:
```bash
# Option 1: eSpeak
sudo apt-get install espeak

# Option 2: Festival
sudo apt-get install festival

# Option 3: Speech Dispatcher
sudo apt-get install speech-dispatcher
```

## ⚙️ Setup

### 1. Environment Configuration
Create a `.env` file in the project directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Get Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### 3. Configure Music Path (Optional)
Update the `musicPath` variable in the code to point to your music file:
```python
musicPath = "/path/to/your/music/file.mp3"
```

## 🚀 Usage

### Starting Jarvis
```bash
python main.py
```

### Voice Commands

#### Website Navigation
- "Open YouTube"
- "Open Wikipedia"
- "Open Google"

#### System Control
- "What's the time?" / "Tell me the time"
- "Open FaceTime"
- "Open Pass" (for Passky)
- "Open music"

#### Microphone Management
- "Change microphone"
- "Test microphone"

#### AI Features
- "Using artificial intelligence [your prompt]" - For dedicated AI processing
- Any other query - For conversational chat

#### System Commands
- "Reset chat" - Clear conversation history
- "Jarvis Quit" - Exit the application

### Example Conversations
```
You: "Hello Jarvis, how are you today?"
Jarvis: "Hello! I'm doing well and ready to assist you. How can I help you today?"

You: "What's the weather like?"
Jarvis: [Provides weather information based on AI knowledge]

You: "Open YouTube"
Jarvis: "Opening YouTube sir..."
```

## 🔧 Configuration Options

### Microphone Priority
The system automatically prioritizes microphones in this order:
1. Boult Audio devices
2. Intel Smart Sound devices
3. Manual selection
4. System default

### AI Model Settings
- **Model**: Gemini 2.0 Flash for chat, Gemini Pro for AI prompts
- **Temperature**: 0.7 (balanced creativity/accuracy)
- **Max Tokens**: 256 (concise responses)
- **Top P**: 1.0 (full vocabulary access)

## 📁 Project Structure
```
jarvis-ai/
├── main.py              # Main application file
├── .env                 # Environment variables (create this)
└── README.md           # This file
```

## 🐛 Troubleshooting

### Common Issues

#### "No TTS engine found" (Linux)
Install a text-to-speech engine:
```bash
sudo apt-get install espeak
```

#### "Microphone not working"
1. Check microphone permissions
2. Try running microphone test
3. Select a different microphone manually

#### "API Error"
1. Verify your Gemini API key is correct
2. Check internet connection
3. Ensure API key has proper permissions

#### "Speech Recognition Failed"
1. Check microphone volume
2. Speak clearly and closer to microphone
3. Reduce background noise
4. Try adjusting ambient noise settings

### Debug Mode
For troubleshooting, monitor the console output which provides detailed information about:
- Microphone selection process
- Speech recognition results
- AI response generation
- TTS status

## 🤝 Contributing

Feel free to contribute to this project! Areas for improvement:
- Additional voice commands
- Better error handling
- More AI model options
- Enhanced TTS voices
- Mobile app integration

## 📜 License

This project is open source. Please ensure you comply with Google's Gemini AI terms of service when using the API.

## 🙏 Acknowledgments

- **Google Gemini AI** for the powerful language model
- **SpeechRecognition** library for voice input
- **Python-dotenv** for environment management
- **Boult Audio** for quality microphone hardware

---

**Created by:** naakaarafr  
**Powered by:** Google Gemini AI  
**Version:** 1.0

*Jarvis is ready to assist you! 🚀*
