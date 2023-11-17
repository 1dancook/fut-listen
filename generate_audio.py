"""
A script to generate audio

This is meant to work on macos
It requires the built in `say` command and sox

sox can be installed with brew install sox
"""

import subprocess
from pathlib import Path

# asset folder, and make sure it exists
ASSET_FOLDER = Path("./src/fut_listen/assets")
ASSET_FOLDER.mkdir(parents=True, exist_ok=True)

# Erase everything in the asset folder before starting
for file in ASSET_FOLDER.glob("*.*"):
    print(f"Deleting {file.name}")
    file.unlink()

def sanitize_phrase(phrase: str) -> str:
    phrase = phrase.lower()
    for c in "!@#$%^&*(){}[];:'\",<.>/?\\":
        phrase = phrase.replace(c, "")
    phrase = phrase.replace(" ", "_")
    return phrase

def save_tone(length, hz, vol, out_file):
    """ Play a tone with sox and sleep for one second """
    out_file = ASSET_FOLDER / Path(f"{out_file}.mp3")
    print("making", out_file)

    # first make the tone file
    args = ["sox", "-n", "-r", "44100", "-c", "1", str(out_file), "synth", str(length), "sine", str(hz), "vol", f"{vol}db",]
    subprocess.run(args)

    # determine if we need some padding
    remaining = 1.0 - length
    if remaining > 0: # pad it with silence
        args = ["sox", str(out_file), str(out_file), "pad", "0", str(remaining)]
        subprocess.run(args)


def say(phrase, filename=None):
    if not filename:
        out_file = sanitize_phrase(phrase) + ".m4a"
        out_file = ASSET_FOLDER / Path(out_file)
    else:
        out_file = ASSET_FOLDER / Path(filename + ".m4a")
    print("making", out_file)
    args = ["say", "-r", "145", "-o", out_file, "--progress", "--channels=1", str(phrase)]
    subprocess.run(args)


if __name__ == "__main__":
    
    say("Now starting the listening section of the test.")
    say("The listening section is finished.")
    say("Good job!")

    for n in range(10):
        say(f"Listening Number {n + 1}")

    for n in range(5):
        number_times_str = "times" if n+1 > 1 else "time"
        say(f"The audio will play {n+1} {number_times_str}", filename=f"audio_play_{n+1}")

    say("Before we start listening, you can read the questions.")

    save_tone(length=0.6, hz=1318.510, vol=-21, out_file="E6") #E6 tone
    save_tone(length=0.25, hz=880, vol=-22, out_file="A5") #A5 tone
