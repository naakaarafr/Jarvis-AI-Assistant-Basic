import speech_recognition as sr
import os
import webbrowser
import google.generativeai as genai
from dotenv import load_dotenv
import datetime
import random
import numpy as np

# Load environment variables from .env file
load_dotenv()

chatStr = ""
selected_microphone_index = None

def list_microphones():
    """List all available microphones and return their details"""
    print("\nAvailable Microphones:")
    print("-" * 50)
    
    microphones = []
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{index}: {name}")
        microphones.append((index, name))
    
    return microphones

def select_microphone():
    """Select microphone with priority on Boult Audio"""
    global selected_microphone_index
    
    microphones = list_microphones()
    
    # Try to auto-select Boult Audio first
    boult_index = None
    intel_index = None
    
    for index, name in microphones:
        name_lower = name.lower()
        if "boult" in name_lower or "airbass" in name_lower:
            boult_index = index
            break
        elif "intel" in name_lower or "smart sound" in name_lower:
            intel_index = index
    
    # Priority selection
    if boult_index is not None:
        selected_microphone_index = boult_index
        print(f"\n✓ Auto-selected Boult Audio microphone (Index: {boult_index})")
        say("Boult Audio microphone selected")
        return True
    elif intel_index is not None:
        selected_microphone_index = intel_index
        print(f"\n✓ Auto-selected Intel microphone (Index: {intel_index})")
        say("Intel microphone selected")
        return True
    else:
        # Manual selection if neither is found
        print("\nBoult Audio or Intel microphone not found automatically.")
        print("Please select a microphone manually:")
        
        try:
            choice = int(input("\nEnter microphone index (or -1 to use default): "))
            if choice == -1:
                selected_microphone_index = None
                print("Using system default microphone")
                say("Using default microphone")
            elif 0 <= choice < len(microphones):
                selected_microphone_index = choice
                print(f"Selected: {microphones[choice][1]}")
                say(f"Selected microphone {choice}")
            else:
                print("Invalid selection. Using default microphone.")
                selected_microphone_index = None
                say("Using default microphone")
        except ValueError:
            print("Invalid input. Using default microphone.")
            selected_microphone_index = None
            say("Using default microphone")
        
        return True

def test_microphone():
    """Test the selected microphone"""
    print("\nTesting microphone... Say something!")
    say("Testing microphone. Please say something.")
    
    r = sr.Recognizer()
    
    try:
        if selected_microphone_index is not None:
            with sr.Microphone(device_index=selected_microphone_index) as source:
                print("Adjusting for ambient noise... Please wait.")
                r.adjust_for_ambient_noise(source, duration=2)
                print("Listening for test...")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
        else:
            with sr.Microphone() as source:
                print("Adjusting for ambient noise... Please wait.")
                r.adjust_for_ambient_noise(source, duration=2)
                print("Listening for test...")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
        
        test_result = r.recognize_google(audio, language="en-in")
        print(f"✓ Microphone test successful! You said: '{test_result}'")
        say("Microphone test successful")
        return True
        
    except sr.WaitTimeoutError:
        print("✗ No speech detected. Check your microphone.")
        say("No speech detected")
        return False
    except sr.UnknownValueError:
        print("✗ Could not understand the speech. Try speaking clearly.")
        say("Could not understand speech")
        return False
    except Exception as e:
        print(f"✗ Microphone test failed: {str(e)}")
        say("Microphone test failed")
        return False

def chat(query):
    global chatStr
    print(chatStr)
    
    # Configure Gemini with API key from environment
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    chatStr += f"Divvyansh: {query}\n Jarvis: "
    
    try:
        # Generate response using Gemini
        response = model.generate_content(
            chatStr,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=256,
                top_p=1.0,
            )
        )
        
        response_text = response.text
        print(f"🤖 Jarvis: {response_text}")
        say(response_text)  # This will make Jarvis speak the response
        chatStr += f"{response_text}\n"
        return response_text
        
    except Exception as e:
        error_msg = f"Error generating response: {str(e)}"
        say("Sorry, I encountered an error while processing your request.")
        print(error_msg)
        return error_msg

def ai(prompt):
    # Configure Gemini with API key from environment
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    
    text = f"Gemini response for Prompt: {prompt} \n *************************\n\n"
    
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=256,
                top_p=1.0,
            )
        )
        
        text += response.text
        print(f"🤖 AI Response: {response.text}")
        say(response.text)  # Make Jarvis speak the AI response too
        
        if not os.path.exists("Gemini"):
            os.mkdir("Gemini")
        
        # Create filename from prompt
        filename = ''.join(prompt.split('intelligence')[1:]).strip()
        if not filename:
            filename = f"prompt-{random.randint(1, 2343434356)}"
            
        with open(f"Gemini/{filename}.txt", "w") as f:
            f.write(text)
            
    except Exception as e:
        error_msg = f"Error in AI function: {str(e)}"
        print(error_msg)
        say("Sorry, I encountered an error while processing your AI request.")

