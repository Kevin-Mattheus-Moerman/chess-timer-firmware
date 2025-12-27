"""
Music Options for the Soldered Pomodoro Timer Solder kit

This program allows playing musical sequences on a buzzer. Users can create their own
music on OnlineSequencer.net and paste the exported notes into the appropriate variables.

The system supports three jumper inputs (JP1, JP2, JP3). When a jumper is connected,
the corresponding musical sequences will be played. If no jumpers are connected,
the default sequences (intro, work, rest) will be used.

How to add your own music:
1. Visit onlinesequencer.net and create your musical sequence
2. Select all the notes and copy them
3. Paste the generated sequence into one of the variables below
4. delete the 'Online Sequencer' tag at the start of the string as well as the ';:' symbols at the end

Note format: 'start_time note duration volume;start_time note duration volume...'

──────────────────────────────────────────────
SEQUENCE SYNTAX EXPLANATION:

Each song is a single string consisting of multiple note entries separated by semicolons (;).

Each note entry follows this format:

    <start_time> <note> <duration> <instrument>

Where:
- start_time : when the note starts, in beats (integer or float)
- note        : note name + octave (e.g. C4, F#6, A#5)
- duration    : note length in beats
- instrument  : ignored by the buzzer but required for syntax (keep it any integer)

Example:
    "0 C4 2 0; 2 E4 2 0; 4 G4 4 0"

This plays C4 for 2 beats, E4 for 2 beats starting at beat 2, and G4 for 4 beats starting at beat 4.

"""
# 2025-12-27 Edited to have Star Wars inspired sounds by Kevin Moerman @kevin-mattheus-moerman

# Default musical sequences (played when no jumpers are connected)
# Create your own at OnlineSequencer.net and paste the exported Arduino code here
intro = '16 E4 1 41;24 A4 1 41;17 F#4 1 41;18 G4 1 41;20 A4 1 41;22 C4 1 41;26 G4 1 41;28 E4 1 41;27 F#4 1 41;0 G3 1 41;2 A3 1 41;4 G3 1 41;5 F#3 1 41;6 E3 1 41;8 G3 1 41;10 A3 1 41;12 G3 1 41;13 F#3 1 41;14 E3 1 41'#'0 E5 1 14;1 E5 1 14;3 E5 1 14;6 E5 1 14;5 C5 1 14;8 G5 1 14'#'2 A6 3 17;6 E6 1 17;9 G6 4 17;0 E6 1 17'  # Introductory music sequence
player_01 = '0 D4 4 50;4 G4 8 50;12 A4 6 50;18 A#4 1 50;19 C5 1 50;20 A#4 8 50;28 D4 6 50'#'2 B4 2 43;0 E5 1 43;4 B4 1 43;5 C5 1 43;6 C#5 1 43'  # Player 1 music
player_02 = '15 A#4 1 50;15 A#4 1 50;15 A#4 1 51;24 G4 2 51;16 G4 2 51;15 A#4 1 43;0 G4 3 43;4 G4 3 43;8 G4 3 43;12 D#4 2 43;16 G4 2 43;24 G4 4 43;15 A#3 1 43;20 D#4 2 43;23 A#4 1 43;23 A#3 1 43' # '9 G#6 1 17;0 D#6 1 17;3 F6 1 17;5 G#6 1 17;7 A#6 1 17'  # Player 2 music
switch_sound = '0 A6 1 43'#'3 A6 2 43;0 C7 2 43' 
start_sound = '0 C7 1 43;16 C7 1 43;8 C7 1 43;24 B7 3 43'

# Alternative musical sequences for jumper 1 (JP1)
intro_jp1 = '0 F#6 1 21;1 A6 1 21;3 C7 1 21;5 B6 1 21'
player_01_jp1 = '7 G#4 1 21;0 F4 1 21;2 F#4 1 21;4 G#4 1 21;6 A#4 1 21'
player_02_jp1 = '6 A7 2 43;0 A6 2 43;3 C#7 2 43'

# Alternative musical sequences for jumper 2 (JP2)
intro_jp2 = '8 G#6 2 43;0 G#6 2 43;3 B6 2 43;6 D#7 2 43;11 A#6 2 43'
player_01_jp2 = '0 C#7 1 41;3 E7 1 41;5 F#7 1 41;9 G#7 1 41'
player_02_jp2 = '0 C#7 2 41;4 G#7 2 41;2 E7 2 41'

# Alternative musical sequences for jumper 3 (JP3)
intro_jp3 = '4 A#6 3 25;0 F6 1 25;2 G6 1 25'
player_01_jp3 = '9 D6 3 25;0 B6 3 25;3 G6 3 25;6 C6 3 25'
player_02_jp3 = '10 F7 3 25;0 G6 3 25;4 A#6 3 25;7 D7 3 25'