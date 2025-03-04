import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random
import platform
import pygame
from flask import Flask, render_template, request, jsonify, redirect, url_for
import cv2
import sys
import numpy as np
from capitals import capitals
from rhymes import say_rhyme
import subprocess
import socket
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import pytz

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['IMAGE_DB'] = 'image_db'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['IMAGE_DB'], exist_ok=True)

recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)

pygame.init()
pygame.mixer.init()

music_dir = r"music"

def handle_specific_questions(question):
    if "hello" in question:
        greet()
        return "Hello! How can I assist you today?"
    elif "how are you" in question:
        return "I'm doing well, thank you for asking."
    elif "tell me a joke" in question:
        return "Why don't scientists trust atoms? Because they make up everything!"
    elif "tell me a fact" in question:
        return "A group of flamingos is called a flamboyance."
    elif "thank you" in question:
        return "You are welcome!"
    elif "bye" in question:
        return "Goodbye!"
    elif "goodbye" in question:
        return "Goodbye!"
    elif "i am happy buddy" in question:
        return "Well sir, What's the reason for you happiness!"
    elif "do you know me" in question:
        return "Yes sir, You are Mr.Sivaji"
    else:
        return None

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen(mode='microphone'):
    if mode == 'microphone':
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print("You said:", query)
            return query.lower().strip()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return ""
    else:
        try:
            query = input("Please enter your command: ")
            return query.lower().strip()
        except Exception as e:
            print("An error occurred:", e)
            return ""

@app.route("/")
def index():
    return render_template("friday.html")


@app.route('/assistant', methods=['POST'])
def assistant():
    if request.method == 'POST':
        data = request.get_json()
        command = data['command'].lower()
        response = process_command(command)
        return jsonify({'response': response})
    return jsonify({'response': 'Error: Method not allowed.'})

def greet():
    current_time = datetime.datetime.now()
    hour = current_time.hour
    if 0 <= hour < 12:
        speak("Good morning, sir! What should I do now?")
    elif 12 <= hour < 18:
        speak("Good afternoon, sir! What should I do now?")
    else:
        speak("Good evening, sir! What should I do now?")

def open_app(app_name):
    app_name = app_name.lower().strip()
    print("Opening application:", app_name)
    system_platform = platform.system().lower()
    if system_platform == "windows":
        try:
            if app_name == "whatsapp":
                webbrowser.open("https://web.whatsapp.com/")
            elif app_name == "camera":
                os.system("start microsoft.windows.camera:")
            else:
                os.system(f"start {app_name}")
        except Exception as e:
            print(e)
            speak("Sorry, I couldn't open the application.")
    elif system_platform == "darwin":
        try:
            if app_name == "whatsapp":
                webbrowser.open("https://web.whatsapp.com/")
            elif app_name == "camera":
                os.system("open -a Photo Booth")
            else:
                os.system(f"open -a {app_name}")
        except Exception as e:
            print(e)
            speak("Sorry, I couldn't open the application.")
    elif system_platform == "linux":
        try:
            if app_name == "whatsapp":
                webbrowser.open("https://web.whatsapp.com/")
            elif app_name == "camera":
                os.system("cheese")
            else:
                os.system(f"{app_name.lower()}")
        except Exception as e:
            print(e)
            speak("Sorry, I couldn't open the application.")
    else:
        speak("Sorry, I cannot open applications on this platform.")

def open_wikipedia(query):
    search_url = "https://en.wikipedia.org/wiki/" + query.replace(" ", "_")
    webbrowser.open(search_url)

def search(query):
    webbrowser.open("https://www.google.com/search?q=" + query)

def play_music():
    global current_song
    current_song = os.path.join(music_dir, random.choice(os.listdir(music_dir)))
    pygame.mixer.music.load(current_song)
    pygame.mixer.music.play()

def play_next_song():
    global current_song
    current_song = os.path.join(music_dir, random.choice(os.listdir(music_dir)))
    pygame.mixer.music.load(current_song)
    pygame.mixer.music.play()

def pause_music():
    pygame.mixer.music.pause()

def resume_music():
    pygame.mixer.music.unpause()

def trace_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        
        # Get the location information
        location = geocoder.description_for_number(parsed_number, 'en')
        
        # Get the carrier information
        service_provider = carrier.name_for_number(parsed_number, 'en')
        
        # Get the timezone information
        time_zones = timezone.time_zones_for_number(parsed_number)
        
        # Get the number type
        number_type = phonenumbers.number_type(parsed_number)
        number_type_str = {
            phonenumbers.PhoneNumberType.MOBILE: "Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Toll-Free",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
            phonenumbers.PhoneNumberType.VOIP: "VoIP",
            phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
            phonenumbers.PhoneNumberType.PAGER: "Pager",
            phonenumbers.PhoneNumberType.UAN: "UAN",
            phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail",
            phonenumbers.PhoneNumberType.UNKNOWN: "Unknown"
        }.get(number_type, "Unknown")
        
        # Get the country code and country name
        country_code = parsed_number.country_code

        
        # Format the number in different formats
        formatted_number_international = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        formatted_number_international_no_space = formatted_number_international.replace(" ", "")
        formatted_number_national = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        formatted_number_e164 = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        formatted_number_rfc3966 = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.RFC3966)
        
        # Verification status
        verification_status = 'By the gathered information, this is a verified mobile number' if phonenumbers.is_valid_number(parsed_number) else 'On the basis of the information gathered, this is not a verified mobile number'
        
        # Simulated Spam Score (without external API)
        spam_score = "Low" if number_type_str == "Mobile" else "Unknown"
        
        # Simulated Call History (local check)
        call_history = "No known incidents"
        
        # Suggest best time to call based on timezone
        best_time_message = ""
        for tz in time_zones:
            # Convert timezone string to a pytz timezone object
            tz_info = pytz.timezone(tz)
            local_time = datetime.datetime.now(tz_info)
            if 22 <= local_time.hour or local_time.hour < 8:
                best_time_message = f"It's currently {local_time.strftime('%I:%M %p')} in this location; consider calling later."
            else:
                best_time_message = f"It's currently {local_time.strftime('%I:%M %p')} in this location; it's a good time to call."
        
        
        # Format the result
        result = f"""
        Trace Result of the given mobile number ({formatted_number_international_no_space}):
        
        Country code        : (+{country_code})
        
        Location       : {location}
        
        Carrier Service provider        : {service_provider}
        
        Timezones      : {', '.join(time_zones)} ({best_time_message})
        
        Number Type    : {number_type_str}
        
        Verification   : {verification_status}
        
        Spam Score     : {spam_score} (based on number type)

        Call History   : {call_history}
        
        
        Alternate Formats:
        - National: {formatted_number_national}
        - E.164: {formatted_number_e164}
        - RFC3966: {formatted_number_rfc3966}
        
        """
        
        return result.strip()
    
    except phonenumbers.phonenumberutil.NumberParseException:
        return "Invalid phone number format"
    except Exception as e:
        return f"An error occurred: {str(e)}"



