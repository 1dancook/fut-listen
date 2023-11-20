
import subprocess
from pathlib import Path
from time import sleep
import click

s1 = r"   -// ┏━╸╻ ╻╺┳╸   ╻  ╻┏━┓╺┳╸┏━╸┏┓╻ \\-   ".center(80)
s2 = r"-+=||  ┣╸ ┃ ┃ ┃ ╺━╸┃  ┃┗━┓ ┃ ┣╸ ┃┗┫  ||=+-".center(80)
s3 = r"   -\\ ╹  ┗━┛ ╹    ┗━╸╹┗━┛ ╹ ┗━╸╹ ╹ //-   ".center(80)
SPLASH = f"{s1}\n{s2}\n{s3}"
SPLASH = SPLASH.replace("/", click.style("/", fg=246))
SPLASH = SPLASH.replace("\\", click.style("\\", fg=246))
SPLASH = SPLASH.replace("|", click.style("|", fg=250))
SPLASH = SPLASH.replace("=", click.style("=", fg=244))
SPLASH = SPLASH.replace("+", click.style("+", fg=241))
SPLASH = SPLASH.replace("-", click.style("-", fg=239))

ASSETS_PATH = Path(__file__).parent / 'assets'

def horizontal_bar(width=80, fg=242, ch="─"):
    click.secho(ch*width, fg=fg)

def get_audio_duration(file_path):
    # Use ffprobe to get the duration of an audio file
    # returns as milliseconds
    result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
            )
    duration = round(float(result.stdout) * 1000)
    return duration

class AudioPlayer():
    """ Holds the state and manages the logic of playing audio files """

    def __init__(self, audio_files, delay, repeat, audio_only, reading_delay, confirm_before, no_start, no_end, no_tone, no_read):
        self.audio_files = audio_files
        self.delay = delay
        self.repeat = repeat
        self.audio_only = audio_only
        self.reading_delay = reading_delay
        self.confirm_before = confirm_before
        self.no_start = no_start
        self.no_end = no_end
        self.no_tone = no_tone
        self.no_read = no_read

    def run(self):
        if not self.no_start and not self.audio_only:
            horizontal_bar()
            self.start()
        self.play_files()
        if not self.no_end and not self.audio_only:
            horizontal_bar()
            self.end()

    def start(self):
        self.notify("Announcing the start of the Listening Section.", notify_str="Announcement", fg="blue")
        self.play(ASSETS_PATH / "now_starting_the_listening_section_of_the_test.m4a")
        sleep(1)

    def end(self):
        self.notify("Announcing the end of the Listening Section.", notify_str="Announcement", fg="blue")
        self.play(ASSETS_PATH / "the_listening_section_is_finished.m4a")

    def play(self, path: Path, really_quiet=True, background=False) -> None:
        args = ["mpv", "--no-config", str(path)]
        if really_quiet:
            args.append("--really-quiet")
        if background:
            subprocess.Popen(['mpv', str(path), "--no-terminal", "--no-config"]) # really quiet is necessary
        else:
            subprocess.run(args)

    def play_with_progress(self, path):
        duration = get_audio_duration(path)
        
        # Start mpv in the background
        subprocess.Popen(['mpv', str(path), "--no-terminal"]) # really quiet is necessary
        color = "green"

        l_bracket = click.style("[", fg=color)
        r_bracket = click.style("]", fg=color)

        label = click.style("[PLAYING]", fg=color)

        # Create a progress bar
        with click.progressbar(
                range(0, duration, 100), 
                label=label, 
                show_eta=False, 
                fill_char=click.style("─", fg=color), 
                empty_char=click.style("─", fg=238), 
                color=True, 
                width=50,
                bar_template=f'%(label)s {l_bracket}%(bar)s{r_bracket}  %(info)s of {duration / 1000}s'
                ) as bar:
            # sleep for every bit
            for x in bar:
                #print(dir(bar))
                sleep(0.1)


    def notify(self, text: str, notify_str: str="info", fg="green", bold=False) -> None:
        """ Print out a formatted notification string given certain text """
        notify_str = click.style(f"[{notify_str.upper()}]", fg=fg, bold=bold)
        prefix = click.style("", dim=True)
        click.secho(f"{prefix}{notify_str} {text}")

    def wait(self, seconds: int) -> None:
        # Create a progress bar
        color = "yellow"
        label = click.style("[WAITING]", fg=color)
        l_bracket = click.style("[", fg=color)
        r_bracket = click.style("]", fg=color)
        with click.progressbar(
                range(0, seconds), 
                label=label,
                show_eta=False, 
                fill_char=click.style("─", fg=color), 
                empty_char=click.style("─", fg=238), 
                color=True, 
                width=50,
                bar_template=f'%(label)s {l_bracket}%(bar)s{r_bracket}  %(info)s of {seconds}s'
                ) as bar:
            # sleep for every bit
            for x in bar:
                if x + 1 > seconds - 3 and not self.no_tone and not self.audio_only and not self.confirm_before:
                    # Play three tones at the end
                    self.play(ASSETS_PATH / "A5.mp3", background=True)
                sleep(1)

    def play_files(self):
        """ Main process to play the audio files """
        for number, audio_file in enumerate(self.audio_files, start=1):
            horizontal_bar()
            self.notify(f"Audio #{number}", notify_str="Starting", fg="magenta")
            self.play_file(number, audio_file)
            self.notify(f"Audio #{number}", notify_str="Finished", fg="magenta")

    def play_file(self, number, audio_file):
        """ Go through a process of playing a file for NUMBERth time. """

        if not self.audio_only:
            self.notify(f"Listening Number {number}", notify_str="Announcement", fg="blue")
            self.play(ASSETS_PATH / f"listening_number_{number}.m4a")
            self.play(ASSETS_PATH / f"audio_play_{number}.m4a")

        if not self.no_read and self.reading_delay > 0 and not self.audio_only:
            self.notify(f"Pause for reading time", notify_str="Announcement", fg="blue")
            self.play(ASSETS_PATH / "before_we_start_listening_you_can_read_the_questions.m4a")
            self.wait(self.reading_delay)

        repeat_str = click.style(f"[Repeat: {self.repeat}x]", fg="green") 
        if self.repeat == 0:
            repeat_str = click.style("[No Repeat]", fg=246)

        delay_str = click.style(f"[Post-Delay: {self.delay}s]", fg="yellow") 
        if self.audio_only:
            delay_str = click.style("[No Post-delay]", fg=246)

        self.notify(f"{audio_file.name}  {repeat_str}  {delay_str}", notify_str="PLAY", fg="green")
        for x in range(self.repeat + 1): # adding one to properly do the repeat
            if self.confirm_before:
                prompt_string = click.style("> Press [ENTER] to continue...", bold=True)
                click.confirm(prompt_string, default=True, show_default=False, prompt_suffix="")

            elif not self.no_tone and not self.audio_only:
                self.play(ASSETS_PATH / "E6.mp3")

            self.play_with_progress(audio_file)

            if not self.confirm_before:
                self.wait(self.delay)