def say(text):
    """Enhanced text-to-speech function"""
    try:
        # Clean the text for better speech
        clean_text = text.replace('"', '').replace("'", "").replace('\n', ' ').strip()
        if not clean_text:
            return
            
        print(f"🔊 Speaking: {clean_text}")
        
        # Cross-platform text-to-speech
        if os.name == 'nt':  # Windows
            import subprocess
            # Using PowerShell with better speech synthesis
            ps_command = f'''
            Add-Type -AssemblyName System.Speech
            $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
            $synth.Rate = 0
            $synth.Volume = 100
            $synth.Speak("{clean_text}")
            '''
            subprocess.run(['powershell', '-Command', ps_command], capture_output=True)
            
        elif os.name == 'posix':  # macOS/Linux
            if os.system('which say > /dev/null 2>&1') == 0:  # macOS
                os.system(f'say -r 200 "{clean_text}"')
            else:  # Linux - try multiple TTS options
                if os.system('which espeak > /dev/null 2>&1') == 0:
                    os.system(f'espeak -s 150 "{clean_text}"')
                elif os.system('which festival > /dev/null 2>&1') == 0:
                    os.system(f'echo "{clean_text}" | festival --tts')
                elif os.system('which spd-say > /dev/null 2>&1') == 0:
                    os.system(f'spd-say "{clean_text}"')
                else:
                    print("⚠️  No TTS engine found. Install espeak, festival, or speech-dispatcher")
                    
    except Exception as e:
        print(f"⚠️  Speech error: {str(e)}")
        print(f"Text was: {text}")

def takeCommand():
    global selected_microphone_index
    r = sr.Recognizer()
    
    try:
        if selected_microphone_index is not None:
            with sr.Microphone(device_index=selected_microphone_index) as source:
                print("Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                # Increased timeout and phrase_time_limit for better recognition
                audio = r.listen(source, timeout=10, phrase_time_limit=5)
        else:
            with sr.Microphone() as source:
                print("Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = r.listen(source, timeout=10, phrase_time_limit=5)
        
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query
        
    except sr.WaitTimeoutError:
        print("Listening timeout - no speech detected")
        return "timeout"
    except sr.UnknownValueError:
        print("Could not understand the audio")
        return "could not understand"
    except Exception as e:
        print(f"Error in speech recognition: {str(e)}")
        return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis A.I (Powered by Gemini)')
    print('=' * 50)
    
    # Initialize microphone selection
    say("Initializing Jarvis A.I powered by Gemini")
    
    if select_microphone():
        # Test the microphone
        if not test_microphone():
            print("\nWould you like to select a different microphone? (y/n)")
            if input().lower().startswith('y'):
                select_microphone()
                test_microphone()
    
    print('\n' + '=' * 50)
    print('Jarvis is ready! Start speaking...')
    say("Jarvis is ready")
    
    while True:
        query = takeCommand()
        
        # Skip processing for timeout or recognition errors
        if query in ["timeout", "could not understand", "Some Error Occurred. Sorry from Jarvis"]:
            continue
        
        # Website opening functionality
        sites = [
            ["youtube", "https://www.youtube.com"], 
            ["wikipedia", "https://www.wikipedia.com"], 
            ["google", "https://www.google.com"],
        ]
        
        site_opened = False
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                site_opened = True
                break
        
        if site_opened:
            continue
            
        # Music functionality
        if "open music" in query:
            # Update this path to your music file
            musicPath = "/Users/Divvyansh Kudesiaa/Downloads/downfall-21371.mp3"
            if os.path.exists(musicPath):
                say("Opening music for you sir")
                os.system(f"open '{musicPath}'")
            else:
                say("Music file not found")
                
        # Time functionality
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            time_response = f"Sir time is {hour} bajke {min} minutes"
            print(f"🕐 {time_response}")
            say(time_response)
            
        # Application opening
        elif "open facetime".lower() in query.lower():
            say("Opening FaceTime for you sir")
            os.system(f"open /System/Applications/FaceTime.app")
            
        elif "open pass".lower() in query.lower():
            say("Opening Passky for you sir")
            os.system(f"open /Applications/Passky.app")
            
        # Microphone management commands
        elif "change microphone" in query.lower() or "switch microphone" in query.lower():
            select_microphone()
            test_microphone()
            
        elif "test microphone" in query.lower():
            test_microphone()
            
        # AI prompt processing
        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
            
        # Quit command
        elif "Jarvis Quit".lower() in query.lower():
            say("Goodbye sir!")
            exit()
            
        # Reset chat
        elif "reset chat".lower() in query.lower():
            chatStr = ""
            say("Chat history has been reset")
            
        # Default chat
        else:
            print("Chatting...")
            chat(query)