def ping_website(website_name):
    if not website_name.startswith(('http://', 'https://')):
        website_name = 'http://' + website_name

    try:
        host = website_name.replace('http://', '').replace('https://', '').split('/')[0]
        ip_address = socket.gethostbyname(host)

        if os.name == 'nt':  # Windows
            ping_command = ['ping', '-n', '4', host]
        else:  # Unix-based systems
            ping_command = ['ping', '-c', '4', host]
        
        # Execute the ping command
        ping_output = subprocess.check_output(ping_command, universal_newlines=True)

        server_info = {
            "Website": website_name,
            "IP Address": ip_address,
            "Ping Output": ping_output
        }

        return server_info

    except subprocess.CalledProcessError as e:
        return f"Ping failed with error: {e.output}"
    
    except socket.gaierror as e:
        return f"DNS resolution failed: {str(e)}"
    
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def format_ping_output(output):
    # Format the ping output to make it more readable
    formatted_output = output.strip().replace('\n', '\n    ')
    return formatted_output

def process_command(command):
    if command.startswith('search for '):
        query = command.replace('search for ', '')
        search(query)  # Assuming you have a search function implemented
        return f'Searching for {query}.'

    elif command.startswith('who is '):
        person = command.replace('who is ', '')
        info = wikipedia.summary(person, sentences=2)
        return info

    elif command.startswith('open '):
        app_name = command.replace('open ', '')
        open_app(app_name)  # Assuming you have an open_app function implemented
        return f'Opening {app_name}.'

    elif command.startswith('play music'):
        play_music()  # Assuming you have a play_music function implemented
        return 'Playing music.'

    elif command == 'pause music':
        pause_music()  # Assuming you have a pause_music function implemented
        return 'Paused music.'

    elif command == 'resume music':
        resume_music()  # Assuming you have a resume_music function implemented
        return 'Resuming music.'

    elif command == 'next song':
        play_next_song()  # Assuming you have a play_next_song function implemented
        return 'Playing next song.'

    elif command == 'tell me a rhyme':
        rhyme = say_rhyme()  # Assuming you have a say_rhyme function implemented
        return rhyme

    elif command.startswith('what is the capital of '):
        country = command.replace('what is the capital of ', '').strip()
        if country.lower() in capitals:  # Assuming you have a capitals dictionary
            return f'The capital of {country.capitalize()} is {capitals[country.lower()]}.'
        else:
            return f'Sorry, I do not know the capital of {country}.'

    elif command.startswith('tell me about '):
        topic = command.replace('tell me about ', '')
        try:
            info = wikipedia.summary(topic, sentences=5)
            return info
        except wikipedia.exceptions.DisambiguationError:
            return f'There are multiple results for {topic}. Can you be more specific?'

    elif command == 'what can you do':
        return 'I can search the web, open applications, play music, tell jokes and rhymes, and provide information.'

    elif command == 'what time is it':
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        return f'It is currently {current_time}.'
    
    elif command == 'what date is it':
        current_date = datetime.datetime.now().strftime('%B %d, %Y')
        return f'Todays date is {current_date}.'

    elif command == 'who are you':
        return 'I am your virtual assistant, Friday, Functional Real-time Intelligence and Data Analytics Yielder.'

    elif command in ['hello', 'hi']:
        greet()  # Assuming you have a greet function implemented
        return 'Hello! How can I assist you today?'

    elif command in ['bye', 'goodbye']:
        return 'Goodbye! Have a great day!'

    elif command == "wake up daddy's home":
        return "Welcome home sir, What should I do now!"
    
    elif command.startswith('i want details about'):
        query = command.replace('i want details about', '').strip().strip('"')
        server_info = ping_website(query)
        
        if isinstance(server_info, dict):
            result = (
                f"--- Details for {server_info['Website']} ---\n"
                f"IP Address: {server_info['IP Address']}\n\n"
                f"--- Ping Output ---\n"
                f"{format_ping_output(server_info['Ping Output'])}"
            )
        else:
            result = server_info
        return f'Getting details about {query}:\n{result}'
    

    elif command.startswith('trace'):
        query = command.replace('trace', '').strip().strip('"')
        trace_result = trace_phone_number(query)
        print(trace_result)
        return trace_result


    
    
    
    else:
        specific_response = handle_specific_questions(command)
        if specific_response:
            return specific_response
        else:
            return "Sorry, I didn't understand that command."
    
    


if __name__ == '__main__':
    app.run(debug=True)