#!/bin/sh

# from https://github.com/quangthanh010290/voice_control_using_raspberry
sudo apt-get update
sudo apt-get install espeak 
sudo apt install libespeak1 -y
sudo apt-get install portaudio19-dev -y
sudo apt-get install python-dev -y
sudo apt-get install  libportaudio2 libportaudiocpp0 portaudio19-dev -y
sudo apt install python-gpiozero -y
sudo apt-get install flac -y
sudo pip install pyttsx3    # text to speech library
sudo pip install PyAudio
sudo pip install SpeechRecognition

# from https://stackoverflow.com/a/64932897/9008720
sudo adduser root pulse-access
sudo pulseaudio --system=true 0<&- >/dev/null 2>&1 &

sudo ./voice.py
