import cv2
import os
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Controller as MouseController

MODEL_PATH = os.getcwd() + '\model\gesture_recognizer.task'

def scroll_down(mouse, number_of_lines):
    mouse.scroll(0, -number_of_lines)

def scroll_up(mouse, number_of_lines):
    mouse.scroll(0, number_of_lines)

def next_tab(keyboard):
    keyboard.press(Key.ctrl)
    keyboard.press(Key.tab)
    keyboard.release(Key.ctrl)
    keyboard.release(Key.tab)

def previous_tab(keyboard):
    keyboard.press(Key.ctrl)
    keyboard.press(Key.shift)
    keyboard.press(Key.tab)
    keyboard.release(Key.ctrl)
    keyboard.release(Key.shift)
    keyboard.release(Key.tab)

if __name__ == "__main__":
    mouse = MouseController()
    keyboard = KeyboardController()

    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.GestureRecognizerOptions(base_options=base_options)
    recognizer = vision.GestureRecognizer.create_from_options(options)
        
    cam = cv2.VideoCapture(0)
    while True:
        time.sleep(0.2)
        result, image = cam.read()

        if result:
            # save the image
            cv2.imwrite("teste.png", image)
            new_image = mp.Image.create_from_file("teste.png")
            # show the image
            recognition_result = recognizer.recognize(new_image)
            if recognition_result.gestures:
                gesture = recognition_result.gestures[0][0].category_name
                print(gesture)
                if gesture == 'Thumb_Up':
                    scroll_up(mouse, 2)
                elif gesture == 'Thumb_Down':
                    scroll_down(mouse, 2)
                elif gesture == 'Open_Palm':
                    next_tab(keyboard)
                elif gesture == 'Closed_Fist':
                    previous_tab(keyboard)
                elif gesture == 'Victory':
                    break

        # If captured image is corrupted, moving to else part 
        else: 
            print("No image detected. Please! try again") 

    print("babai")
