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

def sanitize_phrase(phrase: str) -> str:
    phrase = phrase.lower()
    for c in "!@#$%^&*(){}[];:'\",<.>/?\\":
        phrase = phrase.replace(c, "")
    phrase = phrase.replace(" ", "_")
    return phrase

def save_tone(length=0.6, hz=1000, vol=-22):
    """ Play a tone with sox and sleep for one second """
    out_file = ASSET_FOLDER / Path(f"tone_{length}s@{hz}.mp3")
    print("making", out_file)
    args = ["sox", "-n", "-r", "44100", "-c", "1", str(out_file), "synth", str(length), "sine", str(hz), "vol", f"{vol}db",]
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

    save_tone()
    save_tone(length=0.3, hz=900, vol=-25)
