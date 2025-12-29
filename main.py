# FILE: main.py
# AUTHOR: Štefan Granatir, Josip Šimun Kuči @ Soldered (original)
# BRIEF:    Main Micropython firmware for Soldered Pomodoro Timer Solder Kit.
#           Handles user interaction (buttons), countdown logic, LED colors,
#           buzzer jingles, and 7-segment display updates.
# LAST UPDATED: 2025-09-16
#
# 2025-12-27 Edited to be a chess timer by Kevin Moerman @kevin-mattheus-moerman

import time
import machine
import _thread
import neopixel
import seven_segment
from buzzer_music import music
from music_options import *

# ──────────────────────────────────────────────
# Hardware Configuration

# Buttons are wired with pull-ups, so they read 1 when not pressed, 0 when pressed
btn_increase      = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
btn_decrease    = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
btn_start_stop = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
btn_reset   = machine.Pin(23, machine.Pin.IN, machine.Pin.PULL_UP)

# NeoPixel LED on GPIO 1 (only 1 LED is used here)
led = neopixel.NeoPixel(machine.Pin(1), 1)
brightness_level_base = 0.2  # scale LED brightness so it’s not blinding
brightness_level_high = 0.3
brightness_level_low = 0.1

# Buzzer on GPIO 0 for playing melodies
buzzer = machine.Pin(0, machine.Pin.OUT)

# 7-segment display driver instance
display = seven_segment.SevenSegmentDisplay()


# ──────────────────────────────────────────────
# Utility Functions

def jingle_selection():
    """Selects what jingle is played at the start, when player_01 mode begins
       and when player_02 mode begins. Jingles can be customized, see file music_options.py
       for more info
    """
    # Three jumpers select which jingle set to load
    jumper1 = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_DOWN)
    jumper2 = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_DOWN)
    jumper3 = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)
    
    # Globals store currently chosen jingles
    global intro_jingle, player_01_jingle, player_02_jingle, switch_jingle, start_jingle
    
    # Each jumper corresponds to a different set of intro/player_01/rest melodies
    if jumper1.value()==1:
        intro_jingle = music(intro_jp1, pins=[buzzer], looping=False)
        player_01_jingle = music(player_01_jp1, pins=[buzzer], looping=False)
        player_02_jingle = music(player_02_jp1, pins=[buzzer], looping=False)
    elif jumper2.value()==1:
        intro_jingle = music(intro_jp2, pins=[buzzer], looping=False)
        player_01_jingle = music(player_01_jp2, pins=[buzzer], looping=False)
        player_02_jingle = music(player_02_jp2, pins=[buzzer], looping=False)
    elif jumper3.value()==1:
        intro_jingle = music(intro_jp3, pins=[buzzer], looping=False)
        player_01_jingle = music(player_01_jp3, pins=[buzzer], looping=False)
        player_02_jingle = music(player_02_jp3, pins=[buzzer], looping=False)
    else:
        # Default jingles if no jumper is set
        intro_jingle = music(intro, pins=[buzzer], looping=False)
        player_01_jingle = music(player_01, pins=[buzzer], looping=False)
        player_02_jingle = music(player_02, pins=[buzzer], looping=False)
        
    switch_jingle = music(switch_sound, pins=[buzzer], looping=False) 
    start_jingle = music(start_sound, pins=[buzzer], looping=False) 


def play_jingle(jingle, parallel_flag):
    """Starts a new thread that plays the jingle
    """
    if parallel_flag == True:
        _thread.start_new_thread(_play_jingle_thread, (jingle,) )
    else:
        _play_jingle_thread(jingle)

def _play_jingle_thread(jingle):
    """Plays the jingle given to it through an argument
    """
    # Tick() advances music playback; returns False when finished
    result = True
    while result:
        result = jingle.tick()
        time.sleep(0.04)  # small delay for timing control
    jingle.restart()  # reset jingle so it can be played again later

def update_led(color_tuple, brightness_level):
    # Scale each color channel by brightness_level and send to NeoPixel
    led[0] = tuple(int(c * brightness_level) for c in color_tuple)
    led.write()

def display_time(seconds):
    # Convert amount in seconds into a MM:SS frame string
    m = seconds // 60
    s = seconds % 60
    frame = f"{m:02}{s:02}" # always 4 chars (MMSS)
    display.write(frame)

