# *Friday(Functional Realtime Intelligence and Data Analytics Yielder)*

Friday Code is a versatile Python-based virtual assistant that integrates voice interaction, web search, multimedia processing, and system utilities. This project demonstrates how to combine multiple libraries and custom modules to create an interactive and engaging experience.

---

 Overview

# This assistant leverages a diverse set of modules to handle tasks such as:
- Voice Recognition & Speech: Capturing and processing voice commands with `speech_recognition` and converting text responses into audible speech using `pyttsx3`.
- Time & Date Management: Using `datetime` and `pytz` for accurate time handling.
- Information Retrieval: Fetching information from Wikipedia via the `wikipedia` module.
- Web Integration: Opening web pages and handling browser actions with `webbrowser`.
- System & OS Utilities: Running OS-level commands through `os` and `subprocess`, detecting system details with `platform`.
- Randomization & Multimedia: Using `random` for varied responses, and `pygame` for audio playback.
- Computer Vision: Processing images and videos using OpenCV (`cv2`).
- Web Interface: Providing a simple, interactive interface built with Flask (including `Flask`, `render_template`, `request`, `jsonify`, `redirect`, and `url_for`).
- Numerical Operations: Utilizing `numpy` for advanced computations.
- Networking & Communication: Handling socket connections and network tasks with `socket`.
- Phone Number Analysis: Parsing and extracting details from phone numbers using `phonenumbers` (with submodules for geocoding, carrier info, and timezone detection).
- Custom Functionality:  
  - capitals: A custom module to provide information on capital cities.  
  - rhymes: A custom module that offers functions to generate or retrieve rhyming phrases.

---

 # Features

- Voice Interaction: Easily control the assistant using spoken commands.
- Information Fetching: Get quick facts and summaries from Wikipedia.
- Web Navigation: Seamlessly open and navigate to websites.
- Multimedia Processing: Handle image/video processing tasks with OpenCV.
- Interactive Web Interface: Use a simple Flask web interface for alternative interaction.
- System & Network Utilities: Perform system checks and network communications effortlessly.
- Custom Modules: Enhance functionality with bespoke modules for capitals and rhymes.

---

 # Installation

 # *Prerequisites*

- Python 3.x

 Dependencies

Install the required Python packages using pip:

```bash
pip install speechrecognition pyttsx3 wikipedia pygame flask opencv-python numpy phonenumbers pytz
```

> Note: Some libraries, like OpenCV and pyttsx3, might require additional system-specific dependencies. Please consult the respective library documentation if you encounter any issues during installation.

--
