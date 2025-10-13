import sys
import time
import pygame

lyrics_timing = [
    (0, "I Know I have a fickle heart and a bitterness"),       
    (5, "And a wandering eye, and heaviness in my head"),   
    (12, "but DON'T YOU REMEMBER?"),     
    (21, "DON'T YOU REMEMBER?"),
    (28, "THE REASON YOU LOVED ME?"),
    (36, "Baby, please remember"),            
    (41, "me once more"), 
]

def typing_effect(line, typing_speed=0.1):
    for char in line:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(typing_speed)
    sys.stdout.write("\n")
    sys.stdout.flush()

def display_lyrics_with_timing(lyrics_with_timing, audio_file):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    start_time = time.time() 

    for timestamp, line in lyrics_with_timing:
        while time.time() - start_time < timestamp:
            time.sleep(0.1) 

        typing_effect(line)

    while pygame.mixer.music.get_busy():
        time.sleep(1)

audio_file = "path_to_your_audio_file.mp3"

display_lyrics_with_timing(lyrics_timing, audio_file)
