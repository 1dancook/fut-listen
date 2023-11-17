
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

ASSETS_PATH = Path(__file__).parent / 'assets'

def play_audio(path: Path, really_quiet=True) -> None:
    args = ["mpv", str(path)]
    if really_quiet:
        args.append("--really-quiet")
    run_subprocess(args)

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

def wait(seconds: int) -> None:
    notify(f"Waiting for {seconds} second(s).")
    print("    ", end="", flush=True)
    for x in range(seconds):
        print(".", end="", flush=True)
        if x + 1 > seconds - 3:    # Play three tones at the end
            play_audio(ASSETS_PATH / "A5.mp3")
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

def play_file(number, audio_file, delay, reading_delay, repeat, confirm_before, no_tone, no_read):
    """ Go through a process of playing a file for NUMBER times. """

    play_audio(ASSETS_PATH / f"listening_number_{number}.m4a")
    play_audio(ASSETS_PATH / f"audio_play_{number}.m4a")

    if not no_read and reading_delay > 0:
        play_audio(ASSETS_PATH / "before_we_start_listening_you_can_read_the_questions.m4a")
        confirm_or_delay(confirm_before, reading_delay)

    for x in range(repeat):
        if not no_tone:
            play_audio(ASSETS_PATH / "E6.mp3")
        notify(f"Playing {audio_file.name}")
        play_audio(audio_file, really_quiet=False)
        confirm_or_delay(confirm_before, delay)


@click.command()
@click.option("-p", "--path", type=click.Path(exists=True), help="Specify a path", required=False)
@click.option("-d", "--delay", default=10, help="Specify delay between plays", required=False)
@click.option("-r", "--repeat", default=2, help="Specify the number of times to repeat each audio file.", required=False)
@click.option("--reading-delay", default=15, help="Specify time given to read questions.", required=False)
@click.option("-c", "--confirm-before", is_flag=True, default=False, help="Confirm before playing an audio file.", required=False)
@click.option("-e", "--exclude", multiple=True, type=click.Path(), help="Exclude file (can provide multiple)", required=False)
@click.option("--no-start", is_flag=True, default=False, help="Don't play the start instruction.", required=False)
@click.option("--no-end", is_flag=True, default=False, help="Don't play the end instruction.", required=False)
@click.option("--no-tone", is_flag=True, default=False, help="Don't play the tone before an audio file.", required=False)
@click.option("--no-read", is_flag=True, default=False, help="Don't give read time.", required=False)
@click.option("--ext", default="mp3", help="The audio file extension to use.", required=False)
def cli(path, delay, repeat, reading_delay, confirm_before, exclude, no_start, no_end, no_tone, no_read, ext):
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

    # Check that the delay is at least something!
    if delay < 5:
        raise ValueError("You should use a delay longer than 5 seconds.")

    # Set the path to current directory if not supplied
    if path:
        path = Path(path).expanduser().absolute()
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
    if not click.confirm(prompt_string, default=True, show_default=False, prompt_suffix=""):
        quit()

    # Start section
    if not no_start:
        play_audio(ASSETS_PATH / "now_starting_the_listening_section_of_the_test.m4a")
        sleep(1)

    # Play audio files
    for number, audio_file in enumerate(audio_files, start=1):
        click.secho("="*60, dim=True)
        notify(f"Starting #{number}: {audio_file.name}")
        play_file(number, audio_file, delay, reading_delay, repeat, confirm_before, no_tone, no_read)

    # End section
    if not no_end:
        play_audio(ASSETS_PATH / "the_listening_section_is_finished.m4a")


if __name__ == "__main__":
    cli()