def countdown(seconds, paused_flag, led_color):
    """Counts down the seconds of a given mode and changes the 7-segment display
       to show it
    """
    led_low = False
    done_flag = False
    display.set_decimal_point(1, True) # Set middle decimal point on
    while not done_flag and seconds >= 0:
        # Change LED to last-minute color when only 60s left            
        if seconds <= 10:
            if led_low == True:
                update_led(led_color, brightness_level_low)
                led_low = False
                # time.sleep_ms(200)
            else:
                update_led(led_color, brightness_level_high)
                led_low = True
                # time.sleep_ms(200)

        # Update displayed time
        display_time(seconds)
        
        # Align loop so each iteration lasts ~1 second
        end_time = time.ticks_add(time.ticks_ms(), 1000)
        while time.ticks_diff(end_time, time.ticks_ms()) > 0:
            # Poll buttons etc during the wait
                    
            # Switch player toggle
            if not btn_decrease.value():
                time.sleep_ms(200)  # debounce delay
                play_jingle(switch_jingle, False)
                done_flag = True
                break

            # Pause toggle
            if not btn_start_stop.value():
                time.sleep_ms(300)  # debounce delay
                paused_flag[0] = not paused_flag[0]
                
            # Reset button restarts main()
            if not btn_reset.value():
                main()

            # Handle paused state (digits blink on/off)
            while paused_flag[0]:
                now = time.ticks_ms()
                blink_on = (now // 500) % 2 == 0  # toggle every 500ms

                if not btn_start_stop.value():
                    time.sleep_ms(300)
                    paused_flag[0] = False
                    break

                if blink_on:
                    display_time(seconds)
                else:
                    display.clear()

                time.sleep_ms(50)  # reduce busy-looping
        if done_flag == False:
            seconds -= 1  # move to next second
            
    display.clear() # Clear display
    if seconds<=0: # If done
        return seconds
    else:
        return seconds + 2
        

def set_times():
    # Default Chess timer: 
    # 10 minutes game for each
    time_edit_increment = 1
    player_01 = 10
    player_02 = 10
    idx = 0              # 0 = editing player_01, 1 = editing player_02
    debounce = 200       # debounce time in ms
    last = time.ticks_ms()

    while idx < 2:
        now = time.ticks_ms()
        frame = f"{player_01:02}{player_02:02}"  # Display both times side by side
        blink_on = (now // 500) % 2 == 0

        # Blink the currently edited field to show focus
        if (idx == 0 and not blink_on):
            display.write("  " + frame[2:])  # hide player_01 minutes
        elif (idx == 1 and not blink_on):
            display.write(frame[:2] + "  ")  # hide player_02 minutes
        else:
            display.write(frame)

        # Button handling with debounce
        if not btn_increase.value() and time.ticks_diff(now, last) > debounce:
            if idx == 0: 
                player_01 = min(player_01 + time_edit_increment, 100-time_edit_increment)  # step in 5 mins
            else: 
                player_02 = min(player_02 + time_edit_increment, 100-time_edit_increment)
            last = now

        if not btn_decrease.value() and time.ticks_diff(now, last) > debounce:
            if idx == 0: 
                player_01 = max(player_01 - time_edit_increment, 0)
            else: 
                player_02 = max(player_02 - time_edit_increment, 0)
            last = now

        if not btn_start_stop.value() and time.ticks_diff(now, last) > debounce:
            idx += 1  # move to next field
            last = now

        time.sleep_ms(40)  # small delay to avoid busy-looping

    return player_01 * 60, player_02 * 60  # return values in seconds

def stream_text(frame, time_delay, number_of_repeats):
    n = len(frame)
    # print("n = ", n)
    for _ in range(0, number_of_repeats):
        for i in range(0, n-3): # 0 - n-4            
            display.write(frame[i:i+4])
            time.sleep_ms(time_delay) 

# ──────────────────────────────────────────────
# Main Loop

def main():
    while True: 
        # Led colors
        update_led((35, 91, 121), brightness_level_base)  # Initial LED color = Soldered purple

        # Sounds
        jingle_selection()          # Choose jingles based on jumpers
        play_jingle(intro_jingle, True)  # Play intro tune

        frame = f"_-~-_-~ CHESS ~-_-~-"   # always 4 chars (MMSS)
        stream_text(frame, 200, 1)

        color_player_01 = (255,  255,   0) # Color for player 1
        color_player_02 = (  0,    0, 255)  # Color for player 2
        color_players = (color_player_01, color_player_02)
        
        # Timing
        player_01_secs, player_02_secs = set_times()  # let user adjust times
        paused_flag = [False]  # list used so value can be mutated inside functions

        # Play short countdown sound to indicate ready/set/go
        frame = f"GET READY"   # always 4 chars (MMSS)
        stream_text(frame, 200, 1)
        display.write(f"----")

        # Display first player time
        update_led(color_players[0], brightness_level_base) # LED color for player 1
        play_jingle(start_jingle, False)

        print("Starting game.")
        while True: 
            # Player 1
            update_led(color_players[0], brightness_level_base) # LED color for player 1
            player_01_secs = countdown(player_01_secs, paused_flag, color_players[0])

            if player_01_secs <= 0:
                update_led(color_players[1], brightness_level_base) # LED color for player 2
                play_jingle(player_02_jingle, False)
                frame = f"PLAYER 2 SITH"   
                stream_text(frame, 200, 1)
                time.sleep(1.0)
                break
            
            # Player 2 
            update_led(color_players[1], brightness_level_base) # LED color for player 2
            player_02_secs = countdown(player_02_secs, paused_flag, color_players[1])

            if player_02_secs <= 0:
                update_led(color_players[0], brightness_level_base) # LED color for player 1
                play_jingle(player_01_jingle, False)
                frame = f"PLAYER 1 JEDI"   
                stream_text(frame, 200, 1)
                time.sleep(1.0)
                break

            time.sleep_ms(50)  # small delay to avoid busy-looping 
    
        

if __name__ == "__main__":
    main()  # Run program only if file is executed directly
