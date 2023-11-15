
import subprocess
from pathlib import Path
from time import sleep
import click

SPLASH = """\

  /`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`
  /`     ┏━╸╻ ╻╺┳╸   ╻  ╻┏━┓╺┳╸┏━╸┏┓╻     /`
  /`     ┣╸ ┃ ┃ ┃ ╺━╸┃  ┃┗━┓ ┃ ┣╸ ┃┗┫     /`
  /`     ╹  ┗━┛ ╹    ┗━╸╹┗━┛ ╹ ┗━╸╹ ╹     /`
  /`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`
"""


def notify(text, notify_type="info"):
    """ Print out a formatted notification string given certain text """
    notify_str = ""
    if notify_type.lower().strip() == "info":
        notify_str = click.style("[INFO]", bg="green", fg="black")
    prefix = click.style(">>> ", dim=True)
    click.secho(f"{prefix}{notify_str} {text}")

def run_subprocess(args, capture_output=True, text=True):
    # TODO: expand the exceptions bit
    try:
        subprocess.run(args)
    except:
        pass

def macos_set_tts_language(language):
    """
    Set the TTS language for MacOS

    Example:
        macos_set_tts_language("en") # English
        macos_set_tts_language("ja") # Japanese

    You should have the speech downloaded.

    """

    args = ["defaults", "write", "com.apple.speech.voice.prefs", "SystemTTSLanguage", language]
    run_subprocess(args)

def say(phrase, rate, interactive=True):
    """ Use macos `say` utility for text to speech. """
    args = ["say", "--rate", str(rate), str(phrase)]
    if interactive:
        args.append("-i")
    run_subprocess(args)


def wait(seconds: int) -> None:
    notify(f"Waiting for {seconds} second(s).")
    print("    ", end="", flush=True)
    for x in range(seconds):
        print(".", end="", flush=True)
        if x + 1 > seconds - 3:    # Play three tones at the end
            play_tone(length=0.3, hz=900, vol=-35, pause=False)
            sleep(0.7)
        else:
            sleep(1)
    print(" continuing")

def confirm_or_delay(confirm_before, delay):
    """ Confirm to continue or wait before continuing """
    if confirm_before:
        prompt_string = click.style(">>> Press [ENTER] to continue...", bold=True)
        click.confirm(prompt_string, default=True, show_default=False, prompt_suffix="")
        return
    else:
        wait(delay)

def play_tone(length=0.6, hz=1000, vol=-30, pause=True):
    """ Play a tone with sox and sleep for one second """
    args = ["play", "--no-show-progress", "-n", "synth", str(length), "sin", str(hz), "vol", f"{vol}dB"]
    run_subprocess(args)
    if pause:
        sleep(1) # needs a short pause afterward


def play_file(number, audio_file, delay, reading_delay, repeat, confirm_before, no_tone, no_read, rate):
    """ Go through a process of playing a file for NUMBER times. """

    say(f"Listening number {number}", rate)
    number_times_str = "times" if repeat > 1 else "time"
    say(f"The audio will play {repeat} {number_times_str}", rate)

    if not no_read and reading_delay > 0:
        say(f"Before we start listening, you can read the questions.", rate)
        confirm_or_delay(confirm_before, reading_delay)

    for x in range(repeat):
        if not no_tone:
            play_tone()
        notify(f"Playing {audio_file.name}")
        run_subprocess(["mpv", audio_file])
        confirm_or_delay(confirm_before, delay)


@click.command()
@click.option("-p", "--path", type=click.Path(exists=True), help="Specify a path", required=False)
@click.option("-d", "--delay", default=10, help="Specify delay between plays", required=False)
@click.option("-r", "--rate", default=145, help="Specify the rate for TTS", required=False)
@click.option("--repeat", default=2, help="Specify the number of times to repeat each audio file.", required=False)
@click.option("--reading-delay", default=15, help="Specify time given to read questions.", required=False)
@click.option("-c", "--confirm-before", is_flag=True, default=False, help="Confirm before playing an audio file.", required=False)
@click.option("-e", "--exclude", multiple=True, type=click.Path(), help="Exclude file (can provide multiple)", required=False)
@click.option("--no-start", is_flag=True, default=False, help="Don't play the start instruction.", required=False)
@click.option("--no-end", is_flag=True, default=False, help="Don't play the end instruction.", required=False)
@click.option("--no-tone", is_flag=True, default=False, help="Don't play the tone before an audio file.", required=False)
@click.option("--no-read", is_flag=True, default=False, help="Don't give read time.", required=False)
@click.option("--ext", default="mp3", help="The audio file extension to use.", required=False)
def cli(path, delay, rate, repeat, reading_delay, confirm_before, exclude, no_start, no_end, no_tone, no_read, ext):
    """
    fut-listen

    This command line utility is designed to play the conversation files
    in the current working directory or one specified by --path.

    Any audio files (.mp3) will be sorted by name. The default behavior is:

    1. Play start instruction

    2. Play each audio file 2 times

    3. Play end instruction

    Between sections there will be a default pause of 10 seconds. Warning tones are generated
    and played 3 seconds before.
    """

    # Check that mpv and sox are installed
    if subprocess.run(["which", "mpv"], capture_output=True).returncode == 1:
        click.secho("mpv was not found. Install mpv.", fg="red")
        quit()

    if subprocess.run(["which", "sox"], capture_output=True).returncode == 1:
        click.secho("sox was not found. Install sox.", fg="red")
        quit()

    # Check that the delay is at least something!
    if delay < 5:
        raise ValueError("You should use a delay longer than 5 seconds.")

    # First set the TTS language to English
    macos_set_tts_language("en")

    # Set the path to current directory if not supplied
    if not path:
        path = Path(".").absolute()

    # Glob for .mp3 files and sort them
    audio_files = sorted([file for file in path.glob(f"*.{ext}")])

    if len(audio_files) == 0:
        click.secho(f"No .{ext} files found.")
        quit()

    # Confirm the order and confirm whether or not to continue
    click.clear()
    splash = SPLASH.replace("`", click.style("`", fg="blue", bold=True))
    splash = splash.replace("/", click.style("/", fg="blue"))
    click.secho(splash)
    click.secho(f"The following {len(audio_files)} file(s) will play in this order:")
    click.secho("-"*50, dim=True)

    for n, audio_file in enumerate(audio_files, start=1):
        click.secho(f"  {n:02}. {audio_file.name}")

    click.secho("-"*50, dim=True)
    prompt_string = click.style("Are you ready to start?", bold=True)
    if not click.confirm(prompt_string, prompt_suffix=""):
        quit()

    # Start section
    if not no_start:
        say("Now starting the listening section of the test.", rate)
        sleep(1)

    # Play audio files
    for number, audio_file in enumerate(audio_files, start=1):
        click.secho("="*60, dim=True)
        notify(f"Starting #{number}: {audio_file.name}")
        play_file(number, audio_file, delay, reading_delay, repeat, confirm_before, no_tone, no_read, rate)

    # End section
    if not no_end:
        say("The listening section is finished.", rate)


if __name__ == "__main__":
    cli()
