#!/bin/python

# combine and modified codes from:
# https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi
# https://github.com/quangthanh010290/voice_control_using_raspberry/blob/master/rpi_voice_control.py

import ctypes
import inspect
import os
import pyaudio
import speech_recognition as sr
import threading
import time
from Led import *
from Motor import *
from Ultrasonic import *

def test_Led():
    try:
        led.ledIndex(0x01,255,0,0)      #Red
        led.ledIndex(0x02,255,125,0)    #orange
        led.ledIndex(0x04,255,255,0)    #yellow
        led.ledIndex(0x08,0,255,0)      #green
        led.ledIndex(0x10,0,255,255)    #cyan-blue
        led.ledIndex(0x20,0,0,255)      #blue
        led.ledIndex(0x40,128,0,128)    #purple
        led.ledIndex(0x80,255,255,255)  #white'''
        time.sleep(1)
        led.colorWipe(led.strip, Color(0,0,0))  #turn off the light
    except KeyboardInterrupt:
        led.colorWipe(led.strip, Color(0,0,0))  #turn off the light

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def callback(self,audio):
    try:
        you = rec.recognize_sphinx(audio,keyword_entries=[("help", 1.0)])
    except:
        you = ""
    print(you)
    if "help" in you:
        print("help detected, stop ultrasonic for several seconds")
        for i in range(5):
            _async_raise(ultrasonic_thread.ident, SystemExit)
        ultrasonic.PWM.setMotorModel(0,0,0,0)
        ultrasonic.pwm_S.setServoPwm('0',90)
        test_Led()
        time.sleep(2)
        ultrasonic_thread=threading.Thread(target=ultrasonic.run)
        ultrasonic_thread.start()

for i, mic_name in enumerate (sr.Microphone.list_microphone_names()):
    print("mic: " + mic_name)
    # pulse seems better than usb mic
    if "pulse" in mic_name:
    #if "USB PnP Sound Device" in mic_name:
        mic = sr.Microphone(device_index=i, chunk_size=1024, sample_rate=48000)

try:
    ultrasonic_thread=threading.Thread(target=ultrasonic.run)
    ultrasonic_thread.start()
    rec = sr.Recognizer()
    rec.dynamic_energy_threshold = True
    rec.pause_threshold = 0.8
    rec.energy_threshold = 3000
    with mic as source:
        rec.adjust_for_ambient_noise(source, duration=1)
    rec.listen_in_background(mic, callback, phrase_time_limit=1)
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    for i in range(5):
        _async_raise(ultrasonic_thread.ident, SystemExit)
    ultrasonic.PWM.setMotorModel(0,0,0,0)
    ultrasonic.pwm_S.setServoPwm('0',90)
