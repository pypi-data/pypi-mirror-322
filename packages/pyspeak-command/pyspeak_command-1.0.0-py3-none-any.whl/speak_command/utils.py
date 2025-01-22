import os
import pyttsx3, keyboard, threading

keypress_event = threading.Event()
engine = pyttsx3.init()  
    
def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Erro ao falar: {e}")

def stop_speaking():
    engine.stop()

def detect_keypress():
    # Detecta pressionamento da tecla ESC para parar a fala
    while not keypress_event.is_set():
        if keyboard.is_pressed('esc'):
            print("Parando a fala...")
            stop_speaking()
            keypress_event.set()
            break

def keyPressed():
    keypress_event.clear()
    keypress_thread = threading.Thread(target=detect_keypress, daemon=True)
    keypress_thread.start()