def do_splash_start(audio_files):
    # Confirm the order and confirm whether or not to continue
    click.clear()
    click.secho(SPLASH)
    horizontal_bar()
    click.secho(f"The following {len(audio_files)} file(s) will play in this order:")

    for n, audio_file in enumerate(audio_files, start=1):
        click.secho(f"  {n:02}. {audio_file.name}")

    prompt_string = click.style("Are you ready to start?", bold=True)
    if not click.confirm(prompt_string, default=True, show_default=False, prompt_suffix=""):
        quit()

def get_path(ctx, param, value):
    if not value:
        return Path(".").absolute()
    return Path(value).expanduser().absolute()



@click.command(context_settings={"show_default":True})
@click.option("-p", "--path", type=click.Path(exists=True), callback=get_path, help="Specify a path to search for files.", required=False)
@click.option("-d", "--delay", default=10, help="Specify post-delay after an audio file plays. Doing a delay less than 5 will impact tones.", required=False)
@click.option("-r", "--repeat", default=1, help="Specify the number of times to repeat each audio file. Use 0 for no repeating.", required=False)
@click.option("-a", "--audio-only", is_flag=True, default=False, help="Audio only. Disables all announcements and tones.", required=False)
@click.option("--reading-delay", default=15, help="Specify time given to read questions.", required=False)
@click.option("-c", "--confirm-before", is_flag=True, default=False, help="Confirm before playing an audio file.", required=False)
@click.option("-x", "--exclude", multiple=True, type=click.Path(), help="Exclude file (can provide multiple).", required=False)
@click.option("--no-start", is_flag=True, default=False, help="Disables the starting instruction.", required=False)
@click.option("--no-end", is_flag=True, default=False, help="Disables the ending instruction.", required=False)
@click.option("--no-tone", is_flag=True, default=False, help="Disables the tones.", required=False)
@click.option("--no-read", is_flag=True, default=False, help="Disables the read time.", required=False)
@click.option("--ext", default="mp3", help="The audio file extension to use", required=False)
def cli(path, delay, repeat, audio_only, reading_delay, confirm_before, exclude, no_start, no_end, no_tone, no_read, ext):
    """
    fut-listen

    This command line utility is designed to play the audio files in the current working directory or one specified by --path.

    Any audio files (.mp3 by default) will be sorted by name. The default behavior is:

    \b
    1. Play start instruction
    2. For each audio file:
        1. Play announcements about the Listening Number
        2. Play announcement about reading questions before listening (15s)
           ( warning tones are played )
        3. Play the audio file
        4. Delay for 10s
           ( warning tones are played )
        ( Repeat 3 + 4 )
    3. Play end instruction

    """

    # Check that mpv and sox are installed
    if subprocess.run(["which", "mpv"], capture_output=True).returncode == 1:
        click.secho("mpv was not found. Install mpv.", fg="red")
        quit()

    # Make a list of paths to exclude
    excluded_paths = [Path(excluded_path).absolute() for excluded_path in exclude]

    # Glob for files and sort them
    globbed_files = path.glob(f"*.{ext}")
    audio_files = sorted([file.absolute() for file in globbed_files if file.absolute() not in excluded_paths])

    # Quit if one of the audio files doesn't exist
    for audio_file in audio_files:
        if not audio_file.exists():
            print(f"{audio_file.name()} does not exist. Quitting.")
            quit()

    # Quit if there are no audio files
    if len(audio_files) == 0:
        click.secho(f"No .{ext} files found.")
        quit()

    # Do the splash start and confirm before continuing
    do_splash_start(audio_files)

    # Initialize and start the audio player
    audio_player = AudioPlayer(
            audio_files, 
            delay, 
            repeat, 
            audio_only, 
            reading_delay, 
            confirm_before, 
            no_start, 
            no_end, 
            no_tone, 
            no_read, 
            )

    audio_player.run()


if __name__ == "__main__":
    cli()
